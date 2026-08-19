import pandas as pd
import numpy as np
from trim_db.schema import ureg, Parcel
from trim_db.schema.utils.serialize import register_serializer
from trim_db.schema.parameters.models import ParameterDefinition, CustomParameter
from trim_db.services import *


@register_serializer(Parcel)
def serialize_parcel(pcl: Parcel):
    general_params = get_general_params(pcl)
    water_params = get_water_params(pcl, general_params['parcelType'])
    source_params = get_source_params(pcl)
    soil_abiotic_params = get_soil_abiotic_params(pcl)
    initial_conc = get_initial_concentrations(pcl)

    try:
        cdv = pcl.get_compartment("DryVaporSource")
        spacing_param = cdv.parameters.get("ReceptorSpacing")
        spacing_val = spacing_param.value
    except Exception:
        spacing_val = None

    s = {
        'id': pcl.id,
        'name': pcl.name,
        'description': pcl.description if pcl.description else "None",
        'receptor_spacing': spacing_val,
        'vertices': pcl.vertices,
        'area': pcl.area.m_as('m^2'),
        'compartment_map': {ve.name: [c.name for c in ve.compartments] for ve in pcl.volume_elements},
        **general_params,
        **water_params,
        **source_params,
        **soil_abiotic_params,
        **initial_conc
    }
    try:
        s['mercury_transformation_rates'] = (
            ChemicalService.get_mercury_transformation_rates(pcl)
        )
    except AssertionError:
        pass  # No Mercuries Present
    return s


def safe_get_val(comp, k, default=None):
    param = comp.parameters.get(k)
    if param is None:
        return default
    v = param.value
    if v is None and isinstance(param, ParameterDefinition):
        return default
    return v


def get_general_params(pcl):
    air = False
    water = False
    land = False
    wetland = False
    farm_food_chain = False
    fish_food_web = False

    air_density = None
    air_height = None
    dust_load = None
    dust_density = None
    fraction_organic_matter_on_particulates = None
    erosion_source = 1
    total_erosion_rate = None
    is_tilled = False

    erosion_table_params = get_erosion_params(pcl)

    surface_soil_height = None

    diet_by_media = {}
    biomass_by_media = {}
    bw_by_media = {}

    land_use = None

    # FIXME verify this is okay
    root_soil_height = pcl.get_compartment(media="Root_Zone")
    if root_soil_height:
        root_soil_height = root_soil_height[0].volume_element.height.m_as('m')
        root_soil_height = round(root_soil_height, 4)
    vadose_soil_height = pcl.get_compartment(media="Vadose_Zone")
    if vadose_soil_height:
        vadose_soil_height = vadose_soil_height[0].volume_element.height.m_as('m')
        vadose_soil_height = round(vadose_soil_height, 4)
    groundwater_height = pcl.get_compartment(media="Groundwater")
    if groundwater_height:
        groundwater_height = groundwater_height[0].volume_element.height.m_as('m')
        groundwater_height = round(groundwater_height, 4)

    for comp in pcl.compartments:
        # Check parcel type
        if comp.media.isa('Air', or_child=False):
            air = True
            if air_height is None:
                air_height = comp.volume_element.height.m_as('m')
                air_density = safe_get_val(comp, 'AirDensity', None)
                dust_load = safe_get_val(comp, 'DustLoad', None)
                dust_density = safe_get_val(comp, 'DustDensity', None)
                fraction_organic_matter_on_particulates = safe_get_val(
                    comp, 'FractionOrganicMatteronParticulates', None
                )
        elif comp.media.isa('Surface_Soil'):
            land = True
            if comp.media.isa('Tilled_Soil'):
                land_use = 'Tilled Soil'
            elif comp.media.isa('Untilled_Soil'):
                land_use = 'Untilled Soil'

            if surface_soil_height is None:
                surface_soil_height = comp.volume_element.height.m_as('m')
                total_erosion_rate = safe_get_val(comp, 'TotalErosionRate', None)
                if land_use == 'Tilled Soil': 
                    is_tilled = True
                elif land_use == 'Untilled Soil':
                    is_tilled = False
                else:
                    tillage = safe_get_val(comp, 'soilTillage', 0)
                    try:
                        if int(tillage) == 1:
                            is_tilled = True
                    except ValueError:
                        is_tilled = False
                        
        elif comp.media.isa('Surface_Water'):
            water = True
        elif comp.media.isa('Wetland'):
            wetland = True
        elif comp.media.isa('Farm'):
            farm_food_chain = True

        elif comp.media.isa('Aquatic'):  # Check for fish
            fish_food_web = True
            nm = comp.name
            fish_params = get_fish_params(comp)
            diet_by_media[nm] = fish_params['aquatic_diet_fractions']
            biomass_by_media[nm] = fish_params['aquatic_biomass']
            bw_by_media[nm] = fish_params['aquatic_bw']

        elif comp.media.isa('Coniferous_Forest'):  # Check land use
            land_use = 'Coniferous Forest'
        elif comp.media.isa('Deciduous_Forest'):
            land_use = 'Deciduous Forest'
        elif comp.media.isa('Agriculture'):
            land_use = 'Agriculture (General)'
        elif comp.media.isa('Grass'):
            land_use = 'Grasses/Herbs'

    if not land:
        land_use = 'N/A'  # No land use for air-only and water-only parcels

    if air:
        if water:
            parcel_type = 'Water & Air'
        elif land:
            parcel_type = 'Land & Air'
        else:
            parcel_type = 'Air Only'
    elif water:
        if land:
            parcel_type = 'Land & Water'
        else:
            parcel_type = 'Water Only'
    else:
        if land:
            parcel_type = 'Land Only'
        else:
            parcel_type = 'Empty'

    general_params = {
        'hasAir': 'Yes' if air else 'No',
        'airDensity': air_density,
        'airHeight': air_height,
        'dustLoad': dust_load,
        'dustDensity': dust_density,

        'hasLand': 'Yes' if land else 'No',
        'totalErosionRate': total_erosion_rate,
        'parcelType': parcel_type,
        'landUse': land_use,
        'hasFarmFoodChain': 'Yes' if farm_food_chain else 'No',
        'hasWetland': 'Yes' if wetland else 'No',

        'hasWater': 'Yes' if water else 'No',
        'hasFishFoodWeb': 'Yes' if fish_food_web else 'No',

        'surfaceSoilThickness': surface_soil_height,  
        'rootSoilThickness': root_soil_height,
        'vadoseSoilThickness': vadose_soil_height,
        "groundwaterZoneThickness": groundwater_height,
        'fractionOrganicMatterOnParticulates': fraction_organic_matter_on_particulates,
        'soilTillage': 'Yes' if is_tilled else 'No',

        'aquatic_diet_fractions': diet_by_media,
        'aquatic_biomass': biomass_by_media,
        'aquatic_bw': bw_by_media,

        **erosion_table_params
    }
    return general_params


