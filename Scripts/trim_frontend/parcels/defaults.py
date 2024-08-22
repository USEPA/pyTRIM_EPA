from trim_db.schema import Parcel
from trim_db.schema.utils.serialize import register_serializer
from trim_db.schema.parameters.models import ParameterDefinition, CustomParameter
from trim_db.services import *
import pint
import json

comp_local_cache = {}

@register_serializer(Parcel)
def serialize_parcel(pcl: Parcel):
    init_comp_cache(pcl)
    
    general_params = get_general_params(pcl)
    water_params = get_water_params(pcl, general_params['parcelType'])
    source_params = get_source_params(pcl)
    soil_abiotic_params = get_soil_abiotic_params(pcl)

    s = {
        'id': pcl.id,
        'name': pcl.name,
        'description': pcl.description if pcl.description else "None",
        'vertices': pcl.vertices,
        'area': pcl.area.m_as('m^2'),
        'compartment_map': {ve.name: [c.name for c in ve.compartments] for ve in pcl.volume_elements},
        **general_params,
        **water_params,
        **source_params,
        **soil_abiotic_params
    }

    comp_local_cache.clear()
    return s


def safe_get_val(comp, k, default=None):
    param = comp.parameters.get(k)
    if param is None:
        return default
    v = param.value
    if v is None and isinstance(param, ParameterDefinition):
        return default
    return v


def get_soil_magnitude(comp, attr):
    par_val = comp.__getattr__(attr)
    if isinstance(par_val, pint.Quantity):
        return par_val.magnitude
    return par_val


def init_comp_cache(pcl):
    # calling .compartments and .get_compartment a lot is slow
    comp_local_cache["all"] = pcl.compartments
    for c in comp_local_cache["all"]:
        kwargs = {"name": c.name}
        uuid = f"{pcl.id}_{str(kwargs.keys())}_{str(kwargs.values())}"
        if uuid in comp_local_cache:
            comp_local_cache[uuid].append(c)
        else:
            comp_local_cache.setdefault(uuid, [c])


def get_comp(pcl, kwargs):
    uuid = f"{pcl.id}_{str(kwargs.keys())}_{str(kwargs.values())}"
    comp = comp_local_cache.get(uuid)
    if not comp:
        comp = pcl.get_compartment(**kwargs)
        comp_local_cache[uuid] = comp
    
    if kwargs.get("name") and isinstance(comp, list):
        comp = comp[0]

    return comp


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
    total_erosion_rate = None
    is_tilled = False

    erosion_table_params = {}
    default_erosion = ParameterService.definitions.get_all(variable_name="erosion_table")
    for default_param in default_erosion:
        custom_param = ParameterService.get(
            scenario_id=pcl.scenario_id,
            requirements=f"(self.id == {pcl.id})",
            definition_id=default_param.id,
        )
        if custom_param and custom_param.unit:
            erosion_table_params[default_param.full_name] =  custom_param.unit

    surface_soil_height = None
    root_soil_height = get_comp(pcl, {"name":"Soil_Root_Zone"})
    vadose_soil_height = get_comp(pcl, {"name":"Soil_Vadose_Zone"})
    groundwater_height = get_comp(pcl, {"name":"Groundwater"})

    diet_by_media = {}
    biomass_by_media = {}
    bw_by_media = {}

    land_use = 'Impervious'

    # FIXME verify this is okay
    if root_soil_height:
        root_soil_height = root_soil_height.volume_element.height.m_as('m')
    if vadose_soil_height:
        vadose_soil_height = vadose_soil_height.volume_element.height.m_as('m')
    if groundwater_height:
        groundwater_height = groundwater_height.volume_element.height.m_as('m')

    for comp in comp_local_cache["all"]:
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
        elif comp.media.isa('Surface_Soil', or_child=False):
            land = True
            if surface_soil_height is None:
                surface_soil_height = comp.volume_element.height.m_as('m')
                total_erosion_rate = safe_get_val(comp, 'TotalErosionRate', None)
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
            land_use = 'Agriculture - General'
        elif comp.media.isa('Grass'):
            land_use = 'Grasses/Herbs'
        elif comp.media.isa('Tilled_Soil'):
            land = True
            if surface_soil_height is None:
                surface_soil_height = comp.volume_element.height.m_as('m')
                total_erosion_rate = safe_get_val(comp, 'TotalErosionRate', None)
                is_tilled = True
            land_use = 'Tilled Soil'
        elif comp.media.isa('Untilled_Soil'):
            land = True
            if surface_soil_height is None:
                surface_soil_height = comp.volume_element.height.m_as('m')
                total_erosion_rate = safe_get_val(comp, 'TotalErosionRate', None)
                is_tilled = False
            land_use = 'Untilled Soil'

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


