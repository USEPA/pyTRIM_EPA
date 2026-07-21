from typing import IO
from ..schema.entities.chemicals import Chemical
from ..schema.entities.environment import Parcel
from ..schema.utils.caching import CacheManager
from ..schema.scenarios.models import *
from .generic import GenericService, PermissionsMixin
from .parameters import parameterize
from .users import UserService

__all__ = ['ScenarioService']


class ScenarioService(GenericService[Scenario], PermissionsMixin):
    __model__ = parameterize(Scenario)

    def __init__(self, model, *args, **kwargs):
        self.__instance = model

    def user_permissions(self):
        scenario = self.__instance
        users = {
            u: scenario.access_level(u)
            for u in UserService.get_all() if u.can('view', scenario, ignore_superuser=True)
        }
        return users

    def get_surface_runoff(self):
        return get_scenario_surface_runoff(self.__instance)

    def import_aermod(self, filestream: IO, for_chemical: Chemical, metadata: dict = {}):
        return import_aermod_to_scenario(self.__instance, filestream, for_chemical, metadata=metadata)


@CacheManager.with_caching('surface_runoff')
def get_scenario_surface_runoff(scen):
    soil_comps = []
    water_comps = []
    sink_comps = []
    for c in scen.compartments:
        if c.media.isa('Surface_Soil'):
            soil_comps.append(c)
        elif c.media.isa('Surface_Water'):
            water_comps.append(c)
        elif (c.media.isa("Advection") and not c.media.isa("Flush$")):
            sink_comps.append(c)
    runoffs = {}
    for sender in soil_comps + water_comps:
        sending_parcel = sender.volume_element.parcel.name
        runoffs[sending_parcel] = {}
        runoffs[sending_parcel]['sink'] = 0
        for receiver in soil_comps + sink_comps + water_comps:
            receiving_parcel = receiver.volume_element.parcel.name
            if sender in water_comps:
                if sender == receiver:
                    runoffs[sending_parcel][receiving_parcel] = 1
                else:
                    runoffs[sending_parcel][receiving_parcel] = 0
                continue
            runoff_frac = sender.FractionOfTotalRunoff(receiver=receiver)
            if receiver in sink_comps:
                runoffs[sending_parcel]['sink'] += runoff_frac
            else:
                runoffs[sending_parcel][receiving_parcel] = runoff_frac
    return runoffs


AERMOD_UNITS = {
    'surfaceDepositionRate': 'g / day',
    'aermodAirConcentration': 'ug / m^3'
}