def get_erosion_params(pcl):
    # HACKY
    erosion_table_params = {}
    for param in list(ParameterService.get_all(
        scenario_id=pcl.scenario_id, requirements=make_self_requirements(pcl)
    )):
        if not isinstance(param, CustomParameter):
            continue
        if not param.requirements == f'(self.id == {pcl.id})':
            continue
        if not(
            param.variable_name.startswith('erosion1-')
            or param.variable_name.startswith('erosion2-')
            or param.variable_name.startswith('erosion3-')
        ):
            continue
        if param.variable_name.endswith('-active'):
            erosion_table_params[
                param.variable_name.split('-')[0] + '-active'
            ] = EROSION_TABLE_PARAM_MAP.get(
                param.variable_name.split('-', 1)[1].rsplit('-', 1)[0]
            )
        else:
            erosion_table_params[param.variable_name] =  param.value
    return erosion_table_params


def make_self_requirements(obj):
    return f'(self.id == {obj.id})'


def get_soil_abiotic_params(pcl):
    comp_names = ["Soil_Surface", "Soil_Root_Zone", "Soil_Vadose_Zone", "Groundwater"]

    general_params = ['pH', 'FractionSand', 'OrganicCarbonContent', 'rho']
    gw_params = ['Porosity']
    soil_params = ['VolumeFraction_Vapor', 'AverageVerticalVelocity', 'VolumeFraction_Liquid']
    surf_params = [
        'AirSoilBoundaryThickness', 'FractionofAreaAvailableforErosion',
        'FractionofAreaAvailableforRunoff', 'FractionofAreaAvailableforVerticalDiffusion',
        'TotalRunoffRate'
    ]

    def get_magnitude(comp, param):
        val = comp.parameters.get(param)
        if val is None or val.value is None:
            return None
        return round(val.value, 5)

    soil_abiotic_params = {}

    for name in comp_names:
        comp = pcl.get_compartment(name)
        if not comp:
            continue
        soil_abiotic_params[name] = {
            k: get_magnitude(comp, k) for k in general_params
        }
        if name == 'Groundwater':
            soil_abiotic_params[name].update([
                (k, get_magnitude(comp, k)) for k in gw_params
            ])
        elif 'Soil_' in name:
            soil_abiotic_params[name].update([
                (k, get_magnitude(comp, k)) for k in soil_params
            ])
            if name == 'Soil_Surface':
                soil_abiotic_params[name].update([
                    (k, get_magnitude(comp, k)) for k in surf_params
                ])

    return {"soil_params": soil_abiotic_params}


def get_watershed_area(pcl):
    # Compute watershed area using Markoff chain approach
    # 1. get runoff fractions matrix (rom) and parcel areas as vector (pav)
    ro_array = ScenarioService(pcl.scenario).get_surface_runoff()

    pcl_types = [
        "water"
        if pcl.scenario.get_parcel(name=pn).get_compartment("Surface_water")
        else "N/A"
        for pn in ro_array.keys()
    ]

    pa_dict = {pp.name: pp.area.magnitude for pp in pcl.scenario.parcels}
    rom = []
    pav = []
    pcl_names = []
    for p, ro_dict in ro_array.items():
        pav.append([pa_dict[p]])
        pcl_names.append(p)
        m_row = []
        for pp, ro in ro_dict.items():
            if pp == 'sink':
                continue
            m_row.append(ro)
        rom.append(m_row)
    pav = np.array(pav)
    rom = np.array(rom)
    # 2. Compute watershed area matrix
    wsa_matrix = compute_watershed_areas(rom, pav, pcl_types)
    # 3. get the watershed area specific to this surface water parcel
    return wsa_matrix.loc[pcl_names.index(pcl.name), 0]