def get_parcel_comp_params(pcl, comps, params):
    cmps = [comp for comp in pcl.compartments if comp.name in [c for c in comps]]
    pars = {c.name: {pn: p for pn, p in c.parameters.items()} for c in cmps}
    return {cn: {pn: pars[cn][pn].value if isinstance(pars[cn][pn], CustomParameter) else pars[cn][pn].default_value
                 for pn in params} for cn in comps}


def get_soil_abiotic_params(pcl, run_old=True):
    comps = ["Soil_Surface", "Soil_Root_Zone", "Soil_Vadose_Zone", "Groundwater"]
    if not run_old:
         params = ["pH", "FractionSand", "OrganicCarbonContent", "rho", "Porosity", "VolumeFraction_Vapor",
                   "AverageVerticalVelocity", "VolumeFraction_Liquid", "AirSoilBoundaryThickness",
                   "FractionofAreaAvailableforErosion", "FractionofAreaAvailableforRunoff",
                   "FractionofAreaAvailableforVerticalDiffusion", "TotalRunoffRate"]
         new_soil_abiotic_params = get_parcel_comp_params(pcl, comps, params)
         return {"soil_params": new_soil_abiotic_params}

    has_surf_soil = True if get_comp(pcl, {"name":"Soil_Surface"}) else False
    has_root_soil = True if get_comp(pcl, {"name":"Soil_Root_Zone"}) else False
    has_vadose_soil = True if get_comp(pcl, {"name":"Soil_Vadose_Zone"}) else False
    has_groundwater = True if get_comp(pcl, {"name":"Groundwater"}) else False
    soil_abiotic_params = {}

    if has_surf_soil and has_root_soil and has_vadose_soil and has_groundwater:
        # get pH, fractionSand, organicCarbonContent, density
        for c in comps:
            this_comp = get_comp(pcl, {"name":c})
            params = {"pH": "", "FractionSand": "", "OrganicCarbonContent": "", "rho": ""}
            for k, _ in params.items():
                params[k] = get_soil_magnitude(this_comp, k)
            soil_abiotic_params[c] = params

    if has_groundwater:
        # get porosity
        param = soil_abiotic_params.get("Groundwater")
        if param:
            param["Porosity"] = get_comp(pcl, {"name":"Groundwater"}).Porosity
        else:
            param.setdefault("Groundwater", {"Porosity": get_comp(pcl, {"name":"Groundwater"}).Porosity})
        soil_abiotic_params["Groundwater"] = param

    comps.pop(comps.index("Groundwater"))
    if has_root_soil and has_vadose_soil and has_surf_soil:
        # get VolumeFraction_vapor, AverageVerticalVelocity, VolumeFraction_liquid
        for c in comps:
            this_comp = get_comp(pcl, {"name":c})
            params = {"VolumeFraction_Vapor": "", "AverageVerticalVelocity": "", "VolumeFraction_Liquid": "", "rho": ""}
            if soil_abiotic_params.get(c):
                for k, _ in params.items():
                    soil_abiotic_params[c].setdefault(k, get_soil_magnitude(this_comp, k))
            else:
                for k, _ in params.items():
                    params[k] = get_soil_magnitude(this_comp, k)
                soil_abiotic_params[c] = params

    if has_surf_soil:
        params = {"AirSoilBoundaryThickness": "", "FractionofAreaAvailableforErosion": "",
                  "FractionofAreaAvailableforRunoff": "", "FractionofAreaAvailableforVerticalDiffusion": "",
                  "TotalRunoffRate": ""}
        comp = "Soil_Surface"
        this_comp = get_comp(pcl, {"name":comp})
        if soil_abiotic_params.get(comp):
            for k, _ in params.items():
                soil_abiotic_params[comp].setdefault(k, get_soil_magnitude(this_comp, k))
        else:
            for k, _ in params.items():
                params[k] = get_soil_magnitude(this_comp, k)
            soil_abiotic_params[comp] = params

    return {"soil_params": soil_abiotic_params}


