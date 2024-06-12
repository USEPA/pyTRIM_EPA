from trim_db.schema import Parcel
from trim_db.schema.utils.serialize import register_serializer
from trim_db.schema.parameters.models import ParameterDefinition, CustomParameter
from trim_db.services import *
import pint


@register_serializer(Parcel)
def serialize_parcel(pcl: Parcel):
    general_params = get_general_params(pcl)
    water_params = get_water_params(pcl, general_params['parcelType'])
    source_params = get_source_params(pcl)
    soil_abiotic_params = get_soil_abiotic_params(pcl)

    s = {
        'id': pcl.id,
        'name': pcl.name,
        'description': pcl.description,
        'vertices': pcl.vertices,
        'area': pcl.area.m_as('m^2'),
        'compartment_map': {ve.name: [c.name for c in ve.compartments] for ve in pcl.volume_elements},
        **general_params,
        **water_params,
        **source_params,
        **soil_abiotic_params

    }

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
    total_erosion_rate = None
    is_tilled = False

    surface_soil_height = None
    root_soil_height = None
    vadose_soil_height = None
    groundwater_height = None

    diet_by_media = {}
    biomass_by_media = {}
    bw_by_media = {}

    land_use = 'Impervious'
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
                    comp, 'FractionOrganicMatterOnParticulates', None
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
        elif comp.media.isa('Soil_Root_Zone'):
            if root_soil_height is None:
                root_soil_height = comp.volume_element.height.m_as('m')
        elif comp.media.isa('Soil_Vadose_Zone'):
            if vadose_soil_height is None:
                vadose_soil_height = comp.volume_element.height.m_as('m')
        elif comp.media.isa('Groundwater'):
            if groundwater_height is None:
                groundwater_height = comp.volume_element.height.m_as('m')
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
            land_use = 'Tilled Soil'
        elif comp.media.isa('Untilled_Soil'):
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
        'soilTillage': is_tilled,

        'aquatic_diet_fractions': diet_by_media,
        'aquatic_biomass': biomass_by_media,
        'aquatic_bw': bw_by_media
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

    has_surf_soil = True if pcl.get_compartment(name="Soil_Surface") else False
    has_root_soil = True if pcl.get_compartment(name="Soil_Root_Zone") else False
    has_vadose_soil = True if pcl.get_compartment(name="Soil_Vadose_Zone") else False
    has_groundwater = True if pcl.get_compartment(name="Groundwater") else False
    soil_abiotic_params = {}

    if has_surf_soil and has_root_soil and has_vadose_soil and has_groundwater:
        # get pH, fractionSand, organicCarbonContent, density
        for c in comps:
            this_comp = pcl.get_compartment(name=c)
            params = {"pH": "", "FractionSand": "", "OrganicCarbonContent": "", "rho": ""}
            for k, _ in params.items():
                # par_val = safe_get_val(this_comp, k)
                par_val = this_comp.__getattr__(k)
                mag = par_val.magnitude if isinstance(
                    par_val, pint.Quantity) else par_val
                params[k] = mag
            soil_abiotic_params[c] = params

    if has_groundwater:
        # get porosity
        param = soil_abiotic_params.get("Groundwater")
        if param:
            param["Porosity"] = pcl.get_compartment("Groundwater").Porosity
        else:
            param.setdefault("Groundwater", {"Porosity": pcl.get_compartment("Groundwater").Porosity})
        soil_abiotic_params["Groundwater"] = param

    comps.pop(comps.index("Groundwater"))
    if has_root_soil and has_vadose_soil and has_surf_soil:
        # get VolumeFraction_vapor, AverageVerticalVelocity, VolumeFraction_liquid
        for c in comps:
            this_comp = pcl.get_compartment(name=c)
            params = {"VolumeFraction_Vapor": "", "AverageVerticalVelocity": "", "VolumeFraction_Liquid": "", "rho": ""}
            if soil_abiotic_params.get(c):
                for k, _ in params.items():
                    # par_val = safe_get_val(this_comp, k)
                    par_val = this_comp.__getattr__(k)
                    mag = par_val.magnitude if isinstance(
                        par_val, pint.Quantity) else par_val
                    soil_abiotic_params[c].setdefault(k, mag)
            else:
                for k, _ in params.items():
                    # par_val = safe_get_val(this_comp, k)
                    par_val = this_comp.__getattr__(k)
                    mag = par_val.magnitude if isinstance(
                        par_val, pint.Quantity) else par_val
                    params[k] = mag
                soil_abiotic_params[c] = params

    if has_surf_soil:
        params = {"AirSoilBoundaryThickness": "", "FractionofAreaAvailableforErosion": "",
                  "FractionofAreaAvailableforRunoff": "", "FractionofAreaAvailableforVerticalDiffusion": "",
                  "TotalRunoffRate": ""}
        comp = "Soil_Surface"
        this_comp = pcl.get_compartment(name=comp)
        if soil_abiotic_params.get(comp):
            for k, _ in params.items():
                # par_val = safe_get_val(this_comp, k)
                par_val = this_comp.__getattr__(k)
                mag = par_val.magnitude if isinstance(
                    par_val, pint.Quantity) else par_val
                soil_abiotic_params[comp].setdefault(k, mag)
        else:
            for k, _ in params.items():
                # par_val = safe_get_val(this_comp, k)
                par_val = this_comp.__getattr__(k)
                mag = par_val.magnitude if isinstance(
                    par_val, pint.Quantity) else par_val
                params[k] = mag
            soil_abiotic_params[comp] = params

    return {"soil_params": soil_abiotic_params}