def compute_watershed_areas(runoff_matrix, area_parcels, parcel_type):
    # v3 deducts area of lakes from watershed (technically the area of a lake catches rain and 
    # delivers it to the lake and this how MC computes it. but to be consistent with the builder 
    # formulas this version substracts lake areas from runoff area of lakes only)
    # function to compute watershed areas by markov chain estimation. Only works if lakes runoff 100% to themselves. 
    # Land parcel do not have watersheds and will tend to zero but lake parcel watersheds will be accurate.
    # runoff_matrix is a square nxn matrix that must not include sinks and must include lakes in both rows and columns. 
    # Lakes must runoff 100% to themselves.
    # n is a large number like 200 or 300 that will enable the markov chain to reach steady state. 
    # area_parcels is a single matrix with areas of all parcels in the same order as the rows/cols of the runoff_matrix

    # New in v3: parcel_type is a list of parcel type with the same indexing as the other matrices. 
    # Note: the transpose is required because of the arrangment of the matrix such that row are senders 
    # and cols are receivers. When multiplying by area matrix to estimate watershed, the rows must be receivers, so transpose.

    M = np.matrix(runoff_matrix)# convert to np matrix
    M = np.nan_to_num(M)
    M_n = np.linalg.matrix_power(M, 1000) # raise M to a large number (markov chain estimation of probabilities of endpoint of flow)
    M_n_T = M_n.T # transpose of M_n so that it can be multiplied as a dot product with area parcels
    
    try:
        indexlist=area_parcels.index
    except:
        indexlist=[] # if already a matrix then 
    area_parcels = np.matrix(area_parcels)# convert to np matrix

    runoff_areas = M_n_T @ area_parcels
    try:
        runoff_areas=pd.DataFrame(runoff_areas,index=indexlist)
    except:
        runoff_areas=pd.DataFrame(runoff_areas)

    # new line to subtract parcel area from runoff area is parcel type is water
    runoff_areas.loc[pd.Series(parcel_type).str.contains('water', case=False), 0] -= np.array(area_parcels[pd.Series(parcel_type).str.contains('water', case=False)]).flatten()
    return (runoff_areas)


def calculate_avg_precipitation_runoff_fraction(all_soil_comps, fraction_name):
    # Example
    # get the fraction of precipitation that contributes to overland runoff 
    # summation (area of parcel * runoff_fraction of parcel) / (summation (area of parcels))
    numerator = 0
    denominator = 0
    for soil_comp in all_soil_comps:
        pcl_area = soil_comp.volume_element.parcel.area.magnitude
        pcl_runoff_fraction = getattr(soil_comp, fraction_name)
        numerator += (pcl_area * pcl_runoff_fraction)
        denominator += pcl_area
    try:
        return numerator / denominator
    except ZeroDivisionError:
        return 0


def get_correct_param(par_name, par_obj):
    if par_name in par_obj:
        return par_obj[par_name].value
    return None


def is_significantly_different(a, b):
    return abs(a - b) > 0.000_000_000_1