def get_water_params(pcl, parcel_type):
    precipitation_rate = pcl.scenario.Rain.magnitude
    if precipitation_rate is None:
        precipitation_rate = 0  # 0.0041

    comp_surfaceSoil = get_comp(pcl, {"media": "Surface_Soil"})

    # TODO This is not right. We need params for all chemicals. How to show this in frontend???
    ch = ChemicalService.get(id=32)
    ch.current_scenario(pcl.scenario)

    runoff_watershed_area = 0  # 1e3
    runoff_fraction = 0  # 0.001
    precip_seepage_frac_to_gw = None
    seepage_vol_rate_to_gw = 0  # 1
    sed_soil_erosion_to_sw = 0

    # Even though this function's name is "get_water_parameters" many of the parameters directly below are related to
    # water on land parcels and not water parcels as they are related to watersheds that only exists on land.

    if len(comp_surfaceSoil) > 0:
        comp_surfaceSoil = comp_surfaceSoil[0]

        runoff_watershed_area = (
            comp_surfaceSoil.area
            * comp_surfaceSoil.FractionofAreaAvailableforRunoff
        ).magnitude

        precip_seepage_frac_to_gw = comp_surfaceSoil.GroundwaterSeepageFraction  # 1 - runoff_fraction

        runoff_fraction = 1 - precip_seepage_frac_to_gw

        try:
            seepage_vol_rate_to_gw = (
                precipitation_rate
                * precip_seepage_frac_to_gw
                * runoff_watershed_area
            )
        except Exception as e:
            print(e)


    water_params = {
        'precip_rate': precipitation_rate,
        'precip_runoff_watershed_area': runoff_watershed_area,
        'precip_seepage_vol_rate_to_GW': seepage_vol_rate_to_gw,
        'sed_soil_erosion_to_SW': sed_soil_erosion_to_sw,
        'runoff_fraction': runoff_fraction,
        'seepage_frac': precip_seepage_frac_to_gw
    }

    sw_params = None
    if 'Water' in parcel_type:
        sw = get_comp(pcl, {"media": "Surface_Water"})[0]
        sw_pars = {parn: par for parn, par in sw.parameters.items()}
        sed = get_comp(pcl, {"media": "Sediment"})[0]
        sed_pars = {parn: par for parn, par in sed.parameters.items()}

        # we need a new watershed area here as the watershed of a water parcel is located on surrounding land parcels.
        sw_total_watershed_area = 0
        total_runoff_vol_rate_to_this_sw = 0
        total_seepage_vol_rate_to_gw = 0

        connected_soil_comps = []
        for this_parcel in pcl.scenario.parcels:
            soil_comp = this_parcel.get_compartment("Soil_Surface")
            if soil_comp and soil_comp.connects_to(sw):
                connected_soil_comps.append(soil_comp)
        # sum up watershed area of connected Soil parcels.
        for this_soil_comp in connected_soil_comps:
            this_watershed_area = (
                    this_soil_comp.area
                    * this_soil_comp.FractionofAreaAvailableforRunoff
            ).magnitude
            sw_total_watershed_area += this_watershed_area
            # we need to calculate runoff to this surface_water body using the watershed area above
            comp_link = this_soil_comp.get_links(sw)
            if len(comp_link) > 0:
                tps = comp_link[0].transport_processes(chemical=ch)
                runoff_tps = [t for t in tps if t.name.startswith("Runoff from Surface Soil to Surface Water")]
                if len(runoff_tps) > 0:
                    runoff_tps = runoff_tps[0]
                    precip_runoff = runoff_tps.eval(sender=this_soil_comp, receiver=sw, chemical=ch)
                    this_precip_runoff_frac_to_sw = (precip_runoff / precipitation_rate).magnitude
                else:
                    # This handles exception for Run-off when there is no link between compartments.
                    print(f"No runoff transport from {this_soil_comp.standard_name} to {sw.standard_name}. "
                          f"They are not next to each other. Check Runoff Matrix!")
                    this_precip_runoff_frac_to_sw = 0
            total_runoff_vol_rate_to_this_sw += (
                    precipitation_rate
                    * this_precip_runoff_frac_to_sw
                    * this_watershed_area
            )
            total_runoff_vol_rate_to_this_sw = 0 if total_runoff_vol_rate_to_this_sw else total_runoff_vol_rate_to_this_sw
            this_seepage_frac_to_gw = this_soil_comp.GroundwaterSeepageFraction
            total_seepage_vol_rate_to_gw += (
                    precipitation_rate
                    * this_seepage_frac_to_gw
                    * this_watershed_area
            )
            this_total_erosion_rate = this_soil_comp.TotalErosionRate.magnitude
            sed_soil_erosion_to_sw += (
                this_precip_runoff_frac_to_sw
                * this_total_erosion_rate
                * this_watershed_area
            )
        def get_correct_param(par_name, par_obj):
            par = par_obj.get(par_name)
            return par.value if isinstance(par, CustomParameter) else par.default_value if \
                isinstance(par, ParameterDefinition) else None

        wc_external_inflow = 0
        precipitation_vol_rate_to_sw = 0  # 4.8E6

        try:
            precipitation_vol_rate_to_sw = (
                    precipitation_rate
                    * pcl.area).magnitude
        except Exception as e:
            print(e)

        try:
            evaporation_vol_rate = get_correct_param("waterEvaporationRate", sw_pars) * pcl.area.magnitude
        except Exception:
            evaporation_vol_rate = None
        # evaporation_vol_rate = 3.3E6

        try:
            wc_discharge_vol_rate = float('{:.5f}'.format(
                total_runoff_vol_rate_to_this_sw
                + total_seepage_vol_rate_to_gw
                + wc_external_inflow
                + precipitation_vol_rate_to_sw
                - evaporation_vol_rate
            ))
            wc_discharge_vol_rate = 0 if wc_discharge_vol_rate else wc_discharge_vol_rate
        except Exception:
            wc_discharge_vol_rate = None
        # wc_discharge_vol_rate = 6.2E6
        
        try:
            wc_sed_discharge_rate = (
                get_correct_param("SuspendedSedimentConcentration", sw_pars)
                * wc_discharge_vol_rate
            )
        except Exception:
            wc_sed_discharge_rate = None
        # wc_sed_discharge_rate = 3.13E5

        try:
            sed_burial_vol_rate = (
                get_correct_param("ExternalSedimentInflow", sw_pars)
                + sed_soil_erosion_to_sw
                - wc_sed_discharge_rate
            ) / (get_correct_param("BedDensity", sed_pars) * pcl.area.magnitude)
        except Exception:
            sed_burial_vol_rate = None
        # sed_burial_vol_rate = get_correct_param("SedimentBurialRateToHaveZeroNetDeposition", sed_pars)  # 2.4992e-5

        try:
            sed_deposition_vol_rate = (
                get_correct_param("SedimentDepositionVelocity", sw_pars)
                * get_correct_param("SuspendedSedimentConcentration", sw_pars)
            ) / get_correct_param("BedDensity", sed_pars)
        except Exception:
            sed_deposition_vol_rate = None
        # sed_deposition_vol_rate = get_correct_param("SedimentDepositionRate", sw_pars)  # 3.8462e-5

        try:
            sed_resuspension_vel = (
                sed_deposition_vol_rate
                - sed_burial_vol_rate
            ) / (1 - get_correct_param("Porosity", sed_pars))
        except Exception:
            sed_resuspension_vel = None
        # sed_resuspension_vel = get_correct_param("SedimentResuspensionVelocity", sed_pars)  # 6.2480e-5

        sw_params = {
            'wc_props':  {
                'flush_rate': get_correct_param("Flushes", sw_pars),
                'suspended_sed_conc': get_correct_param("SuspendedSedimentConcentration", sw_pars),
                'algae_density': get_correct_param("AlgaeDensityInWaterColumn", sw_pars),
                'chloride_conc': get_correct_param("ChlorideConcentration", sw_pars),
                'chlorophyll_conc': get_correct_param("ChlorophyllConcentration", sw_pars),
                'mean_depth': sw.volume_element.top - sw.volume_element.bottom,
                'evaporation_rate': get_correct_param("waterEvaporationRate", sw_pars),
                'evaporation_vol_rate': evaporation_vol_rate,
                'suspended_organic_carbon': get_correct_param("OrganicCarbonContent", sw_pars),
                'water_ph': get_correct_param("pH", sw_pars),
                'sed_deposition_vel': get_correct_param("SedimentDepositionVelocity", sw_pars),
                'water_temp': get_correct_param("WaterTemperature", sw_pars),
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
                'bed_thickness': sed.volume_element.top - sed.volume_element.bottom,
                'sed_burial_vol_rate': sed_burial_vol_rate,
                'sed_deposition_vol_rate': sed_deposition_vol_rate,
                'sed_resuspension_vel': sed_resuspension_vel,
                'sed_soil_erosion_to_sw': sed_soil_erosion_to_sw
            }
        }
    water_params['surface_water'] = sw_params
    return water_params


def get_source_params(pcl):
    chem_objs = {c for c in pcl.scenario.chemicals}
    source_comps = [c for c in comp_local_cache["all"] if c.media.isa("Source")]
    chems = {c.name: {} for c in pcl.scenario.chemicals}
    source_params = {"sources": chems}
    for comp in source_comps:
        for chem in chem_objs:
            try:
                source_params["sources"][chem.name][comp.volume_element.name] = {comp.name: comp.surfaceDepositionRate(chemical=chem).magnitude}
            except AttributeError:
                source_params["sources"][chem.name][comp.volume_element.name] = {comp.name: comp.surfaceDepositionRate(chemical=chem)}
    return source_params


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
        "FractionDietFishBenthicOmnivore": 0.5,
        "FractionDietFishOmnivore": 0.5,
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
        'top': 800,
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
        'top': 1000,
        'bottom': 800,
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
        'variable_name': 'unitSoilLoss',
        'full_name': 'unitSoilLoss',
        'domain_id': None,
        'default_value': 0.00036,
        'default_unit': 'kg/m^2/day',
        'default_formula_id': None
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