def import_aermod_to_scenario(scenario: Scenario, filestream: IO, for_chemical: Chemical, metadata: dict = {}):
    import pandas as pd
    from shapely import MultiPoint, Point
    from shapely.ops import nearest_points
    from trim_core.aermod import AermodReader
    from trim_core.coordinates import CoordinateMapper

    try:
        df = AermodReader(filestream).as_dataframe()
    except Exception as e:
        print('parse airmod lines error:', e)
        import traceback
        traceback.print_exc()
        raise

    # print('>>>>>>>>>> Initial load:')
    # print(df)

    # Filter by zflag
    if 'ZFLAG' in df.columns.values:
        zflag_restriction = metadata.get('zflag_restriction')
        if zflag_restriction is not None:
            # Filter to user-specified value
            if zflag_restriction not in df.ZFLAG.unique():
                raise ValueError(
                    f'ZFLAG={zflag_restriction} not found in file'
                )
            df = df[df["ZFLAG"] == zflag_restriction].copy()
        avail_zflags = df.ZFLAG.unique()
        if len(avail_zflags) > 1:
            # By default, filter to lowest value
            lowest_zflag = min(avail_zflags)
            df = df[df["ZFLAG"] == lowest_zflag].copy()

    # print('>>>>>>>>>> ZFLAG filtered:')
    # print(df)

    # drop collocated X,Y receptors while keeping the lowest elevation point
    df = df.sort_values(['X', 'Y', 'ZELEV']).drop_duplicates(
        ['X', 'Y'], keep='first'
    )

    # remove if NET ID = POLGRID. This does not always work.
    # We will also need a user restriction to limit
    # receptors intended for TRIM modeling
    # – i.e., Cartesian grid with no overlapping receptors
    df_aermod = df[~df['NET ID'].str.startswith('POLGRID')].copy()

    try:
        # Convert AERMOD X and Y to WGS84 coordinates.
        coord_sys = metadata.get('coordinate_system') or ''
        if coord_sys.upper() == 'UTM':
            utm_zone = metadata['utm_zone']
            coord_mapper = CoordinateMapper(
                'UTM', 'WGS84_LONGLAT', utm_zone=utm_zone
            )
            df_aermod['wgs_x'] = df_aermod.apply(
                lambda z: coord_mapper.translate(float(z.X), float(z.Y))[0],
                axis=1
            )
            df_aermod['wgs_y'] = df_aermod.apply(
                lambda z: coord_mapper.translate(float(z.X), float(z.Y))[1],
                axis=1
            )
        else:
            df_aermod['wgs_x'] = df_aermod.X.astype('float')
            df_aermod['wgs_y'] = df_aermod.Y.astype('float')
    except Exception as e:
        print('parse airmod wgs_x/wgs_y error:', e)
        import traceback
        traceback.print_exc()
        raise

    # print('>>>>>>>>>> Mapped coords:')
    # print(df_aermod)

    parcels: dict[int, Parcel] = {p.id: p for p in scenario.parcels}

    def get_containing_parcel_id(x, y):
        for p in parcels.values():
            if p.contains_point(x, y):
                return p.id
        return None

    def get_compartment(pcl_id, media):
        compartment = parcels[pcl_id].get_compartment(
            media=media, or_child=False
        )
        if not compartment:
            return None
        if isinstance(compartment, list):
            compartment = compartment[0]
        return compartment

    def get_compartment_height(pcl_id, media, default=(0 * scenario.parameters.unit_registry('m'))):
        compartment = get_compartment(pcl_id, media)
        if not compartment:
            return default
        return compartment.height

    def get_compartment_volume(pcl_id, media, default=(0 * scenario.parameters.unit_registry('m^3'))):
        compartment = get_compartment(pcl_id, media)
        if not compartment:
            return default
        return compartment.volume

    try:
        # add parcel location to each receptor in aermod file
        df_aermod['parcel_id'] = df_aermod.apply(
            lambda z: get_containing_parcel_id(z.wgs_x, z.wgs_y),
            axis=1
        )
        # drop any receptors that are not mapped to layout
        df_aermod = df_aermod.dropna(
            subset=['parcel_id']
        ).reset_index(drop=True)
        # add parcel areas (m^2)
        df_aermod['parcel_area'] = df_aermod.parcel_id.apply(
            lambda p_id: parcels[p_id].area.magnitude
        )
        df_aermod['air_compartment_height'] = df_aermod.parcel_id.apply(
            lambda p_id: get_compartment_height(p_id, 'Air')
        )
        df_aermod['air_compartment_volume'] = df_aermod.parcel_id.apply(
            lambda p_id: get_compartment_volume(p_id, 'Air')
        )
    except Exception as e:
        print(f"Error finding parcels corresponding to sources: {e}")
        import traceback
        traceback.print_exc()
        raise

    # print('>>>>>>>>>> Added parcel areas & compartment heights:')
    # print(df_aermod)

    def get_distance_to_nearest_neighbor(from_x, from_y, neighbors_df):
        point = Point(from_x, from_y)  # make a shapely point object of current point of interest
        other_points = MultiPoint([
            Point(x, y) for x, y in zip(neighbors_df.X, neighbors_df.Y)
            if (x != from_x or y != from_y)
        ])
        nearest_point = nearest_points(point, other_points)
        dist = point.distance(nearest_point[1])  # distance of point of interest to nearest neighbor
        return dist

    try:
        # compute number of days of cumulative
        ndays = df_aermod['NUM HRS'].loc[1] / 24
        spacing = metadata.get('spacing')
        if spacing == 'Non-Uniform':
            # Compute weighted average of receptors in the parcel
            # using distance of influence of each receptor as weight
            # First, compute distance to nearest receptor
            df_all_coords = pd.DataFrame({
                'X': df_aermod.wgs_x,
                'Y': df_aermod.wgs_y
            })
            df_aermod['spacing'] = df_aermod.apply(
                lambda z: get_distance_to_nearest_neighbor(
                    from_x=z.wgs_x, from_y=z.wgs_y, neighbors_df=df_all_coords
                ),
                axis=1
            )
            # Calculate receptor area (m^2)
            dft = df_aermod.copy()  # temp df
            # area of influence of the receptor computed as a square
            # with side equal to distance of nearest receptor
            dft['rep_area'] = (dft['spacing']) ** 2
            # first step of weighting by area of influence
            # Calculate (ug) for each receptor volume (m^3)
            dft['weighted_conc'] = dft['AVERAGE CONC'] * dft['rep_area'] * dft['air_compartment_height']  # ug/m^3 * (m^2 * m) = ug
            # Calculate (g) for each receptor area (m^2)
            dft['weighted_dry_depo'] = dft['DRY DEPO'] * dft['rep_area']  # g/m^2 * m^2 = g
            dft['weighted_wet_depo'] = dft['WET DEPO'] * dft['rep_area']  # g/m^2 * m^2 = g
            # Sum (ug)/(g) by parcel
            aggdep = dft.groupby(['parcel_id', 'parcel_area', 'air_compartment_height'])[[
                'weighted_conc', 'weighted_dry_depo', 'weighted_wet_depo',
                'spacing', 'rep_area'
            ]].sum().reset_index()
            # second step of weighting (divide by sum of weights in parcel)
            aggdep['agg_conc'] = (  # Calculate flux by correcting (ug) by volume (m^3)
                (aggdep['weighted_conc'] / aggdep['air_compartment_volume'])  # ug / m^3
            )
            # Calculate flux by correcting (g) by number of days in AERMOD modeling period
            aggdep['agg_dry_depo'] = (
                aggdep['weighted_dry_depo'] / ndays  # g / day
            )
            aggdep['agg_wet_depo'] = (
                aggdep['weighted_wet_depo'] / ndays  # g / day
            )
        else:
            # Assume uniform spacing
            # Compute flat averages of all receptors in the parcel
            # Calculate average for each parcel (g/m^2)
            aggdep = df_aermod.groupby(['parcel_id', 'parcel_area', 'air_compartment_height'])[[
                'AVERAGE CONC', 'DRY DEPO', 'WET DEPO'
            ]].mean().reset_index()
            aggdep['agg_conc'] = (
                aggdep['AVERAGE CONC']  # ug/m^3
            )
            # Calculate flux by correcting (g/m^2)
            # by number of days in AERMOD modeling period
            aggdep['agg_dry_depo'] = (
                (aggdep['DRY DEPO'] / ndays) * aggdep['parcel_area']  # (g/m^2 / day) * m^2 = g/day
            )
            aggdep['agg_wet_depo'] = (
                (aggdep['WET DEPO'] / ndays) * aggdep['parcel_area']  # (g/m^2 / day) * m^2 = g/day
            )
    except Exception as e:
        print(f'Possible Grouping Error: {e}')
        import traceback
        traceback.print_exc()
        raise

    # print('>>>>>>>>>> Added aggregate deposition:')
    # print(aggdep)

    try:
        aggdep = aggdep[[
            'parcel_id', 'agg_conc', 'agg_dry_depo', 'agg_wet_depo'
        ]]
        aggdep.columns = [
            'parcel_id', 'Concentration_Avg', 'Dry_Deposition_Avg', 'Wet_Deposition_Avg'
        ]
        aermod_results: dict[int, dict[str, float]] = aggdep.set_index('parcel_id').to_dict(orient='index')
    except Exception as e:
        print('parse airmod res_json error:', e)
        import traceback
        traceback.print_exc()
        raise

    # print('>>>>>>>>>> Result JSON:')
    # print(aermod_results)

    def update_aermod_value(parcel: Parcel, target_media: str, target_param: str, aermod_val: float):
        compartment = parcel.get_compartment(
            media=target_media, or_child=False
        )
        # print('\t>', compartment)
        if not compartment:
            return
        if isinstance(compartment, list):
            compartment = compartment[0]

        param = compartment.parameters.get_custom(target_param)
        # print('\t\t->', param)

        if not param:
            compartment.parameters.add(
                target_param, formula=f'{aermod_val} if chemical.id == {for_chemical.id} else 0',
                unit=AERMOD_UNITS[target_param]
            )

    try:
        chem_spec = metadata.get('chemical_species') or 'Particle'
        for p_id, vals in aermod_results.items():
            parcel = parcels[p_id]
            # print('*', parcel)
            # print(vals)

            update_aermod_value(
                parcel, f'Source|Dry_{chem_spec}', 'surfaceDepositionRate',
                vals['Dry_Deposition_Avg']
            )
            update_aermod_value(
                parcel, f'Source|Wet_{chem_spec}', 'surfaceDepositionRate',
                vals['Wet_Deposition_Avg']
            )
            update_aermod_value(
                parcel, 'Air', 'aermodAirConcentration',
                vals['Concentration_Avg']
            )
    except Exception as e:
        print('parse airmod formulas error:', e)
        import traceback
        traceback.print_exc()
        raise

    return aermod_results