def get_water_params(pcl, parcel_type):
    runoff_watershed_area = 0  # 1e3
    runoff_fraction = None  # 0.001
    precip_seepage_frac_to_gw = None
    seepage_vol_rate_to_gw = 0  # 1
    sed_soil_erosion_to_sw = 0
    evapotranspiration_fraction = None

    precipitation_rate = pcl.scenario.Rain.magnitude
    if precipitation_rate is None:
        precipitation_rate = 0  # 0.0041

    # Even though this function's name is "get_water_parameters" many of the parameters directly below are related to
    # water on land parcels and not water parcels as they are related to watersheds that only exists on land.

    comp_surfaceSoil = pcl.get_compartment(media="Surface_Soil")
    if len(comp_surfaceSoil) > 0:
        comp_surfaceSoil = comp_surfaceSoil[0]
        runoff_watershed_area = (
            comp_surfaceSoil.area
            * comp_surfaceSoil.FractionofAreaAvailableforRunoff
        ).magnitude

        precip_seepage_frac_to_gw = comp_surfaceSoil.GroundwaterSeepageFraction  # 1 - runoff_fraction
        runoff_fraction = comp_surfaceSoil.PrecipitationRunoffFraction  # 1 - precip_seepage_frac_to_gw
        evapotranspiration_fraction = comp_surfaceSoil.EvapotranspirationFraction 

        try:
            seepage_vol_rate_to_gw = (
                precipitation_rate * 365
                * precip_seepage_frac_to_gw
                * runoff_watershed_area
            )
        except Exception as e:
            print('error calculating seepage_vol_rate_to_gw:', e)

    water_params = {
        'precip_rate': precipitation_rate,
        'precip_runoff_watershed_area': runoff_watershed_area,
        'precip_seepage_vol_rate_to_GW': seepage_vol_rate_to_gw,
        'sed_soil_erosion_to_SW': sed_soil_erosion_to_sw,
        'runoff_fraction': runoff_fraction,
        'seepage_frac': precip_seepage_frac_to_gw,
        'evapotrans_frac': evapotranspiration_fraction
    }

    sw_params = None
    if 'Water' in parcel_type:
        sw = pcl.get_compartment(media="Surface_Water")[0]
        sw_pars = dict(sw.parameters)
        sed = pcl.get_compartment(media="Sediment")[0]
        sed_pars = dict(sed.parameters)

        # we need a new watershed area here as the watershed of a water parcel is located on surrounding land parcels.
        sw_total_watershed_area = 0
        total_runoff_vol_rate_to_this_sw = 0
        total_seepage_vol_rate_to_gw = 0

        # get watershed area for water parcel
        sw_total_watershed_area = get_watershed_area(pcl)

        all_soil_comps = []
        connected_soil_comps = []
        for soil_comp in pcl.scenario.get_compartment(media="Surface_Soil"):
            all_soil_comps.append(soil_comp)
            if soil_comp.connects_to(sw):
                connected_soil_comps.append(soil_comp)

        # weighted average of precipitation fractions
        avg_precip_runoff_frac = calculate_avg_precipitation_runoff_fraction(all_soil_comps, 'PrecipitationRunoffFraction')
        avg_precip_seepage_frac = calculate_avg_precipitation_runoff_fraction(all_soil_comps, 'GroundwaterSeepageFraction')
        
        # sum up watershed area of connected Soil parcels.
        for this_soil_comp in connected_soil_comps:
            # this_watershed_area = (
            #         this_soil_comp.area
            #         * this_soil_comp.FractionofAreaAvailableforRunoff
            # ).magnitude
            # sw_total_watershed_area += this_watershed_area
            # we need to calculate runoff to this surface_water body using the watershed area above
            # comp_link = this_soil_comp.get_links(sw)
            # if len(comp_link) > 0:
            #     tps = comp_link[0].transport_processes(chemical=ch)
            #     runoff_tps = [t for t in tps if t.name.startswith("Runoff from Surface Soil to Surface Water")]
            #     if len(runoff_tps) > 0:
            #         runoff_tps = runoff_tps[0]
            #         precip_runoff = runoff_tps.eval(sender=this_soil_comp, receiver=sw, chemical=ch)
            #         this_precip_runoff_frac_to_sw = (precip_runoff / precipitation_rate).magnitude
            #     else:
            #         # This handles exception for Run-off when there is no link between compartments.
            #         print(f"No runoff transport from {this_soil_comp.standard_name} to {sw.standard_name}. "
            #               f"They are not next to each other. Check Runoff Matrix!")
            #         this_precip_runoff_frac_to_sw = 0

            erosion_rate = this_soil_comp.TotalErosionRate.magnitude if this_soil_comp.TotalErosionRate else 0
            sed_soil_erosion_to_sw += (
                erosion_rate
                * this_soil_comp.FractionOfTotalRunoff(sw) # surface runoff matrix
                * this_soil_comp.volume_element.parcel.area.magnitude
            )

        total_runoff_vol_rate_to_this_sw = (
                precipitation_rate * 365
                * avg_precip_runoff_frac
                * sw_total_watershed_area
        )
        total_seepage_vol_rate_to_gw = (
                precipitation_rate * 365
                * avg_precip_seepage_frac
                * sw_total_watershed_area
        )

        precipitation_vol_rate_to_sw = 0  # 4.8E6
        wc_external_inflow = get_correct_param("ExternalWaterInflow", sw_pars) or 0
        wc_flush_rate = get_correct_param("Flushes", sw_pars)

        fr_param = sw.parameters.get("Flushes")
        wc_flush_rate_is_autocalc = 'True'
        if isinstance(fr_param, CustomParameter) and fr_param.formula:
            wc_flush_rate_is_autocalc = 'True' if fr_param.formula.equation == 'True' else 'False'

        try:
            precipitation_vol_rate_to_sw = (
                    precipitation_rate * 365
                    * pcl.area).magnitude
        except Exception as ex:
            print(f'Problem Calculating Precipitation Volumetric Rate to Surface Water:\n {ex}')

        try:
            evaporation_vol_rate = get_correct_param("waterEvaporationRate", sw_pars) * pcl.area.magnitude
        except Exception as ex:
            evaporation_vol_rate = None
            print(f'Problem Calculating Water Column Evaporation Volumetric Rate:\n {ex}')
        # evaporation_vol_rate = 3.3E6

        try:
            wc_discharge_vol_rate = float('{:.5f}'.format(
                total_runoff_vol_rate_to_this_sw
                + total_seepage_vol_rate_to_gw
                + wc_external_inflow
                + precipitation_vol_rate_to_sw
                 - evaporation_vol_rate
            ))

            if wc_flush_rate_is_autocalc == 'False':
                wc_discharge_vol_rate = float('{:.5f}'.format(
                    wc_flush_rate * abs(sw.MeanDepth.magnitude) * pcl.area.magnitude
                ))
        except Exception as ex:
            wc_discharge_vol_rate = None
            print(f'Problem Calculating Water Column Discharge Volumetric Rate:\n {ex}')

        # wc_discharge_vol_rate = 6.2E6
        
        try:
            wc_sed_discharge_rate = (
                get_correct_param("SuspendedSedimentConcentration", sw_pars)
                * (wc_discharge_vol_rate)
            )
        except Exception as ex:
            wc_sed_discharge_rate = None
            print(f'Problem Calculating Sediment Discharge Rate:\n {ex}')
        # wc_sed_discharge_rate = 3.13E5

        try:
            sed_burial_vol_rate = ( # need to convert all to /day
                get_correct_param("ExternalSedimentInflow", sw_pars)
                + sed_soil_erosion_to_sw
                - (wc_sed_discharge_rate / 365)
            ) / (get_correct_param("BedDensity", sed_pars) * pcl.area.magnitude)

            sed_burial_vol_rate = max(sed_burial_vol_rate, 0)

            burial_par = sed_pars.get("SedimentBurialRateToHaveZeroNetDeposition")
            if isinstance(burial_par, ParameterDefinition):
                ParameterService.create(definition=burial_par, scenario=pcl.scenario,
                                        requirements=f"(self.id == {sed.id})", value=sed_burial_vol_rate,
                                        unit=burial_par.default_unit)
                ParameterService.commit()
            elif isinstance(burial_par, CustomParameter):
                if is_significantly_different(burial_par.value, sed_burial_vol_rate):
                    burial_par.value = sed_burial_vol_rate
                    ParameterService.commit()
        except Exception as ex:
            sed_burial_vol_rate = None
            print(f'Problem Calculating Sediment Burial Rate:\n {ex}')
        # sed_burial_vol_rate = get_correct_param("SedimentBurialRateToHaveZeroNetDeposition", sed_pars)  # 2.4992e-5

        try:
            sed_deposition_vol_rate = (
                get_correct_param("SedimentDepositionVelocity", sw_pars)
                * get_correct_param("SuspendedSedimentConcentration", sw_pars)
            ) / get_correct_param("BedDensity", sed_pars)
        except Exception as ex:
            sed_deposition_vol_rate = None
            print(f'Problem Calculating Sediment Deposition Volumetric Rate:\n {ex}')
        # sed_deposition_vol_rate = get_correct_param("SedimentDepositionRate", sw_pars)  # 3.8462e-5

        try:
            sed_resuspension_vel = (
                sed_deposition_vol_rate
                - sed_burial_vol_rate
            ) / (1 - get_correct_param("Porosity", sed_pars))
            resus_par = sed_pars.get("SedimentResuspensionVelocity")
            if isinstance(resus_par, ParameterDefinition):
                ParameterService.create(definition=resus_par, scenario=pcl.scenario,
                                        requirements=f"(self.id == {sed.id})", value=sed_resuspension_vel,
                                        unit=resus_par.default_unit)
                ParameterService.commit()
            elif isinstance(resus_par, CustomParameter):
                if is_significantly_different(resus_par.value, sed_resuspension_vel):
                    resus_par.value = sed_resuspension_vel
                    ParameterService.commit()
        except Exception as ex:
            sed_resuspension_vel = None
            print(f'Problem Calculating Sediment Resuspension Velocity:\n {ex}')
        # sed_resuspension_vel = get_correct_param("SedimentResuspensionVelocity", sed_pars)  # 6.2480e-5

        sw_params = {
            'autocalc': {
                'flush_rate': wc_flush_rate_is_autocalc
            },
            'wc_props':  {
                'flush_rate': wc_flush_rate,
                'suspended_sed_conc': get_correct_param("SuspendedSedimentConcentration", sw_pars),
                'algae_density': get_correct_param("AlgaeDensityInWaterColumn", sw_pars),
                'chloride_conc': get_correct_param("ChlorideConcentration", sw_pars),
                'chlorophyll_conc': get_correct_param("ChlorophyllConcentration", sw_pars),
                'mean_depth': abs(sw.MeanDepth.magnitude),
                'evaporation_rate': get_correct_param("waterEvaporationRate", sw_pars),
                'evaporation_vol_rate': evaporation_vol_rate,
                'suspended_organic_carbon': get_correct_param("OrganicCarbonContent", sw_pars),
                'water_ph': get_correct_param("pH", sw_pars),
                'sed_deposition_vel': get_correct_param("SedimentDepositionVelocity", sw_pars),
                'water_temp': get_correct_param("WaterTemperature", sw_pars),
                'externalWaterInflow': wc_external_inflow,
                'sed_inflow': get_correct_param("ExternalSedimentInflow", sw_pars),
                'discharge_vol_rate': wc_discharge_vol_rate,
                'sed_discharge_rate': wc_sed_discharge_rate,
                'connected_watershed_area': sw_total_watershed_area,
                'connected_runoff_to_this_sw': total_runoff_vol_rate_to_this_sw,
                'connected_seepage_to_gw': total_seepage_vol_rate_to_gw,
                'precip_vol_rate_to_SW': precipitation_vol_rate_to_sw,
            },
            'sed_props': {
                'bed_density': get_correct_param("BedDensity", sed_pars), 
                'organic_carbon_frac': get_correct_param("OrganicCarbonContent", sed_pars),
                'bed_pH': get_correct_param("pH", sed_pars),
                'bed_porosity': get_correct_param("Porosity", sed_pars),
                'bed_thickness': round(sed.volume_element.top - sed.volume_element.bottom, 4),
                'sed_burial_vol_rate': sed_burial_vol_rate,
                'sed_deposition_vol_rate': sed_deposition_vol_rate,
                'sed_resuspension_vel': sed_resuspension_vel,
                'sed_soil_erosion_to_sw': sed_soil_erosion_to_sw
            }
        }
    water_params['surface_water'] = sw_params
    return water_params


