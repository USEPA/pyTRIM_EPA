import re, json
import numpy as np
from copy import deepcopy
from pprint import pprint
import geopandas as gpd
from shapely.geometry import Polygon, Point
from shapely.prepared import prep
from ..scenarios.utils import init_parameter_definitions
from .defaults import SURFACE_SOIL_SPECIFIC_MEDIA_PARAMS

from flask_api import ApiResult
from pyproj import Transformer

from trim_frontend.scenarios.utils import update_dynamic_params
from trim_db.schema import ureg, CustomParameter, ParameterDefinition, Parcel
from trim_db.services import ChemicalService, CompartmentService, FormulaService, \
    ParameterService, ParcelService, ScenarioService, VolumeElementService
from trim_db.services.parameters import get_or_create_custom_param, update_custom_param_value
from .defaults import get_watershed_area, \
     Air_Parcel_VolElem_defaults, Aquatic_Biota_SW_Compartment_defaults, \
     Aquatic_Biota_Sed_Compartment_defaults, Farm_Biota_SurfSoil_Compartment_defaults, \
     LAND_USE_TYPES, AQUATIC_DIET, Land_Parcel_VolElem_defaults, Water_Parcel_VolElem_defaults, \
     Wet_Dry_Source_VolElem_defaults, EROSION_DEFAULTS
from .forms import ScenarioParcelsForm
from ..scenarios.forms import ScenarioAbioticPropertiesForm
from ..utils.logging import make_logger