def get_water_params(pcl, parcel_type):
    precipitation_rate = pcl.scenario.Rain
    if precipitation_rate is None:
        precipitation_rate = 0  # 0.0041

    comp_surfaceSoil = pcl.get_compartment(media="Surface_Soil")

    # TODO This is not right. We need params for all chemicals. How to show this in frontend???
    ch = ChemicalService.get(id=32)
    ch.current_scenario(pcl.scenario)

    runoff_watershed_area = 0  # 1e3
    runoff_fraction = 0  # 0.001
    precip_runoff_frac_to_sw = 0

    if len(comp_surfaceSoil) > 0:
        comp_surfaceSoil = comp_surfaceSoil[0]
        runoff_watershed_area = (
            comp_surfaceSoil.area
            * comp_surfaceSoil.FractionofAreaAvailableforRunoff
        ).magnitude
        if precipitation_rate > 0 and comp_surfaceSoil.TotalRunoffRate:
            runoff_fraction = (
                comp_surfaceSoil.TotalRunoffRate / precipitation_rate
            ).magnitude
        if precipitation_rate > 0:
            comp_surfaceWater = pcl.get_compartment(media="Surface_Water")
            if len(comp_surfaceWater) > 0:
                precip_runoff = 0
                for comp_sw in comp_surfaceWater:
                    comp_link = comp_surfaceSoil.get_links(comp_sw)
                    if len(comp_link) > 0:
                        tps = comp_link[0].transport_processes(chemical=ch)
                        precip_runoff += tps[0].eval(sender=comp_surfaceSoil, receiver=comp_sw, chemical=ch)
                precip_runoff_frac_to_sw = precip_runoff / precipitation_rate

    precip_seepage_frac_to_gw = 1 - runoff_fraction

    sed_soil_erosion_to_sw = 100

    runoff_vol_rate_to_sw = 0  # 1
    precipitation_vol_rate_to_sw = 0  # 4.8E6
    seepage_vol_rate_to_gw = 0  # 1
    if precipitation_rate > 0:
        try:
            runoff_vol_rate_to_sw = (
                precipitation_rate
                * precip_runoff_frac_to_sw
                * runoff_watershed_area
            )
        except Exception:
            pass
        try:
            precipitation_vol_rate_to_sw = (precipitation_rate * pcl.area).magnitude
        except Exception:
            pass
        try:
            seepage_vol_rate_to_gw = (
                precipitation_rate
                * precip_seepage_frac_to_gw
                * runoff_watershed_area
            )
        except Exception:
            pass

    water_params = {
        'precip_rate': precipitation_rate,
        'precip_runoff_watershed_area': runoff_watershed_area,
        'precip_seepage_vol_rate_to_GW': seepage_vol_rate_to_gw,
        'precip_runoff_vol_rate_to_SW': runoff_vol_rate_to_sw,
        'precip_vol_rate_to_SW': precipitation_vol_rate_to_sw,
        'sed_soil_erosion_to_SW': sed_soil_erosion_to_sw,
        'runoff_fraction': runoff_fraction,
        'seepage_frac': precip_seepage_frac_to_gw
    }

    sw_params = None
    if 'Water' in parcel_type:
        sw = pcl.get_compartment(media='Surface_Water')[0]
        sw_pars = {parn: par for parn, par in sw.parameters.items()}
        sed = pcl.get_compartment(media='Sediment')[0]
        sed_pars = {parn: par for parn, par in sed.parameters.items()}

        def get_correct_param(par_name, par_obj):
            par = par_obj.get(par_name)
            return par.value if isinstance(par, CustomParameter) else par.default_value if \
                isinstance(par, ParameterDefinition) else None

        wc_external_inflow = 0

        try:
            evaporation_vol_rate = get_correct_param("waterEvaporationRate", sw_pars) * pcl.area.magnitude
        except Exception:
            evaporation_vol_rate = None
        # evaporation_vol_rate = 3.3E6

        try:
            wc_discharge_vol_rate = float('{:.5f}'.format(
                runoff_vol_rate_to_sw
                + seepage_vol_rate_to_gw
                + wc_external_inflow
                + (precipitation_vol_rate_to_sw * 2)
                - evaporation_vol_rate
            ))
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
                'sed_discharge_rate': wc_sed_discharge_rate
            },
            'sed_props': {
                'bed_density': get_correct_param("BedDensity.magnitude", sed_pars),
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
    source_comps = [c for c in pcl.compartments if c.media.isa("Source")]
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