def get_initial_concentrations(pcl):
    chem_objs = {c for c in pcl.scenario.chemicals}
    chems = {c.name: {} for c in pcl.scenario.chemicals}
    initial_conc = {"initialConcentrations": chems}
    for chem in chem_objs:
        for comp in pcl.compartments:
            unit = "g / m^3" if comp.media.id in [2, 5, 7, 56, 55, 8, 9] else "g / kg" if comp.media.id in [23, 24, 27, 28, 29, 31, 32, 33, 37, 39, 41, 43, 44, 45, 46, 47, 48, 49, 50, 51] else "g / L" if comp.media.id in [10, 4] else ""
            spd = initial_conc["initialConcentrations"][chem.name].get(comp.volume_element.name)
            # Ultimately we need to use initialConcentrationConverted but we need to solve the unit incomaptibility issue.
            if spd:
                spd.setdefault(comp.name, {'ic': comp.initialConcentration(chem).magnitude, 'unit': unit})
            else:
                initial_conc["initialConcentrations"][chem.name].setdefault(comp.volume_element.name, {
                    comp.name: {'ic': comp.initialConcentration(chem).magnitude, 'unit': unit}})
    return initial_conc


def get_source_params(pcl):
    source_params = {}
    for chem in pcl.scenario.chemicals:
        chem_name = chem.name
        if chem_name not in source_params:
            source_params[chem_name] = {}
        for ve in pcl.volume_elements:
            ve_name = ve.name
            if ve_name not in source_params[chem_name]:
                source_params[chem_name][ve_name] = {}
            for comp in ve.compartments:
                deposition_rate = comp.surfaceDepositionRate(chemical=chem)  # slow ...
                try:
                    deposition_rate = deposition_rate.magnitude
                except Exception:
                    pass
                source_params[chem_name][ve_name][comp.name] = deposition_rate
    return {'sources': source_params}