# note - this is mainly just code relocated from routes.py with absolutely zero changes.
# handle_parcel_update is technically new -- but is really just refactoring, taking logic that
# lived in the "update_parcel" method in routes.py and refactoring it ever-so-slightly
# so that we can utilize this logic from either UI widgets or CSV uploads. I did NOT write this
# original code and have not done a thorough review
# tfeiler 20240618
#
# manually merged in Max's latest changes on June 29
def handle_parcel_update(p:Parcel, parcels_data:dict):
    logger = make_logger('handle_parcel_update')

    land_use = get_land_use(p)

    print(f"\t\tREFACTORED HANDLE_PARCEL_UPDATE FOR {p}")
    pprint(parcels_data)
    print(f"land_use == '{land_use}'\n")

    air_params = {
        'dustLoad': "DustLoad",
        "dustDensity": "DustDensity",
        "airDensity": "AirDensity",
        "fractionOrganicMatterOnParticulates": "FractionOrganicMatteronParticulates"
    }

    fraction_params = {
        "RunoffFractions": "PrecipitationRunoffFraction",
        "GroundwaterSeepageFractions": "GroundwaterSeepageFraction",
        "EvapotranspirationFractions": "EvapotranspirationFraction"
    }

    misc_water_params = {
        'flush_rate': "Flushes",
        'suspended_sed_conc': "SuspendedSedimentConcentration",
        'algae_density': "AlgaeDensityInWaterColumn",
        'chloride_conc': "ChlorideConcentration",
        'chlorophyll_conc': "ChlorophyllConcentration",
        'mean_depth': "MeanDepth",
        'evaporation_rate': "waterEvaporationRate",
        'suspended_organic_carbon': "OrganicCarbonContent",
        'water_ph': "pH",
        'sed_deposition_vel': "SedimentDepositionVelocity",
        'water_temp': "WaterTemperature",
        'sed_inflow': "ExternalSedimentInflow",
        'externalWaterInflow': "ExternalWaterInflow"
    }

    bed_params = {
        'bed_density': 'BedDensity',
        'organic_carbon_frac': "OrganicCarbonContent",
        'bed_pH': "pH",
        'bed_porosity': "Porosity",
        'bed_thickness': "MeanThickness"
    }

    fish_comps = {
        "Zooplankton": "Zooplankton",
        "FishHerbivore": "Water_Column_Herbivore",
        "FishBenthicOmnivore": "Benthic_Omnivore",
        "FishOmnivore": "Water_Column_Omnivore",
        "FishBenthicCarnivore": "Benthic_Carnivore",
        "FishCarnivore": "Water_Column_Carnivore"
    }

    fish_comps2 = {
        "BenthicCarnivore": "Benthic_Carnivore",
        "BenthicInvertebrate": "Benthic_Invertebrate",
        "BenthicOmnivore": "Benthic_Omnivore",
        "Macrophyte": "Macrophyte",
        "WaterColumnCarnivore": "Water_Column_Carnivore",
        "WaterColumnHerbivore": "Water_Column_Herbivore",
        "WaterColumnOmnivore": "Water_Column_Omnivore",
        "Zooplankton": "Zooplankton"
    }
    fish_fields = ([f'{x}Biomass' for x in fish_comps2] + [f'{x}Weight' for x in fish_comps2])

    misc_params = [
        "pH", "rho", "AverageVerticalVelocity", "FractionSand", "OrganicCarbonContent",
        "VolumeFraction_Liquid", "VolumeFraction_Vapor", "Porosity", "AirSoilBoundaryThickness",
        "FractionofAreaAvailableforErosion", "FractionofAreaAvailableforRunoff",
        "FractionofAreaAvailableforVerticalDiffusion", "TotalRunoffRate"
    ]

    # Update the specified property
    field_name = parcels_data["field"]

    if field_name == "parcelType":
        # Delete all compartments and volume elements
        delete_parcel_contents(p)
        if parcels_data['parcelType'] == "Air Only":
            # add standard Air Volume element and compartments
            # initialize_parcel_contents(p, "Air")
            initialize_parcel_contents(p, Air_Parcel_VolElem_defaults)
        if parcels_data['parcelType'] == "Water Only":
            # add standard Water Volume element and compartments
            initialize_parcel_contents(p, Water_Parcel_VolElem_defaults)
        if parcels_data['parcelType'] == "Land Only":
            # add standard Land Volume element and compartments
            initialize_parcel_contents(p, Land_Parcel_VolElem_defaults)
        if parcels_data['parcelType'] == "Land & Air":
            # concat Land and Air defaults
            land_and_air_parcel_vol_elem_defaults = deepcopy(Land_Parcel_VolElem_defaults)
            land_and_air_parcel_vol_elem_defaults.update(Air_Parcel_VolElem_defaults)
            # add standard Land & Air Volume element and compartments
            initialize_parcel_contents(p, land_and_air_parcel_vol_elem_defaults)
        if parcels_data['parcelType'] == "Water & Air":
            # concat Water and Air defaults
            water_and_air_parcel_vol_elem_defaults = deepcopy(Water_Parcel_VolElem_defaults)
            water_and_air_parcel_vol_elem_defaults.update(Air_Parcel_VolElem_defaults)
            # add standard Water & Air Volume element and compartments
            initialize_parcel_contents(p, water_and_air_parcel_vol_elem_defaults)

    elif field_name == "landUse":
        if parcels_data['landUse'] == land_use:
            return
        if parcels_data['landUse'] in LAND_USE_TYPES:
            print(f'NEW LAND USE DETECTED {land_use} >> {parcels_data["landUse"]}')
            create_base_land_compartments(parcels_data, p, land_use)

        surfsoil_ve = p.get_volume_element("SurfSoil")
        if surfsoil_ve and surfsoil_ve.get_compartment("Farm"): # FFC should reset back to 'No' on change
            CompartmentService.delete(surfsoil_ve.get_compartment("Farm"))
                
        if parcels_data['landUse'] in ['Impervious']:
            if surfsoil_ve and surfsoil_ve.get_compartment("Wetland"):
                CompartmentService.delete(surfsoil_ve.get_compartment("Wetland"))

    elif field_name == "hasFarmFoodChain":
        surfsoil_ve = p.get_volume_element("SurfSoil")
        if parcels_data[field_name] == "Yes":
            CompartmentService.create(
                name="Farm", volume_element=surfsoil_ve,
                media=CompartmentService.media.get(name="Farm"),
            )
        else:
            if surfsoil_ve.get_compartment("Farm"):
                CompartmentService.delete(surfsoil_ve.get_compartment("Farm"))

    elif field_name == "hasFishFoodWeb":
        biotic_ve = deepcopy(Water_Parcel_VolElem_defaults)
        biotic_ve["Sed"]["Compartments"] = deepcopy(Aquatic_Biota_Sed_Compartment_defaults["Compartments"])
        biotic_ve["SW"]["Compartments"] = deepcopy(Aquatic_Biota_SW_Compartment_defaults["Compartments"])
        if parcels_data[field_name] == "Yes":
            sw = p.get_volume_element("SW")
            if sw:
                initialize_parcel_contents(p, biotic_ve)
                init_diet_table_custom_parameters(p)
            else:
                raise ValueError("Cannot create or get Fish Compartment")
        else:
            for vek, vev in biotic_ve.items():
                ve = p.get_volume_element(vek)
                if ve:
                    for k, v in biotic_ve[vek]["Compartments"].items():
                        cmp = ve.get_compartment(v["name"])
                        if cmp:
                            logger.info(f"Deleted {cmp.name}")
                            CompartmentService.delete(cmp, False)

    elif field_name == "hasWetland":
        def update_precip_fractions(ve, vals={}):
            # Wetland has different default surface precipitation values
            surfsoil = ve.get_compartment("Soil_Surface")
            kwargs = {"requirements": f"(self.id == {surfsoil.id})", "scenario_id": ve.parcel.scenario_id}
            
            evapo = surfsoil.parameters.get('EvapotranspirationFraction')
            groundwater = surfsoil.parameters.get('GroundwaterSeepageFraction')
            precip = surfsoil.parameters.get('PrecipitationRunoffFraction')

            evapo = get_or_create_custom_param(evapo, {**kwargs, "definition_id": evapo.id})
            groundwater = get_or_create_custom_param(groundwater, {**kwargs, "definition_id": groundwater.id})
            precip = get_or_create_custom_param(precip, {**kwargs, "definition_id": precip.id})
            
            update_custom_param_value(evapo, vals["evapo"])
            update_custom_param_value(groundwater, vals["groundwater"])
            update_custom_param_value(precip, vals["precip"])

            update_dynamic_params(p.scenario)

        if parcels_data[field_name] == "Yes":
            ve = p.get_volume_element("SurfSoil")
            if ve:
                m = CompartmentService.media.get(name='Wetland')
                c = CompartmentService.get_or_create(name="Wetland", volume_element=ve, media=m)
                update_precip_fractions(ve, {"evapo":0.4, "groundwater":0, "precip":0.6})
            else:
                raise ValueError("Cannot create or get Wetland Compartment")
        else:
            ve = p.get_volume_element("SurfSoil")
            if ve:
                c = ve.get_compartment("Wetland")
                if c:
                    CompartmentService.delete(c, False)
                update_precip_fractions(ve, {"evapo":0.35, "groundwater":0.25, "precip":0.4})

    elif field_name == "description":
        p.description = parcels_data['description']

    elif field_name == 'totalErosionRate':
        val = float(parcels_data['totalErosionRate'])
        for c in p.compartments:
            if c.media.isa('Surface_Soil'):
                ter = c.parameters.get('TotalErosionRate')
                par = get_or_create_custom_param(
                    ter,
                    {"requirements": f"(self.id == {c.id})", "scenario_id": p.scenario_id},
                )
                update_custom_param_value(par, val)
        ParameterService.commit()

    elif ("erosion1-" in field_name or "erosion2-" in field_name or "erosion3-" in field_name): # HACKY
        option_num = int(field_name.split('-')[0].replace('erosion', ''))

        # Delete all erosionN- params for other options,
        # and only store one active parameter at a time
        for param in list(p.scenario.parameters.values()):
            if not isinstance(param, CustomParameter):
                continue
            if not(
                param.variable_name.startswith('erosion1-')
                or param.variable_name.startswith('erosion2-')
                or param.variable_name.startswith('erosion3-')
            ):
                continue
            if not param.requirements == f'(self.id == {p.id})':
                continue
            if (
                param.variable_name.endswith('-active')
                or not param.variable_name.startswith(f'erosion{option_num}-')
            ):
                ParameterService.delete(param, no_commit=True)

        # Create/update the specified parameter
        param_def = ParameterService.definitions.get_or_create(
            variable_name=field_name,
            full_name=field_name,
            domain=ParameterService.domains.get(name='Scenario')
        )
        param = ParameterService.get_or_create(
            definition_id=param_def.id,
            scenario_id=p.scenario_id,
            requirements=f'(self.id == {p.id})', # parcel id
        )
        val = parcels_data[field_name]
        has_value = (str(val) == '0' or (val or ''))
        if has_value:
            # has value; update the param
            param.value = parcels_data[field_name]
            ParameterService.update(param)
        else:
            # no value; delete the param
            ParameterService.delete(param)

        if has_value and (str(parcels_data.get('is_active')).lower() == 'true'):
            # Create/update the specified parameter active flag
            param_def = ParameterService.definitions.get_or_create(
                variable_name=f'{field_name}-active',
                full_name=f'{field_name}-active',
                domain=ParameterService.domains.get(name='Scenario')
            )
            param = ParameterService.get_or_create(
                definition_id=param_def.id,
                scenario_id=p.scenario_id,
                requirements=f'(self.id == {p.id})', # parcel id
            )
            param.value = 1
            ParameterService.update(param)

    elif field_name in air_params:
        par_name = air_params[field_name]
        # the below part was generating error due to missing par for dustLoad, dustDensity etc...
        cmp = [c for c in p.compartments if "Air in Air_" in c.standard_name][0]
        par = get_or_create_custom_param(
            cmp.parameters.get(par_name),
            {"requirements": f"(self.id == {cmp.id})", "scenario_id": p.scenario_id},
        )
        update_custom_param_value(par, parcels_data[field_name])
        ParameterService.commit()

    elif field_name == "surfaceSoilThickness":
        update_soil_thickness(p, "Soil_Surface", 'SurfSoil', parcels_data['surfaceSoilThickness'])

    elif field_name == "rootSoilThickness":
        update_soil_thickness(p, "Soil_Root_Zone", 'RootSoil', parcels_data['rootSoilThickness'])

    elif field_name == "vadoseSoilThickness":
        update_soil_thickness(p, "Soil_Vadose_Zone", 'VadoseSoil', parcels_data['vadoseSoilThickness'])
        
    elif field_name == "groundwaterZoneSoilThick":
        update_soil_thickness(p, "Groundwater", 'GW', parcels_data['groundwaterZoneSoilThick'])

    elif field_name == "tillage":
        for c in p.compartments:
            if c.name == 'Soil_Surface':
                par = get_or_create_custom_param(
                    ParameterService.definitions.get(full_name="soilTillage"),
                    {
                        "requirements": f"(self.id == {c.id})",
                        "scenario_id": p.scenario.id,
                    },
                    no_commit=True
                )
                if parcels_data['tillage'] == "Yes":
                    update_custom_param_value(par, 1)
                elif parcels_data['tillage'] == "No":
                    update_custom_param_value(par, 0)
        ParameterService.commit()

    elif field_name in fraction_params:
        soil_comp = p.get_compartment("Soil_Surface")
        # data_name = field_name if field_name == "GroundwaterSeepageFractions" else "RunoffFractions"
        # seepage_frac_val = float(parcels_data[data_name]) if data_name == "GroundwaterSeepageFractions" else 1-float(parcels_data[data_name])
        # runoff_frac_val = 1 - seepage_frac_val
        # watershed_area = (
        #         soil_comp.area
        #         * soil_comp.FractionofAreaAvailableforRunoff
        # ).magnitude
        # evapotranspiration_frac_val = parcels_data["EvapotranspirationFractions"]
        # seepage_frac_val = parcels_data["GroundwaterSeepageFractions"]
        # runoff_frac_val = parcels_data["RunoffFractions"]
        frac_val = float(parcels_data[field_name])
        # for par_name, par_val in {"TotalRunoffRate": total_runoff_val, "GroundwaterSeepageFraction": seepage_frac_val,
        #                           "EvapotranspirationFraction": evapotranspiration_frac_val}.items():
        par_name = fraction_params[field_name]
        par_val = frac_val
        par = get_or_create_custom_param(
            soil_comp.parameters.get(par_name),
            {
                "requirements": f"(self.id == {soil_comp.id})",
                "scenario_id": p.scenario.id,
            },
            no_commit=True
        )
        update_custom_param_value(par, par_val)

        if field_name == "RunoffFractions":
            update_dynamic_params(p.scenario)
            ParcelService.update(p)
            return ApiResult(json.dumps({
                'message': 'success',
                'TotalRunoffRate': soil_comp.TotalRunoffRate.magnitude
            }))

    elif field_name in misc_water_params:
        par_name = misc_water_params[field_name]
        comp = p.get_compartment("Surface_water")
        par = comp.parameters.get(par_name)

        if field_name == "mean_depth":
            csw = p.get_compartment("Surface_water")
            h_diff = (csw.height.magnitude - float(parcels_data[field_name]))
            # Now shift bounds of everything below the SW volume element
            ves = [a for a in p.volume_elements]
            for ve in ves:
                if ve.top <= csw.volume_element.bottom:
                    print(f'new {ve.name} top = {ve.top + h_diff} and bottom = {ve.bottom + h_diff}')
                    ve.top = ve.top + h_diff
                    ve.bottom = ve.bottom + h_diff
            # finally fix the surface water element bottom
            csw.volume_element.bottom = -1 * float(parcels_data[field_name])

        if par:
            par = get_or_create_custom_param(
                par,
                {
                    "requirements": f"(self.id == {comp.id})",
                    "scenario_id": p.scenario.id,
                }
            )
            update_custom_param_value(par, parcels_data[field_name])

        if field_name == 'flush_rate':
            if not par.formula:
                new_formula_obj = FormulaService.create(equation=parcels_data['autocalc'])
                par.formula = new_formula_obj
            else:
                FormulaService.get(par.formula.id).equation = parcels_data['autocalc']
                FormulaService.commit()

    elif field_name in bed_params:
        par_name = bed_params[field_name]
        comp = p.get_compartment("Sediment")
        par = comp.parameters.get(par_name)
        if field_name == "bed_thickness":
            sed_ve = comp.volume_element
            thickness_before = sed_ve.height
            sed_ve.bottom = sed_ve.top - float(parcels_data[field_name])
            thickness_now = sed_ve.height

            # shift everything below the sediment volume element
            delta_thickness = thickness_now.magnitude - thickness_before.magnitude
            ves = [a for a in p.volume_elements]
            for ve in ves:
                if ve.top <= sed_ve.bottom:
                    print(f'new {ve.name} top = {ve.top - delta_thickness} and bottom = {ve.bottom - delta_thickness}')
                    ve.top = ve.top - delta_thickness
                    ve.bottom = ve.bottom - delta_thickness

        elif par:
            par = get_or_create_custom_param(
                par,
                {
                    "requirements": f"(self.id == {comp.id})",
                    "scenario_id": p.scenario.id,
                },
            )
            update_custom_param_value(par, parcels_data[field_name])
        else:
            par_obj = [pp for pp in ParameterService.definitions.get_all() if
                       pp.full_name == par_name]
            comp.parameters.add(par_name, domain_name="Compartment", unit=par_obj[0].default_unit)
            comp.parameters.get(par_name).value = parcels_data[field_name]
            comp.parameters.get(par_name).scenario_id = p.scenario_id

    elif field_name in fish_comps:
        comp_name = fish_comps[field_name]
        params = [pd for pd in parcels_data.keys() if pd not in ["id", "field", "csrf_token"]]
        # print(f"{field_name} {[c for c in p.compartments if c.name == comp_name[field_name]]}")
        this_comp = [c for c in p.compartments if c.name == comp_name][0]
        for param in params:
            this_par = get_or_create_custom_param(
                this_comp.parameters[param],
                {"requirements": f"(self.id == {this_comp.id})", "scenario_id": p.scenario_id},
                no_commit=True
            )
            update_custom_param_value(this_par, parcels_data[param])
        ParameterService.commit()

    elif field_name in fish_fields:
        if "Biomass" in field_name:
            base_name = field_name.replace("Biomass", "")
            prop = "BiomassPerArea"
        elif "Weight" in field_name:
            base_name = field_name.replace("Weight", "")
            prop = "BW"

        for this_comp in p.compartments:
            if this_comp.name == fish_comps2[base_name]:
                this_param = get_or_create_custom_param(
                    this_comp.parameters.get(prop),
                    {"requirements": f"(self.id == {this_comp.id})", "scenario_id": p.scenario_id},
                    no_commit=True
                )
                update_custom_param_value(this_param, float(parcels_data[field_name]))
        ParameterService.commit()

    elif field_name in misc_params:
        this_comp = p.get_compartment(name=parcels_data["comp_name"])
        this_par = get_or_create_custom_param(
            this_comp.parameters.get(parcels_data["field"]),
            {"requirements": f"(self.id == {this_comp.id})", "scenario_id": p.scenario_id},
        )
        update_custom_param_value(this_par, float(parcels_data[field_name]))

        # we no longer want to use a formula for auto calculating this
        if field_name in ['AverageVerticalVelocity', 'TotalRunoffRate'] and this_par.formula:
            this_par.formula = None
            ParameterService.commit()

    elif field_name == "emission":
        src_comp = p.get_compartment(name=parcels_data["compartment_name"])
        src_par = src_comp.parameters.get('surfaceDepositionRate')
        chem = ChemicalService.get(name=parcels_data["chemical_name"])
        if src_par:
            src_par = get_or_create_custom_param(
                src_par,
                {"requirements": f"(self.id == {src_comp.id})", "scenario_id": p.scenario.id},
                new_formula=True
            )

            eq = src_par.formula.equation
            # We have the chemical in the formula
            if f'chemical.id == {str(chem.id)}' in eq:
                formula_parts = eq.split(f"if chemical.id == {chem.id}")
                formula_part = formula_parts[0]
                if "else" in formula_part:
                    arr = formula_part.split("else")[:-1]
                    formula_part = "else".join(arr + [f' {parcels_data["emission_value"]} '])
                else:
                    formula_part = f'{parcels_data["emission_value"]} '
                formula_parts[0] = formula_part
                new_formula = f"if chemical.id == {chem.id}".join(formula_parts)
                print(new_formula)
            # We do not have the chemical in the formula. We need to add it...
            else:
                eq_arr = eq.split("else")
                eq_arr.insert(-2, f' {parcels_data["emission_value"]} if chemical.id == {chem.id} ')
                new_formula = "else".join(eq_arr)
                print(new_formula)
            FormulaService.get(src_par.formula.id).equation = new_formula
            FormulaService.commit()
    elif field_name == "initial concentration":
        ic_comp = p.get_compartment(name=parcels_data["compartment_name"])
        ic_par = ic_comp.parameters.get('initialConcentration')
        chem = ChemicalService.get(name=parcels_data["chemical_name"])
        if ic_par:
            unit = "g / m^3" if ic_comp.media.id in [2, 5, 7, 56, 55, 8, 9] else "g / kg" if ic_comp.media.id in [23, 24, 27, 28, 29, 31, 32, 33, 37, 39, 41, 43, 44, 45, 46, 47, 48, 49, 50, 51] else "g / L" if ic_comp.media.id in [10, 4] else ""
            ic_par = get_or_create_custom_param(
                ic_par,
                {"requirements": f"(self.id == {ic_comp.id})", "scenario_id": p.scenario.id, "unit": unit},
                new_formula=True
            )

            eq = ic_par.formula.equation
            # We have the chemical in the formula
            if f'chemical.id == {str(chem.id)}' in eq:
                formula_parts = eq.split(f"if chemical.id == {chem.id}")
                formula_part = formula_parts[0]
                if "else" in formula_part:
                    arr = formula_part.split("else")[:-1]
                    formula_part = "else".join(arr + [f' {parcels_data["initial_concentration_value"]} '])
                else:
                    formula_part = f'{parcels_data["initial_concentration_value"]} '
                formula_parts[0] = formula_part
                new_formula = f"if chemical.id == {chem.id}".join(formula_parts)
                print(new_formula)
            # We do not have the chemical in the formula. We need to add it...
            else:
                eq_arr = eq.split("else")
                eq_arr.insert(-2, f' {parcels_data["initial_concentration_value"]} if chemical.id == {chem.id} ')
                new_formula = "else".join(eq_arr)
                print(new_formula)
            FormulaService.get(ic_par.formula.id).equation = new_formula
            FormulaService.commit()
    elif field_name == "runoff_matrix_value":
        scn = ScenarioService.get(id=p.scenario.id)
        sender_parcel_name = parcels_data["sender"].replace("ro_", "")
        receivers = parcels_data["receiver"].split(",")
        values = parcels_data["ro_value"].split(",")
        sp = [sp for sp in scn.parcels if sp.name == sender_parcel_name][0]
        sender_comp = sp.get_compartment("Soil_Surface")
        sender_par = [sender_comp.parameters.get("FractionOfTotalRunoff")]
        if len(sender_par) > 0:
            sender_par = get_or_create_custom_param(
                sender_par[0],
                {"requirements": f"(self.id == {sender_comp.id})", "scenario_id": scn.id},
                new_formula=True
            )

            eq = sender_par.formula.equation
            for ri, rec in enumerate(receivers):
                receiver_name = rec.replace("ro_", "")
                replacing_value = values[ri]
                if receiver_name == "sink":  # Runoff goes directly to the sin in same parcel (sender parcel)
                    receiver_comp = sp.get_compartment(name="Soil_Advection_Sink", media="Advection")
                    if isinstance(receiver_comp, list):
                        receiver_comp = receiver_comp[0]
                else:
                    rp = [rp for rp in scn.parcels if rp.name == receiver_name][0]
                    receiver_comp = rp.get_compartment("Soil_Surface")
                    if not receiver_comp: # try for water parcels
                        receiver_comp = rp.get_compartment("Surface_water")
                entity_name = "receiver"
                formula_entity = receiver_comp
                # this pattern captures integers, decimals and/or numbers with scientific notations that may or may
                # not be in parentheses
                val_pattern = re.compile(r"\(?(\d+(?:\.\d+(?:[eE][+\-]?\d+)?))\)?")
                # We have the receiver compartment in the formula
                if not sender_comp.connects_to(receiver_comp):
                    CompartmentService.links.create(sender_id=sender_comp.id, receiver_id=receiver_comp.id)
                # TODO #2 if a value is given as zero and it exists in formula remove it from formula paying
                #  attention to parenthesis.
                if f'{entity_name}.id in {{{str(formula_entity.id)}}}' in eq:
                    formula_parts = eq.split(f"if {entity_name}.id in {{{formula_entity.id}}}")
                    formula_part = formula_parts[0]
                    if "else" in formula_part:
                        arr = formula_part.split("else")[:-1]
                        val_part = formula_part.split("else")[-1]
                        val_to_replace = val_pattern.findall(val_part)
                        rep_val = val_part.replace(val_to_replace[0], replacing_value)
                        formula_part = "else".join(arr + [f' {rep_val} '])
                    else:
                        val_to_replace = val_pattern.findall(formula_part)
                        rep_val = formula_part.replace(val_to_replace[0], replacing_value)
                        formula_part = f'{rep_val}'
                    formula_parts[0] = formula_part
                    new_formula = f"if {entity_name}.id in {{{formula_entity.id}}}".join(formula_parts)
                    print(new_formula)
                # We do not have the receiver compartment in the formula. We need to add it...
                else:
                    eq_arr = eq.split("else")
                    eq_arr.insert(-2, f' ({replacing_value}) if {entity_name}.id in {{{formula_entity.id}}} ')
                    new_formula = "else".join(eq_arr)
                    print(new_formula)
                eq = new_formula
            FormulaService.get(sender_par.formula.id).equation = new_formula
            FormulaService.commit()
    elif field_name == "receptor_spacing":
        submitted_spacing_val = parcels_data.get("receptor_spacing")

        if (not str(submitted_spacing_val).isnumeric()):
            raise Exception(f"bad input {submitted_spacing_val}")

        cdv = p.get_compartment('DryVaporSource')
        param_obj = cdv.parameters.get("ReceptorSpacing")

        # first time through this is a "ParameterDefinition"; subsequent visits
        # it is a CustomParameter....so create/update as needed
        if type(param_obj) is ParameterDefinition:
            param = ParameterService.get_or_create(
                definition_id=param_obj.id,
                scenario_id=p.scenario_id,
                requirements=f"(self.id == {cdv.id})", # compartment id
                value=submitted_spacing_val
            )

            ParameterService.update(param)
        elif type(param_obj) is CustomParameter:
            param_obj.value = submitted_spacing_val
            ParameterService.update(param_obj)
        else:
            raise Exception("unexpected param_obj type...")

        ParameterService.commit()
    elif field_name == "vertices":
        print(f"save vertices change FOR {p.id} / {p.name}...")
        coords_data = json.loads(parcels_data.get("vertices", []))

        if coords_data:
            # coords_data is lat,long; we store long,lat in TRIM
            long_lat = [ [x[1], x[0]] for x in coords_data ]
            p.vertices = long_lat


    # Update record
    ParcelService.update(p)