def get_fish_params(comp):
    diet_by_media = {
        f'FractionDiet{x}': safe_get_val(comp, f'FractionDiet{x}', AQUATIC_DIET[comp.name][f'FractionDiet{x}'])
        for x in AQUATIC_BIOTA
    }
    biomass_by_media = safe_get_val(comp, 'BiomassPerArea', None)
    bw_by_media = safe_get_val(comp, 'BW', None)

    fish_params = {
        'aquatic_diet_fractions': diet_by_media,
        'aquatic_biomass': biomass_by_media,
        'aquatic_bw': bw_by_media
    }

    return fish_params


LAND_USE_TYPES = [
    'Impervious',
    'Tilled Soil',
    'Untilled Soil',
    'Agriculture (General)',
    'Grasses/Herbs',
    'Deciduous Forest',
    'Coniferous Forest'
]

AQUATIC_BIOTA = [
    'Algae',
    'Macrophyte',
    'Zooplankton',
    'BenthicInvertebrate',
    'FishHerbivore',
    'FishBenthicOmnivore',
    'FishOmnivore',
    'FishBenthicCarnivore',
    'FishCarnivore'
]

AQUATIC_DIET = {
    "Benthic_Carnivore": {
        "FractionDietAlgae": 0,
        "FractionDietMacrophyte": 0,
        "FractionDietZooplankton": 0,
        "FractionDietBenthicInvertebrate": 0.5,
        "FractionDietFishHerbivore": 0,
        "FractionDietFishBenthicOmnivore": 0.5,
        "FractionDietFishOmnivore": 0,
        "FractionDietFishBenthicCarnivore": 0,
        "FractionDietFishCarnivore": 0
    },
    "Benthic_Invertebrate": {
        "FractionDietAlgae": 0,
        "FractionDietMacrophyte": 0,
        "FractionDietZooplankton": 0,
        "FractionDietBenthicInvertebrate": 0,
        "FractionDietFishHerbivore": 0,
        "FractionDietFishBenthicOmnivore": 0,
        "FractionDietFishOmnivore": 0,
        "FractionDietFishBenthicCarnivore": 0,
        "FractionDietFishCarnivore": 0
    },
    "Benthic_Omnivore": {
        "FractionDietAlgae": 0,
        "FractionDietMacrophyte": 0,
        "FractionDietZooplankton": 0,
        "FractionDietBenthicInvertebrate": 1,
        "FractionDietFishHerbivore": 0,
        "FractionDietFishBenthicOmnivore": 0,
        "FractionDietFishOmnivore": 0,
        "FractionDietFishBenthicCarnivore": 0,
        "FractionDietFishCarnivore": 0
    },
    "Macrophyte": {
        "FractionDietAlgae": 0,
        "FractionDietMacrophyte": 0,
        "FractionDietZooplankton": 0,
        "FractionDietBenthicInvertebrate": 0,
        "FractionDietFishHerbivore": 0,
        "FractionDietFishBenthicOmnivore": 0,
        "FractionDietFishOmnivore": 0,
        "FractionDietFishBenthicCarnivore": 0,
        "FractionDietFishCarnivore": 0
    },
    "Water_Column_Carnivore": {
        "FractionDietAlgae": 0,
        "FractionDietMacrophyte": 0,
        "FractionDietZooplankton": 0,
        "FractionDietBenthicInvertebrate": 0,
        "FractionDietFishHerbivore": 0,
        "FractionDietFishBenthicOmnivore": 0,
        "FractionDietFishOmnivore": 1,
        "FractionDietFishBenthicCarnivore": 0,
        "FractionDietFishCarnivore": 0
    },
    "Water_Column_Herbivore": {
        "FractionDietAlgae": 0,
        "FractionDietMacrophyte": 0,
        "FractionDietZooplankton": 1,
        "FractionDietBenthicInvertebrate": 0,
        "FractionDietFishHerbivore": 0,
        "FractionDietFishBenthicOmnivore": 0,
        "FractionDietFishOmnivore": 0,
        "FractionDietFishBenthicCarnivore": 0,
        "FractionDietFishCarnivore": 0
    },
    "Water_Column_Omnivore": {
        "FractionDietAlgae": 0,
        "FractionDietMacrophyte": 0,
        "FractionDietZooplankton": 0,
        "FractionDietBenthicInvertebrate": 0,
        "FractionDietFishHerbivore": 1,
        "FractionDietFishBenthicOmnivore": 0,
        "FractionDietFishOmnivore": 0,
        "FractionDietFishBenthicCarnivore": 0,
        "FractionDietFishCarnivore": 0
    },
    "Zooplankton": {
        "FractionDietAlgae": 1,
        "FractionDietMacrophyte": 0,
        "FractionDietZooplankton": 0,
        "FractionDietBenthicInvertebrate": 0,
        "FractionDietFishHerbivore": 0,
        "FractionDietFishBenthicOmnivore": 0,
        "FractionDietFishOmnivore": 0,
        "FractionDietFishBenthicCarnivore": 0,
        "FractionDietFishCarnivore": 0
    }
}


Wet_Dry_Source_VolElem_defaults = {
    'DryParticleSource': {
        'name': 'DryParticleSource',
        'top': -3.65,
        'bottom': -11.65,
        'Compartments': {
            'DryParticleSource': {
                'name': 'DryParticleSource',
                'media_name': 'Dry_Particle'
            }
        }
    },
    'DryVaporSource': {
        'name': 'DryVaporSource',
        'top': -11.65,
        'bottom': -19.65,
        'Compartments': {
            'DryVaporSource': {
                'name': 'DryVaporSource',
                'media_name': 'Dry_Vapor'
            }
        }
    },
    'WetParticleSource': {
        'name': 'WetParticleSource',
        'top': -19.65,
        'bottom': -27.65,
        'Compartments': {
            'WetParticleSource': {
                'name': 'WetParticleSource',
                'media_name': 'Wet_Particle'
            }
        }
    },
    'WetVaporSource': {
        'name': 'WetVaporSource',
        'top': -27.65,
        'bottom': -35.65,
        'Compartments': {
            'WetVaporSource': {
                'name': 'WetVaporSource',
                'media_name': 'Wet_Vapor'
            }
        }
    }
}

Air_Parcel_VolElem_defaults = {
    'Air': {
        'name': 'Air',
        'top': 226,
        'bottom': 0,
        'Compartments': {
            'Air': {
                'name': 'Air',
                'media_name': 'Air'
            },
            'Degradation_Reaction_Sink_Air': {
                'name': 'Degradation_Reaction_Sink',
                'media_name': 'Degradation_Reaction'
            }
        }
    },
    'UpperAir': {
        'name': 'UpperAir',
        'top': 10000,
        'bottom': 226,
        'Compartments': {
            'UpperAir': {
                'name': 'Air',
                'media_name': 'Air'
            }
        }
    }
}

Land_Parcel_VolElem_defaults = {
    'SurfSoil': {
        'name': 'SurfSoil',
        'top': 0,
        'bottom': -0.01,
        'layers': ["Soil_Root_Zone", "Soil_Vadose_Zone", "Groundwater", "DryVaporSource", "WetVaporSource", "DryParticleSource", "WetParticleSource"],
        'Compartments': {
            'Soil_Surface': {
                'name': 'Soil_Surface',
                'media_name': 'Surface_Soil'
            },
            'Degradation_Reaction_Sink_SurfSoil': {
                'name': 'Degradation_Reaction_Sink',
                'media_name': 'Degradation_Reaction'
            },
            'Soil_Advection_Sink': {
                'name': 'Soil_Advection_Sink',
                'media_name': 'Advection'
            },
            'Leaf_Grasses_Herbs': {
                'name': 'Leaf_Grasses_Herbs',
                'media_name': 'Grass_Leaf'
            },
            'Leaf_Particle_Grasses_Herbs': {
                'name': 'Leaf_Particle_Grasses_Herbs',
                'media_name': 'Grass_Leaf_Particle'
            },
            'Stem_Grasses_Herbs': {
                'name': 'Stem_Grasses_Herbs',
                'media_name': 'Grass_Stem'
            },
            'Root_Grasses_Herbs': {
                'name': 'Root_Grasses_Herbs',
                'media_name': 'Grass_Root'
            }
        }
    },
    'RootSoil': {
        'name': 'RootSoil',
        'top': -0.01,
        'bottom': -0.8,
        'layers': ["Soil_Vadose_Zone", "Groundwater", "DryVaporSource", "WetVaporSource", "DryParticleSource", "WetParticleSource"],
        'Compartments': {
            'Soil_Root_Zone': {
                'name': 'Soil_Root_Zone',
                'media_name': 'Root_Zone'
            },
            'Degradation_Reaction_Sink_RootSoil': {
                'name': 'Degradation_Reaction_Sink',
                'media_name': 'Degradation_Reaction'
            }
        }
    },
    'VadoseSoil': {
        'name': 'VadoseSoil',
        'top': -0.8,
        'bottom': -2.2,
        'layers': ["Groundwater", "DryVaporSource", "WetVaporSource", "DryParticleSource", "WetParticleSource"],
        'Compartments': {
            'Soil_Vadose_Zone': {
                'name': 'Soil_Vadose_Zone',
                'media_name': 'Vadose_Zone'
            },
            'Degradation_Reaction_Sink_VadoseSoil': {
                'name': 'Degradation_Reaction_Sink',
                'media_name': 'Degradation_Reaction'
            }
        }
    },
    'GW': {
        'name': 'GW',
        'top': -2.2,
        'bottom': -5.2,
        'layers': ["DryVaporSource", "WetVaporSource", "DryParticleSource", "WetParticleSource"],
        'Compartments': {
            'Groundwater': {
                'name': 'Groundwater',
                'media_name': 'Groundwater'
            },
            'Degradation_Reaction_Sink_GW': {
                'name': 'Degradation_Reaction_Sink',
                'media_name': 'Degradation_Reaction'
            }
        }
    }
}

# these defaults are set when land use == tilled or untilled
Farm_Biota_SurfSoil_Compartment_defaults = {
    'Compartments': {
        'Soil_Surface': {
            'name': 'Soil_Surface',
            'media_name': 'Surface_Soil'
        },
        'Degradation_Reaction_Sink_SurfSoil': {
            'name': 'Degradation_Reaction_Sink',
            'media_name': 'Degradation_Reaction'
        },
        'Soil_Advection_Sink': {
            'name': 'Soil_Advection_Sink',
            'media_name': 'Advection'
        }
    }
}

Water_Parcel_VolElem_defaults = {
    'SW': {
        'name': 'SW',
        'top': 0,
        'bottom': -3.6,
        'Compartments': {
            'Surface_water': {
                'name': 'Surface_water',
                'media_name': 'Surface_Water'
            },
            'Degradation_Reaction_Sink': {
                'name': 'Degradation_Reaction_Sink',
                'media_name': 'Degradation_Reaction'
            },
            'Flush_Rate_Sink': {
                'name': 'Flush_Rate_Sink',
                'media_name': 'Flush_Rate'
            }
        }
    },
    'Sed': {
        'name': 'Sed',
        'top': -3.6,
        'bottom': -3.65,
        'Compartments': {
            'Sediment': {
                'name': 'Sediment',
                'media_name': 'Sediment'
            },
            'Degradation_Reaction_Sink': {
                'name': 'Degradation_Reaction_Sink',
                'media_name': 'Degradation_Reaction'
            },
            'Burial_Sink': {
                'name': 'Burial_Sink',
                'media_name': 'Burial'
            }
        }
    }
}