# TODO - define "Air Only", etc. as constants somewhere?!?!?
# forgiving translation of user-supplied value
def get_canonical_parcel_type(p_type):
    normalized = p_type.upper().replace(" ", "")

    if normalized == "AIRONLY":
        return "Air Only"
    elif normalized == "WATERONLY":
        return "Water Only"
    elif normalized == "LANDONLY":
        return "Land Only"
    elif normalized == "LAND&AIR":
        return "Land & Air"
    elif normalized == "WATER&AIR":
        return "Water & Air"


# forgiving translation of user-supplied value
def get_canonical_land_use_type(lu_type):
    normalized = lu_type.upper().replace(" ", "")

    for x in LAND_USE_TYPES:
        if x.upper().replace(" ", "") == normalized:
            return x


def get_ve_defaults_for_parcel_type(parcel_type):
    normalized = parcel_type.upper().replace(" ", "")

    if normalized == "AIRONLY":
        return Air_Parcel_VolElem_defaults
    elif normalized == "WATERONLY":
        return Water_Parcel_VolElem_defaults
    elif normalized == "LANDONLY":
        return Land_Parcel_VolElem_defaults
    elif normalized == "LAND&AIR":
        combo = deepcopy(Land_Parcel_VolElem_defaults)
        combo.update(Air_Parcel_VolElem_defaults)
        return combo
    elif normalized == "WATER&AIR":
        combo = deepcopy(Water_Parcel_VolElem_defaults)
        combo.update(Air_Parcel_VolElem_defaults)
        return combo


def initialize_parcel_contents(new_parcel, vol_elem_defaults=None):
    if vol_elem_defaults is None:
        vol_elem_defaults = deepcopy(Land_Parcel_VolElem_defaults)
        vol_elem_defaults.update(Air_Parcel_VolElem_defaults)
    else:
        vol_elem_defaults = deepcopy(vol_elem_defaults)
    # Add the Sources
    vol_elem_defaults.update(Wet_Dry_Source_VolElem_defaults)

    for ve_name, ve in vol_elem_defaults.items():
        # Create standard volume elements
        nve = VolumeElementService.get_or_create(
            name=ve_name,
            parcel=new_parcel,
            create_kwargs={
                'top': ve['top'],
                'bottom': ve['bottom']
            }
        )
        nve.top = ve['top']
        nve.bottom = ve['bottom']
        for c_name, c in ve["Compartments"].items():
            # print(f'creating {c_name} for volume element {ve_name}')
            # Create standard compartments linking them to default volume elements and media for each compartment
            # nc = new_parcel.get_compartment(c_name) # This won't work because the compartment names are not unique
            nc = CompartmentService.get_or_create(
                name=c_name, volume_element=nve, no_commit=True
            )
            nc.volume_element = nve
            if nc.media is None or nc.media.name != c['media_name']:
                nc.media = CompartmentService.media.get(name=c["media_name"])
            # print('- initializing params')
            initialize_compartment_custom_parameters(nc)
    ParameterService.commit()

    update_dynamic_params(new_parcel.scenario, skip_existing=True)