Aquatic_Biota_Sed_Compartment_defaults = {
    'Compartments': {
        'Benthic_Carnivore': {
            'name': 'Benthic_Carnivore',
            'media_name': 'Benthic_Carnivore'
        },
        'Benthic_Invertebrate': {
            'name': 'Benthic_Invertebrate',
            'media_name': 'Benthic_Invertebrate'
        },
        'Benthic_Omnivore': {
            'name': 'Benthic_Omnivore',
            'media_name': 'Benthic_Omnivore'
        }
    }
}

Aquatic_Biota_SW_Compartment_defaults = {
    'Compartments': {
        'Macrophyte': {
            'name': 'Macrophyte',
            'media_name': 'Macrophyte'
        },
        'Water_Column_Carnivore': {
            'name': 'Water_Column_Carnivore',
            'media_name': 'Water_Column_Carnivore'
        },
        'Water_Column_Herbivore': {
            'name': 'Water_Column_Herbivore',
            'media_name': 'Water_Column_Herbivore'
        },
        'Water_Column_Omnivore': {
            'name': 'Water_Column_Omnivore',
            'media_name': 'Water_Column_Omnivore'
        },
        'Zooplankton': {
            'name': 'Zooplankton',
            'media_name': 'Plankton'
        }
    }
}

# These are parameters specific to surface soil needed for new media that are child of surface soil. Replace domain_id
# with the id of the new domain specific to that new media.
SURFACE_SOIL_SPECIFIC_MEDIA_PARAMS = [
    {
        'variable_name': 'conc_Colloid',
        'full_name': 'conc_Colloid',
        'domain_id': None,
        'default_value': 0.01,
        'default_unit': 'kg/m^3',
        'default_formula_id': None
    },
    {
        'variable_name': 'Depth',
        'full_name': 'Depth',
        'domain_id': None,
        'default_value': None,
        'default_unit': 'm',
        'default_formula_id': 165
    },
    {
        'variable_name': 'Height',
          'full_name': 'Height',
          'domain_id': None,
          'default_value': None,
          'default_unit': 'm',
          'default_formula_id': 166
    },
    {
        'variable_name': 'isBiotic',
        'full_name': 'isBiotic',
        'domain_id': None,
        'default_value': 0.0,
        'default_unit': None,
        'default_formula_id': None
    },
    {
        'variable_name': 'rho_Colloid',
        'full_name': 'rho_Colloid',
        'domain_id': None,
        'default_value': 2650.0,
        'default_unit': 'kg/m^3',
        'default_formula_id': None
    },
    {
        'variable_name': 'TotalMass',
        'full_name': 'TotalMass',
        'domain_id': None,
        'default_value': None,
        'default_unit': 'kg',
        'default_formula_id': 167
    },
    {
        'variable_name': 'Volume',
        'full_name': 'Volume',
        'domain_id': None,
        'default_value': None,
        'default_unit': 'm^3',
        'default_formula_id': 168
    },
    {
        'variable_name': 'VolumeFraction_Colloid',
        'full_name': 'VolumeFraction_Colloid',
        'domain_id': None,
        'default_value': None,
        'default_unit': 'm^3[colloid]/m^3[compartment]',
        'default_formula_id': 169
    },
    {
        'variable_name': 'VolumeFraction_LiquidColloid',
        'full_name': 'VolumeFraction_LiquidColloid',
        'domain_id': None,
        'default_value': 0.22,
        'default_unit': '',
        'default_formula_id': None
    },
    {
        'variable_name': 'wetConcOutputUnits',
        'full_name': 'wetConcOutputUnits',
        'domain_id': None,
        'default_value': None,
        'default_unit': None,
        'default_formula_id': 170
    },
    {
        'variable_name': 'FractionOfTotalErosion',
        'full_name': 'FractionOfTotalErosion',
        'domain_id': None,
        'default_value': None,
        'default_unit': None,
        'default_formula_id': 2484
    },
    {
        'variable_name': 'FractionOfTotalRunoff',
        'full_name': 'FractionOfTotalRunoff',
        'domain_id': None,
        'default_value': None,
        'default_unit': None,
        'default_formula_id': 2485
    },
    {
        'variable_name': 'sedimentDeliveryRatioSlopeCoef',
        'full_name': 'sedimentDeliveryRatioSlopeCoef',
        'domain_id': None,
        'default_value': 0.125,
        'default_unit': None,
        'default_formula_id': None
    }
]

EROSION_TABLE_PARAM_MAP = {
    'rainfall_erosivity_index': 'R',
    'erodibility_index': 'K',
    'slope_gradient': 'S',
    'slope_length': 'L',
    'topographical_length-slope_factor': 'LS',
    'cover_management_factor': 'C',
    'supporting_practices_factor': 'P',
    'unit_soil_loss': 'A',
    'empirical_intercept_coefficient': 'a',
    'empirical_slope_coefficient': 'b',
    'sediment_delivery_ratio': 'SD',
    'total_effective_erosion_rate': 'Total Effective Erosion Rate'
}

EROSION_DEFAULTS = {
    'R': 300 * ureg('((100 * ft * US_ton) / acre) / year'),
    'K': 0.36 * ureg('(ton / acre) / ((100 * ft * US_ton) / acre)'),
    'LS': 1.5,
    'P': 1
}