# This is for parameters of new compartments whose default value cannot be used
# and will need custom parameters defined
# at the time of creation of new compartment.
def initialize_compartment_custom_parameters(nc):
    # Add in custom parameters for new compartments using the self.id = <id of new compartment>
    this_parcel = nc.volume_element.parcel
    if nc.media.isa('Surface_Soil'):
        # Default Total Erosion Rate
        ter_val = calc_default_erosion_rate_sdr(this_parcel)
        add_compartment_custom_parameters(nc, "TotalErosionRate", ter_val, "kg/m^2/day")

    if nc.media.isa("Flora"):
        # add AllowExchange_Dynamic, AllowExchange_SteadyState_forAir, AllowExchange_SteadyState_forOther
        ae_pars_ss = ['AllowExchange_SteadyState_forAir', 'AllowExchange_SteadyState_forOther']
        # Using 1 for steady state (continuously exchanging) as default
        for ae_par in ae_pars_ss:
            ae_ss_val = 1
            add_compartment_custom_parameters(nc, ae_par, ae_ss_val, None)
        # Search scenario and see if compartments with same media exists and use their Allow Exchange
        # (should be fixed value for that media across all parcels of the scenario for compartments with
        # that media
        search_comps = [c for c in this_parcel.scenario.compartments if c.media.isa(nc.media)]
        ae_val = 0.5
        if len(search_comps) > 0:
            ae_vals = list(set([c.parameters.get("AllowExchange_Dynamic").value for c in search_comps if
                                c.parameters.get("AllowExchange_Dynamic") is not None and
                                isinstance(c.parameters.get("AllowExchange_Dynamic"), CustomParameter)]))
            if len(ae_vals) > 0:
                ae_val = ae_vals[0]
        add_compartment_custom_parameters(nc, 'AllowExchange_Dynamic', ae_val, None)

    if nc.media.isa("Soil") or nc.media.isa("Groundwater"):
        # get the defaults from the user defined json templates in the frontend
        # add pH
        ph_val = get_default_value_from_json_form(f"Abiotic_{nc.media.name}", 'pH')
        add_compartment_custom_parameters(nc, 'pH', ph_val, None)
        # add OrganicCarbonContent
        occ_val = get_default_value_from_json_form(f"Abiotic_{nc.media.name}", 'OrganicCarbonContent')
        add_compartment_custom_parameters(nc, 'OrganicCarbonContent', occ_val, None)
        if not nc.media.isa("Groundwater"):
            # add Air content
            air_c_val = get_default_value_from_json_form(f"Abiotic_{nc.media.name}", 'VolumeFraction_Vapor')
            add_compartment_custom_parameters(nc, 'VolumeFraction_Vapor', air_c_val, None)
            # add Water content
            water_c_val = get_default_value_from_json_form(f"Abiotic_{nc.media.name}", 'VolumeFraction_Liquid')
            add_compartment_custom_parameters(nc, 'VolumeFraction_Liquid', water_c_val, None)

    if nc.media.isa('Dry_Vapor'):
        receptor_spacing_val = get_default_value_from_json_form('Parcels_Props', 'parcels-receptor_spacing')
        add_compartment_custom_parameters(nc, 'ReceptorSpacing', int(receptor_spacing_val), None)

    # if nc.media.isa('Surface_Water') or nc.media.isa("Sediment"):


def add_compartment_custom_parameters(nc, par_name, par_val, par_unit):
    return get_or_create_custom_param(
        ParameterService.definitions.get(full_name=par_name),
        {
            "requirements": f"(self.id == {nc.id})",
            "scenario_id": nc.volume_element.parcel.scenario.id,
            "value": par_val,
            "unit": par_unit,
        },
        no_commit=True
    )


def init_diet_table_custom_parameters(pcl):
    comp_names = AQUATIC_DIET.keys()
    for comp_name in comp_names:
        comp = pcl.get_compartment(comp_name)
        for param_name in AQUATIC_DIET[comp_name]:
            param = get_or_create_custom_param(
                comp.parameters[param_name],
                {"requirements": f"(self.id == {comp.id})", "scenario_id": pcl.scenario_id},
                no_commit=True
            )
            param.value = AQUATIC_DIET[comp_name][param_name]
    ParameterService.commit()


def calc_default_erosion_rate_sdr(pcl):
    surf_soil_comp = pcl.get_compartment(media='Surface_Soil')
    if not surf_soil_comp:
        return None
    else:
        surf_soil_comp = surf_soil_comp[0]

    has_farm_food_chain = pcl.get_compartment(media='Farm') or False

    land_use = get_land_use(pcl)
    if land_use == 'Impervious':
        cover_management_factor = 0
    elif land_use in ['Agriculture (General)', 'Tilled Soil']:
        if has_farm_food_chain:
            cover_management_factor = 0.5
        else:
            cover_management_factor = 1.0
    elif land_use == 'Untilled Soil':
        if has_farm_food_chain:
            cover_management_factor = 0.1
        else:
            cover_management_factor = 1.0
    else:
        cover_management_factor = 0.1

    unit_soil_loss = (
        EROSION_DEFAULTS['R']
        * EROSION_DEFAULTS['K']
        * EROSION_DEFAULTS['LS']
        * cover_management_factor
        * EROSION_DEFAULTS['P']
    ).to('(kg / m^2) / day')

    area_in_sq_mile = pcl.area.to('mile^2').magnitude
    if area_in_sq_mile <= 0.1:
        intercept_coef = 2.1
    elif 0.1 < area_in_sq_mile <= 1:
        intercept_coef = 1.9
    elif 1 < area_in_sq_mile <= 10:
        intercept_coef = 1.4
    elif 10 < area_in_sq_mile <= 100:
        intercept_coef = 1.2
    else:
        intercept_coef = 0.6

    intercept_coef = intercept_coef

    slope_coef = surf_soil_comp.parameters["sedimentDeliveryRatioSlopeCoef"].default_value
    sed_delivery_ratio = intercept_coef * (pcl.area.magnitude ** (-1 * slope_coef))

    return (unit_soil_loss * sed_delivery_ratio).magnitude


def get_land_use(pcl):
    land = False
    land_use = 'Grasses/Herbs'
    for comp in pcl.compartments:
        if comp.media.isa('Surface_Soil', or_child=False):
            land = True
        elif comp.media.isa('Coniferous_Forest'):  # Check land use
            land = True
            land_use = 'Coniferous Forest'
        elif comp.media.isa('Deciduous_Forest'):
            land = True
            land_use = 'Deciduous Forest'
        elif comp.media.isa('Agriculture'):
            land = True
            land_use = 'Agriculture (General)'
        elif comp.media.isa('Grass'):
            land = True
            land_use = 'Grasses/Herbs'
        elif comp.media.isa('Tilled_Soil'):
            land = True
            land_use = 'Tilled Soil'
        elif comp.media.isa('Untilled_Soil'):
            land = True
            land_use = 'Untilled Soil'
    if not land:
        land_use = 'N/A'  # No land use for air-only and water-only parcels
    return land_use


PARAMS_WITH_COMPARTMENT_ID_IN_FORMULA = [
    "MethylationRate", "DemethylationRate", "ReductionRate"
]


def delete_parcel_contents(del_parcel):
    print('deleting parcel compartments')
    for c in del_parcel.compartments:
        # Delete Links
        comp_id = c.id
        scenario_id = c.current_scenario().id
        lr = CompartmentService.links.get_all(receiver_id=comp_id)
        ls = CompartmentService.links.get_all(sender_id=comp_id)
        for lnk_r in lr:
            CompartmentService.links.delete(lnk_r)
        for lnk_s in ls:
            CompartmentService.links.delete(lnk_s)

        # Delete Custom Parameters
        # print(f'- delete parameters for {c}')
        custom_params = ParameterService(c).get_own_custom_parameters()
        for cp in custom_params:
            ParameterService.delete(cp, no_commit=True)

        # Delete compartment id from formulas with custom values for give compartment (from legacy Trim)
        # print(f'-- remove compartment {c} from custom formulas')
        for var_name in PARAMS_WITH_COMPARTMENT_ID_IN_FORMULA:
            par = ParameterService.get_custom_parameters_by_name(
                var_name, scenario_id=scenario_id
            )
            if not par:
                continue
            par = par[0]
            eq = par.formula.equation
            del_id = c.id
            if str(del_id) not in eq:
                continue
            eq_parts = eq.split('compartment.id in {')
            for i, p in enumerate(eq_parts):
                if i == 0:
                    continue
                sub_parts = p.split('}')
                complist = sub_parts[0].split(",")

                # tfeiler bandaid - not fully following logic here; just avoiding a crash
                if len(complist) == 1 and complist[0].strip() == '':
                    new_complist = ''
                else:
                    new_complist = [str(int(i.strip())) for i in complist if int(i.strip()) != del_id]

                sub_parts[0] = " , ".join(new_complist)
                eq_parts[i] = "}".join(sub_parts)
            new_eq = 'compartment.id in {'.join(eq_parts)
            ParameterService.get(par.id).formula.equation = new_eq
            # ParameterService.commit()

        # Delete Compartments
        # print(f'- delete compartment {c}')
        CompartmentService.delete(c)

    # Delete associated HACKY params at the scenario level
    print('deleting erosion-table parameters')
    for param in list(del_parcel.scenario.parameters.values()):
        if not isinstance(param, CustomParameter):
            continue
        if not param.requirements == f'(self.id == {del_parcel.id})':
            continue
        if not(
            param.variable_name.startswith('erosion1-')
            or param.variable_name.startswith('erosion2-')
            or param.variable_name.startswith('erosion3-')
        ):
            continue
        ParameterService.delete(param, no_commit=True)

    # Delete Volume Elements
    print('deleting parcel volume elements')
    for ve in del_parcel.volume_elements:
        # print(f'- delete volume element {ve}')
        VolumeElementService.delete(ve, False)


# Some parameters just not have any default values or any values to be referenced at the time of the
# initialization/creation of the entity (i.e. compartment). In these cases we can get the default values from
# the relevant flask form template (json) from the frontend.
def get_default_value_from_json_form(form_name, parameter_name):
    json_forms = {
        'Abiotic_Air': ScenarioAbioticPropertiesForm.__getattribute__(
            ScenarioAbioticPropertiesForm, "AirAbioticTable"
        ),
        'Abiotic_Surface_Soil': ScenarioAbioticPropertiesForm.__getattribute__(
            ScenarioAbioticPropertiesForm, "SurfaceSoilAbioticTable"
        ),
        'Abiotic_Tilled_Soil': ScenarioAbioticPropertiesForm.__getattribute__(
            ScenarioAbioticPropertiesForm, "SurfaceSoilAbioticTable"
        ),
        'Abiotic_Root_Zone': ScenarioAbioticPropertiesForm.__getattribute__(
            ScenarioAbioticPropertiesForm, "RootSoilAbioticTable"
        ),
        'Abiotic_Vadose_Zone': ScenarioAbioticPropertiesForm.__getattribute__(
            ScenarioAbioticPropertiesForm, "VadoseSoilAbioticTable"
        ),
        'Abiotic_Groundwater': ScenarioAbioticPropertiesForm.__getattribute__(
            ScenarioAbioticPropertiesForm, "GWSoilAbioticTable"
        ),
        'Parcels_Props': getattr(ScenarioParcelsForm, "mapTable")
    }
    form_obj = json_forms[form_name]
    form_class = form_obj.kwargs['form_class']
    def_val = form_class.__getattribute__(form_class, parameter_name).kwargs["default"]
    return def_val


def update_soil_thickness(p, comp_name, layer_name, thickness):
    soil_ve = p.get_compartment(comp_name).volume_element

    thickness_before = soil_ve.height
    soil_ve.bottom = soil_ve.top + (-1 * float(thickness))
    thickness_now = soil_ve.height
    delta_thickness = thickness_now.magnitude - thickness_before.magnitude
    for layer in Land_Parcel_VolElem_defaults[layer_name]['layers']:
        soil_ve = p.get_compartment(layer).volume_element
        soil_ve.top = (-1 * delta_thickness) + soil_ve.top
        soil_ve.bottom = (-1 * delta_thickness) + soil_ve.bottom


def create_base_land_compartments(parcels_data, p, land_use):
    ve_surfsoil = VolumeElementService.get(name="SurfSoil", parcel_id=p.id)
    c_surfsoil = CompartmentService.get(name="Soil_Surface", volume_element_id=ve_surfsoil.id)

    custom_param_erosion = c_surfsoil.parameters.get("TotalErosionRate")
    custom_param_erosion = get_or_create_custom_param(custom_param_erosion, {
        "scenario_id": p.scenario_id,
        "requirements": f'(self.id == {c_surfsoil.id})',
        "value": 0
    })

    # delete existing compartments
    if land_use in ['Tilled Soil', 'Untilled Soil', 'Impervious']:
        # Revert Soil_surface compartment to default media (Surface_Soil [id = 7])
        c_surfsoil.media = CompartmentService.media.get(name="Surface_Soil")  # Surface Soil
        CompartmentService.update(c_surfsoil)
        # if switching from Impervious, calculate Total erosion rate
        if land_use == 'Impervious':
            custom_param_erosion.value = calc_default_erosion_rate_sdr(p)
    else:
        # it is flora so delete compartments with a flora parent
        for c in p.compartments:
            if c.media.isa('Flora'):
                # Remove links (foreign key constraint)
                lr = CompartmentService.links.get_all(receiver_id=c.id)
                ls = CompartmentService.links.get_all(sender_id=c.id)
                for lnk_r in lr:
                    CompartmentService.links.delete(lnk_r)
                for lnk_s in ls:
                    CompartmentService.links.delete(lnk_s)
                # Remove custom_parameters with the requirement self.id = c.id
                # Again this is not a good way to find the custom parameters of the compartment
                # custom_params = ParameterService.get_all(requirements=f'(self.id == {c.id})')
                custom_params = [cp for _, cp in c.parameters.items() if isinstance(cp, CustomParameter)]
                for cp in custom_params:
                    ParameterService.delete(cp, False)
                # Remove compartments
                CompartmentService.delete(c, False)

    # Create the base compartments for the new land use/ land cover
    new_comps = []
    if parcels_data['landUse'] == 'Tilled Soil':
        c_surfsoil.media_id = CompartmentService.media.get(name='Tilled_Soil').id
        init_tillage_default_params('Tilled_Soil')
        update_tillage_formula_media('Tilled_Soil')
        c_surfsoil.soilTillage = 1

    elif parcels_data['landUse'] == 'Untilled Soil':
        c_surfsoil.media_id = CompartmentService.media.get(name='Untilled_Soil').id
        init_tillage_default_params('Untilled_Soil')
        update_tillage_formula_media('Untilled_Soil')
        c_surfsoil.soilTillage = 0

    elif parcels_data['landUse'] == 'Impervious':
        c_surfsoil.media_id = CompartmentService.media.get(name='Impervious').id
        custom_param_erosion.value = 0

    elif parcels_data['landUse'] == 'Coniferous Forest':
        new_comps += [
            CompartmentService.create(
                name="Leaf_Coniferous_Forest", volume_element=ve_surfsoil, media=CompartmentService.media.get(name="Coniferous_Leaf"),
            ),
            CompartmentService.create(
                name="Leaf_Particle_Coniferous_Forest", volume_element=ve_surfsoil, media=CompartmentService.media.get(name="Coniferous_Leaf_Particle"),
            )]

    elif parcels_data['landUse'] == 'Deciduous Forest':
        new_comps += [
            CompartmentService.create(
                name="Leaf_Deciduous_Forest", volume_element=ve_surfsoil, media=CompartmentService.media.get(name="Deciduous_Leaf"),
            ),
            CompartmentService.create(
                name="Leaf_Particle_Deciduous_Forest", volume_element=ve_surfsoil, media=CompartmentService.media.get(name="Deciduous_Leaf_Particle"),
            )]

    elif parcels_data['landUse'] == 'Grasses/Herbs':
        new_comps += [
            CompartmentService.create(
                name="Leaf_Grasses_Herbs", volume_element=ve_surfsoil, media=CompartmentService.media.get(name="Grass_Leaf"),
            ),
            CompartmentService.create(
                name="Leaf_Particle_Grasses_Herbs", volume_element=ve_surfsoil, media=CompartmentService.media.get(name="Grass_Leaf_Particle"),
            ),
            CompartmentService.create(
                name="Stem_Grasses_Herbs", volume_element=ve_surfsoil, media=CompartmentService.media.get(name="Grass_Stem"),
            ),
            CompartmentService.create(
                name="Root_Grasses_Herbs", volume_element=ve_surfsoil, media=CompartmentService.media.get(name="Grass_Root"),
            )]
        
    elif parcels_data['landUse'] == 'Agriculture (General)':
        new_comps += [
            CompartmentService.create(
                name="Leaf_Agriculture", volume_element=ve_surfsoil, media=CompartmentService.media.get(name="Agriculture_Leaf"),
            ),
            CompartmentService.create(
                name="Leaf_Particle_Agriculture", volume_element=ve_surfsoil, media=CompartmentService.media.get(name="Agriculture_Leaf_Particle"),
            ),
            CompartmentService.create(
                name="Stem_Agriculture", volume_element=ve_surfsoil, media=CompartmentService.media.get(name="Agriculture_Stem"),
            ),
            CompartmentService.create(
                name="Root_Agriculture", volume_element=ve_surfsoil, media=CompartmentService.media.get(name="Agriculture_Root"),
            )]

    # layers and thickness
    surfsoil_thickness = (-1 * Land_Parcel_VolElem_defaults['SurfSoil']['bottom'])
    if parcels_data['landUse'] in ['Tilled Soil', 'Agriculture (General)']:
        surfsoil_thickness = 0.2
    rootsoil_thickness = round(0.8 - surfsoil_thickness, 2)
    update_soil_thickness(p, 'Soil_Surface', 'SurfSoil', surfsoil_thickness)
    update_soil_thickness(p, 'Soil_Root_Zone', 'RootSoil', rootsoil_thickness)

    # reset cover_management_factor (HACKY)
    for param in list(p.scenario.parameters.values()):
        if not isinstance(param, CustomParameter):
            continue
        if not(
            param.variable_name.startswith('erosion3-cover_management_factor')
        ):
            continue
        if not param.requirements == f'(self.id == {p.id})':
            continue
        ParameterService.delete(param, no_commit=True)

    CompartmentService.update(c_surfsoil)
    for nc in new_comps:
        initialize_compartment_custom_parameters(nc)
    CompartmentService.commit()


def init_tillage_default_params(till_media_name):
    #media_id = [m.id for m in CompartmentService.media.get_all() if m.name == till_media_name][0]
    domain_id = [d.id for d in ParameterService.domains.get_all()
                 if d.requirements == f'self.media.isa("{till_media_name}")'][0]
    new_pd_kwargs = SURFACE_SOIL_SPECIFIC_MEDIA_PARAMS
    for i, pd in enumerate(new_pd_kwargs):
        for k, v in pd.items():
            if k == 'domain_id':
                new_pd_kwargs[i]['domain_id'] = domain_id

    init_parameter_definitions(new_pd_kwargs, check_subtypes=True)


def update_tillage_formula_media(till_media_name):
    # REPLACING/APPENDING MEDIA.ID FOR MISSING MEDIA WITH KNOWN/EXISTING PARENT COMPARTMENT IN A FORMULA
    new_media_id = [m.id for m in CompartmentService.media.get_all() if m.name == till_media_name][0]
    old_media_id = [m.id for m in CompartmentService.media.get_all() if m.name == "Surface_Soil"][0]
    fl = {}
    old_id = str(old_media_id)
    new_id = str(new_media_id)
    search_id_regex = r'(media.id\sin\s\{.*\b(' + old_id + r')\b.*\})'
    regex_id_list = re.compile("(?:media\.id\sin\s{([\,\s\d+]+)\})")
    old_id_regex = r'.*\b(' + old_id + r')\b.*'
    new_id_regex = r'.*\b(' + new_id + r')\b.*'
    old_id_replace_regex = r'\b(' + old_id + r')\b'
    for f in FormulaService.get_all():
        if re.search(search_id_regex, f.equation):
            fl[f.id] = []
            old_id_lists = regex_id_list.findall(f.equation)
            for idl in old_id_lists:
                if re.search(old_id_regex, idl) and not re.search(new_id_regex, idl):
                    fl[f.id].append((idl, re.sub(old_id_replace_regex, f'{old_id} , {new_id}', idl)))

    for fid, fv in fl.items():
        f = FormulaService.get(id=fid)
        nf = f.equation
        for ids in fv:
            nf = nf.replace(f'media.id in {{{ids[0]}}}', f'media.id in {{{ids[1]}}}')
        # print(f'old formula: {f.equation}\nnew formula: {nf}\n')
        f.equation = nf
    FormulaService.commit()


def create_new_parameter_defs_for_domain(comp_name):
    domain_id = [d.id for d in CompartmentService.get(name=comp_name).domains if d.requirements][0]
    med_par_defs = [pd for pd in ParameterService.definitions.get_all() if pd.domain_id == domain_id]
    # TODO Complete this for affinity
    pass


# adapted from Samuel's "grid_points_in_polygon_meters" method
def calculate_receptor_grid_points_for_parcel(pcl:Parcel):
    """
    Calculate a rectangular grid of points inside the polygon defined by a parcel's
    vertices and spacing custom parameter.

    Parameters:
        pcl (Parcel): parcel

    Returns:
        None if error; else a dictionary with keys:
            "scenario_id": the scenario id
            "spacing_m": spacing in meters
            "long_lat_pairs": list of lists of floats: Points representing the grid (in EPSG:4326 / WGS84). longitude is first element, latitude is second
                                e.g.:
                                    [
                                        [-85.41157568471587, 44.26498030459199],
                                        .....
                                        [-85.41157568471587, 44.26562360214414]
                                    ]
    """
    try:

        # EPSG:4326 is WGS84, which is what our parcel vertices are based on.
        # Samuel's algorithm switches to 3857 for calculating the grid points
        CRS_FOR_WGS84 = 4326
        CRS_FOR_GRID_CALCS = 3857
        # note -- according to https://github.com/CityScope/CS_choiceModels/issues/4,
        # CRS84 is also equvalent to EPSG:4326

        def get_comp(p:Parcel, kwargs):
            comp = p.get_compartment(**kwargs)

            if kwargs.get("name") and isinstance(comp, list):
                comp = comp[0]

            return comp

        cdv = get_comp(pcl, {"name":"DryVaporSource"})
        spacing_param = cdv.parameters.get("ReceptorSpacing")
        spacing_meters = spacing_param.default_value if type(spacing_param) is ParameterDefinition else spacing_param.value

        if len(pcl.vertices) == 0:
            print(f"WARNING - {pcl} has no defined vertices; returning empty list")
            return None

        # Load it into a GeoDataFrame so we can change coordinate systems using gdf.to_crs
        gdf = gpd.GeoDataFrame((Polygon(pcl.vertices),), columns=['geometry'], crs=CRS_FOR_WGS84)
        # (this dataframe is a single row with a single column; geometry contains all the points

        # Project to a CRS in meters (Web Mercator here; you could also use UTM for better accuracy)
        gdf_proj = gdf.to_crs(epsg=CRS_FOR_GRID_CALCS)
        polygon = gdf_proj.geometry[0]
        prep_poly = prep(polygon)

        # Get bounding box in projected meters
        min_x, min_y, max_x, max_y = polygon.bounds
        x_coords = np.arange(min_x, max_x + spacing_meters, spacing_meters)
        y_coords = np.arange(min_y, max_y + spacing_meters, spacing_meters)

        # Generate grid
        points_inside = []
        for x in x_coords:
            for y in y_coords:
                pt = Point(x, y)
                if prep_poly.contains(pt):
                    points_inside.append(pt)

        # Convert list of Points to GeoDataFrame in EPSG:3857, then reproject back to EPSG:4326
        points_gdf = gpd.GeoDataFrame(geometry=points_inside, crs=f"EPSG:{CRS_FOR_GRID_CALCS}")
        # return points_gdf.to_crs(epsg=CRS_FOR_WGS84)
        converted_points = points_gdf.to_crs(epsg=CRS_FOR_WGS84)

        simple_list_of_longs_and_lats = []
        for row in converted_points.itertuples():
            simple_pt = [[x[0], x[1]] for x in row.geometry.coords][0]
            simple_list_of_longs_and_lats.append(simple_pt)

        return {
            "parcel_id": pcl.id,
            "spacing_m": spacing_meters,
            "long_lat_pairs": simple_list_of_longs_and_lats
        }
    except Exception as e:
        print(f"ERROR calculating grid points for parcel {pcl}: {e}")
        return None

# this is an adapted version of Samuel's "geojson_to_aermod_receptors" function; minor
# changes made to help it work within TRIM app
def geojson_to_aermod_receptors(geojson_contents, utm_zone=None, northern_hemisphere=True):
    """
    Converts GeoJSON points to AERMOD receptor file format.

    Parameters:
    - geojson_contents: str containing GeoJSON
    - utm_zone: int, UTM zone number
    - northern_hemisphere: bool, True if northern hemisphere, False for southern

    Output:
    - AERMOD receptor file text (to be written to a file, returned to client, etc.)
    """
    # Set up transformer for lat/lon -> UTM
    proj_str = f"+proj=utm +zone={utm_zone} +datum=WGS84 +units=m +no_defs"
    if not northern_hemisphere:
        proj_str += " +south"
    transformer = Transformer.from_crs("EPSG:4326", proj_str, always_xy=True)

    # Read GeoJSON
    parsed_geojson = json.loads(geojson_contents)

    receptors = []

    # Extract coordinates
    for feature in parsed_geojson['features']:
        geom = feature['geometry']
        if geom['type'] == 'Point':
            lon, lat = geom['coordinates']
            x, y = transformer.transform(lon, lat)
            receptors.append((x, y))
        else:
            print(f"Skipping non-point geometry: {geom['type']}")

    # generate output
    aermod_format = ""
    for idx, (x, y) in enumerate(receptors, start=1):
        aermod_format += f"RE DISCCART {x:.2f} {y:.2f} 0.0\n"
    aermod_format += "END\n"

    return aermod_format
