import re, json
import numpy as np
from copy import deepcopy
from pprint import pprint
from ..scenarios.utils import init_parameter_definitions
from ..scenarios.defaults import get_surface_runoff
from .defaults import SURFACE_SOIL_SPECIFIC_MEDIA_PARAMS

from flask_api import ApiResult

from trim_db.schema import CustomParameter, ParameterDefinition, Parcel
from trim_db.services import ChemicalService, CompartmentService, FormulaService, ParameterService, ParcelService, ScenarioService, VolumeElementService
from trim_db.services.parameters import get_or_create_custom_param, update_custom_param_value
from .defaults import Air_Parcel_VolElem_defaults, Aquatic_Biota_SW_Compartment_defaults, Aquatic_Biota_Sed_Compartment_defaults, Farm_Biota_SurfSoil_Compartment_defaults, LAND_USE_TYPES, AQUATIC_DIET, Land_Parcel_VolElem_defaults, Water_Parcel_VolElem_defaults, Wet_Dry_Source_VolElem_defaults
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

    Air_params = [('dustLoad', "DustLoad"),
                  ("dustDensity", "DustDensity"),
                  ("airDensity", "AirDensity"),
                  ("fractionOrganicMatterOnParticulates", "FractionOrganicMatteronParticulates")]

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

    if field_name == "landUse":
        if parcels_data['landUse'] in ['Coniferous Forest', 'Deciduous Forest', 'Agriculture (General)',
                                       'Grasses/Herbs', 'Tilled Soil', 'Untilled Soil', 'Impervious']:
            # COMPARTMENT CHANGE
            if not parcels_data['landUse'] == land_use:
                print(f'NEW LAND USE DETECTED {land_use} >> {parcels_data["landUse"]}')
                create_base_land_compartments(parcels_data, p, land_use)
        if parcels_data['landUse'] not in ['Tilled Soil', 'Untilled Soil']:
            ve = p.get_volume_element("SurfSoil")
            if ve:
                if ve.get_compartment("Farm"):
                    cmp = ve.get_compartment("Farm")
                    CompartmentService.delete(cmp, False)
        if parcels_data['landUse'] in ['Impervious']:
            ve = p.get_volume_element("SurfSoil")
            if ve:
                if ve.get_compartment("Wetland"):
                    cmp = ve.get_compartment("Wetland")
                    CompartmentService.delete(cmp, False)

    if field_name == "hasFarmFoodChain":
        biotic_ve = deepcopy(Land_Parcel_VolElem_defaults)
        biotic_ve["SurfSoil"]["Compartments"] = deepcopy(Farm_Biota_SurfSoil_Compartment_defaults["Compartments"])
        if parcels_data['hasFarmFoodChain'] == "Yes":
            surfsoil = p.get_volume_element("SurfSoil")
            if surfsoil:
                initialize_parcel_contents(p, biotic_ve)
            else:
                raise ValueError("Cannot create or get Farm Compartment")
        if parcels_data['hasFarmFoodChain'] == "No":
            for vek, vev in biotic_ve.items():
                ve = p.get_volume_element(vek)
                if ve:
                    for k, v in biotic_ve[vek]["Compartments"].items():
                        cmp = ve.get_compartment(v["name"])
                        if cmp:
                            logger.info(f"Deleted {cmp.name}")
                            CompartmentService.delete(cmp, False)
    if field_name == "hasFishFoodWeb":
        biotic_ve = deepcopy(Water_Parcel_VolElem_defaults)
        biotic_ve["Sed"]["Compartments"] = deepcopy(Aquatic_Biota_Sed_Compartment_defaults["Compartments"])
        biotic_ve["SW"]["Compartments"] = deepcopy(Aquatic_Biota_SW_Compartment_defaults["Compartments"])
        if parcels_data['hasFishFoodWeb'] == "Yes":
            sw = p.get_volume_element("SW")
            if sw:
                initialize_parcel_contents(p, biotic_ve)
                init_diet_table_custom_parameters(p)
            else:
                raise ValueError("Cannot create or get Fish Compartment")
        if parcels_data['hasFishFoodWeb'] == "No":
            for vek, vev in biotic_ve.items():
                ve = p.get_volume_element(vek)
                if ve:
                    for k, v in biotic_ve[vek]["Compartments"].items():
                        cmp = ve.get_compartment(v["name"])
                        if cmp:
                            logger.info(f"Deleted {cmp.name}")
                            CompartmentService.delete(cmp, False)
    if field_name == "hasWetland":
        if parcels_data['hasWetland'] == "Yes":
            ve = p.get_volume_element("SurfSoil")
            if ve:
                m = CompartmentService.media.get(name='Wetland')
                c = CompartmentService.get_or_create(name="Wetland", volume_element=ve, media=m)
            else:
                raise ValueError("Cannot create or get Wetland Compartment")
        if parcels_data['hasWetland'] == "No":
            ve = p.get_volume_element("SurfSoil")
            if ve:
                cmp = ve.get_compartment("Wetland")
                if cmp:
                    CompartmentService.delete(cmp, False)
    if field_name == "description":
        p.description = parcels_data['description']
    if field_name == 'totalErosionRate':
        for c in p.compartments:
            if c.media.isa('Surface_Soil'):
                par = c.parameters.get('TotalErosionRate')
                par.value = parcels_data['totalErosionRate']
    if "erosion1" in field_name or "erosion2" in field_name or "erosion3" in field_name: # unique structure
        param = ParameterService.definitions.get(full_name=field_name)
        param = ParameterService.get_or_create(
            definition_id=param.id,
            scenario_id=p.scenario_id,
            requirements=f"(self.id == {p.id})", # parcel id
        )
        # storing in unit since value is decimal only
        param.unit = parcels_data[field_name]
        ParameterService.update(param)
        ParameterService.commit()
    if field_name in [k for k, v in Air_params]:
        par_name = [v for k, v in Air_params if k == field_name][0]
        # the below part was generating error due to missing par for dustLoad, dustDensity etc...
        cmp = [c for c in p.compartments if "Air in Air_" in c.standard_name][0]
        par = get_or_create_custom_param(
            cmp.parameters.get(par_name),
            {"requirements": f"(self.id == {cmp.id})", "scenario_id": p.scenario_id},
        )
        update_custom_param_value(par, parcels_data[field_name])
        ParameterService.commit()
    # Note that 0 is the fixed datum for volume element boundary locations
    if field_name == "airHeight":
        for co in p.compartments:
            if co.name == "Air":
                co.volume_element.top = parcels_data['airHeight']

    if field_name == "surfaceSoilThickness":
        thickness_before = p.get_compartment("Soil_Surface").volume_element.height.magnitude
        p.get_compartment("Soil_Surface").volume_element.bottom = \
            p.get_compartment("Soil_Surface").volume_element.top + \
            (-1 * float(parcels_data['surfaceSoilThickness']))
        thickness_now = p.get_compartment("Soil_Surface").volume_element.height.magnitude
        delta_thickness = thickness_now - thickness_before
        for soil_comp in ["Soil_Root_Zone", "Soil_Vadose_Zone", "Groundwater", "DryVaporSource", "WetVaporSource",
                          "DryParticleSource", "WetParticleSource"]:
            p.get_compartment(soil_comp).volume_element.top = \
                (-1 * delta_thickness) + p.get_compartment(soil_comp).volume_element.top
            p.get_compartment(soil_comp).volume_element.bottom = \
                (-1 * delta_thickness) + p.get_compartment(soil_comp).volume_element.bottom
    if field_name == "rootSoilThickness":
        thickness_before = p.get_compartment("Soil_Root_Zone").volume_element.height
        p.get_compartment("Soil_Root_Zone").volume_element.bottom = \
            p.get_compartment("Soil_Root_Zone").volume_element.top + \
            (-1 * float(parcels_data['rootSoilThickness']))
        thickness_now = p.get_compartment("Soil_Root_Zone").volume_element.height
        delta_thickness = thickness_now.magnitude - thickness_before.magnitude
        for soil_comp in ["Soil_Vadose_Zone", "Groundwater", "DryVaporSource", "WetVaporSource",
                          "DryParticleSource", "WetParticleSource"]:
            p.get_compartment(soil_comp).volume_element.top = \
                (-1 * delta_thickness) + p.get_compartment(soil_comp).volume_element.top
            p.get_compartment(soil_comp).volume_element.bottom = \
                (-1 * delta_thickness) + p.get_compartment(soil_comp).volume_element.bottom
    if field_name == "vadoseSoilThickness":
        thickness_before = p.get_compartment("Soil_Vadose_Zone").volume_element.height
        p.get_compartment("Soil_Vadose_Zone").volume_element.bottom = \
            p.get_compartment("Soil_Vadose_Zone").volume_element.top + \
            (-1 * float(parcels_data['vadoseSoilThickness']))
        thickness_now = p.get_compartment("Soil_Vadose_Zone").volume_element.height
        delta_thickness = thickness_now.magnitude - thickness_before.magnitude
        for soil_comp in ["Groundwater", "DryVaporSource", "WetVaporSource",
                          "DryParticleSource", "WetParticleSource"]:
            p.get_compartment(soil_comp).volume_element.top = \
                (-1 * delta_thickness) + p.get_compartment(soil_comp).volume_element.top
            p.get_compartment(soil_comp).volume_element.bottom = \
                (-1 * delta_thickness) + p.get_compartment(soil_comp).volume_element.bottom
    if field_name == "groundwaterZoneSoilThick":
        thickness_before = p.get_compartment("Groundwater").volume_element.height
        p.get_compartment("Groundwater").volume_element.bottom = \
            p.get_compartment("Groundwater").volume_element.top + \
            (-1 * float(parcels_data['groundwaterZoneSoilThick']))
        thickness_now = p.get_compartment("Groundwater").volume_element.height
        delta_thickness = thickness_now.magnitude - thickness_before.magnitude
        for soil_comp in ["DryVaporSource", "WetVaporSource",
                          "DryParticleSource", "WetParticleSource"]:
            p.get_compartment(soil_comp).volume_element.top = \
                (-1 * delta_thickness) + p.get_compartment(soil_comp).volume_element.top
            p.get_compartment(soil_comp).volume_element.bottom = \
                (-1 * delta_thickness) + p.get_compartment(soil_comp).volume_element.bottom
    if field_name == "tillage":
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

    if field_name in ["EvapotranspirationFractions", "GroundwaterSeepageFractions", "RunoffFractions"]:
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
        par_name_map = {"RunoffFractions": "PrecipitationRunoffFraction",
                       "GroundwaterSeepageFractions": "GroundwaterSeepageFraction",
                       "EvapotranspirationFractions": "EvapotranspirationFraction"}
        # for par_name, par_val in {"TotalRunoffRate": total_runoff_val, "GroundwaterSeepageFraction": seepage_frac_val,
        #                           "EvapotranspirationFraction": evapotranspiration_frac_val}.items():
        par_name = par_name_map[field_name]
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
            total_runoff_val = frac_val * p.scenario.Rain.magnitude  # was multiplied by watershed area but removed per Arun on 08/12/2024
            par_name = "TotalRunoffRate"
            par_val = total_runoff_val
            par = get_or_create_custom_param(
                soil_comp.parameters.get(par_name),
                {
                    "requirements": f"(self.id == {soil_comp.id})",
                    "scenario_id": p.scenario.id,
                },
                no_commit=True
            )
            update_custom_param_value(par, par_val)

    if field_name in ['flush_rate', 'suspended_sed_conc', 'algae_density', 'chloride_conc', 'chlorophyll_conc',
                      'mean_depth', 'evaporation_rate', 'suspended_organic_carbon', 'water_ph',
                      'sed_deposition_vel', 'water_temp', 'sed_inflow']:
        par_name = {'flush_rate': "Flushes",
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
                    'sed_inflow': "ExternalSedimentInflow"}
        comp = p.get_compartment("Surface_water")
        par = comp.parameters.get(par_name[field_name])
        if par:
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
                       pp.full_name == par_name[field_name]]
            comp.parameters.add(par_name[field_name], domain_name="Compartment", unit=par_obj[0].default_unit)
            comp.parameters.get(par_name[field_name]).value = parcels_data[field_name]
            comp.parameters.get(par_name[field_name]).scenario_id = p.scenario_id

    if field_name in ['bed_density', 'organic_carbon_frac', 'bed_pH', 'bed_porosity', 'bed_thickness']:
        par_name = {'bed_density': 'BedDensity',
                    'organic_carbon_frac': "OrganicCarbonContent",
                    'bed_pH': "pH",
                    'bed_porosity': "Porosity",
                    'bed_thickness': "MeanThickness"}
        comp = p.get_compartment("Sediment")
        par = comp.parameters.get(par_name[field_name])
        if par:
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
                       pp.full_name == par_name[field_name]]
            comp.parameters.add(par_name[field_name], domain_name="Compartment", unit=par_obj[0].default_unit)
            comp.parameters.get(par_name[field_name]).value = parcels_data[field_name]
            comp.parameters.get(par_name[field_name]).scenario_id = p.scenario_id

    if field_name in ["Zooplankton", "FishHerbivore", "FishBenthicOmnivore", "FishOmnivore",
                      "FishBenthicCarnivore", "FishCarnivore"]:
        comp_name = {"Zooplankton": "Zooplankton",
                     "FishHerbivore": "Water_Column_Herbivore",
                     "FishBenthicOmnivore": "Benthic_Omnivore",
                     "FishOmnivore": "Water_Column_Omnivore",
                     "FishBenthicCarnivore": "Benthic_Carnivore",
                     "FishCarnivore": "Water_Column_Carnivore"
                     }
        params = [pd for pd in parcels_data.keys() if pd not in ["id", "field", "csrf_token"]]
        # print(f"{field_name} {[c for c in p.compartments if c.name == comp_name[field_name]]}")
        this_comp = [c for c in p.compartments if c.name == comp_name[field_name]][0]
        for param in params:
            this_par = get_or_create_custom_param(
                this_comp.parameters[param],
                {"requirements": f"(self.id == {this_comp.id})", "scenario_id": p.scenario_id},
                no_commit=True
            )
            update_custom_param_value(this_par, parcels_data[param])
        ParameterService.commit()

    if field_name in ["BenthicCarnivoreBiomass", "BenthicInvertebrateBiomass", "BenthicOmnivoreBiomass",
                      "MacrophyteBiomass", "WaterColumnCarnivoreBiomass", "WaterColumnHerbivoreBiomass",
                      "WaterColumnOmnivoreBiomass", "ZooplanktonBiomass", "BenthicCarnivoreWeight",
                      "BenthicInvertebrateWeight", "BenthicOmnivoreWeight",
                      "WaterColumnCarnivoreWeight", "WaterColumnHerbivoreWeight", "WaterColumnOmnivoreWeight",
                      "ZooplanktonWeight"]:
        comp_name = {
            "BenthicCarnivore": "Benthic_Carnivore",
            "BenthicInvertebrate": "Benthic_Invertebrate",
            "BenthicOmnivore": "Benthic_Omnivore",
            "Macrophyte": "Macrophyte",
            "WaterColumnCarnivore": "Water_Column_Carnivore",
            "WaterColumnHerbivore": "Water_Column_Herbivore",
            "WaterColumnOmnivore": "Water_Column_Omnivore",
            "Zooplankton": "Zooplankton"
        }
        if "Biomass" in field_name:
            base_name = field_name.replace("Biomass", "")
            prop = "BiomassPerArea"
        elif "Weight" in field_name:
            base_name = field_name.replace("Weight", "")
            prop = "BW"

        for this_comp in p.compartments:
            if this_comp.name == comp_name[base_name]:
                this_param = get_or_create_custom_param(
                    this_comp.parameters.get(prop),
                    {"requirements": f"(self.id == {this_comp.id})", "scenario_id": p.scenario_id},
                    no_commit=True
                )
                update_custom_param_value(this_param, float(parcels_data[field_name]))
        ParameterService.commit()

    if field_name in ["pH", "rho", "AverageVerticalVelocity", "FractionSand", "OrganicCarbonContent",
                      "VolumeFraction_Liquid", "VolumeFraction_Vapor", "Porosity", "AirSoilBoundaryThickness",
                      "FractionofAreaAvailableforErosion", "FractionofAreaAvailableforRunoff",
                      "FractionofAreaAvailableforVerticalDiffusion", "TotalRunoffRate"]:
        this_comp = p.get_compartment(name=parcels_data["comp_name"])
        this_par = get_or_create_custom_param(
            this_comp.parameters.get(parcels_data["field"]),
            {"requirements": f"(self.id == {this_comp.id})", "scenario_id": p.scenario_id},
        )
        update_custom_param_value(this_par, float(parcels_data[field_name]))
    if field_name == "emission":
        src_comp = [c for c in p.compartments if c.name == parcels_data["compartment_name"]][0]
        src_par = [par for parn, par in src_comp.parameters.items() if parn == "surfaceDepositionRate"]
        chem = ChemicalService.get(name=parcels_data["chemical_name"])
        if len(src_par) > 0:
            src_par = get_or_create_custom_param(
                src_par[0],
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
    if field_name == "runoff_matrix_value":
        scn = ScenarioService.get(id=p.scenario.id)
        sender_parcel_name = parcels_data["sender"].replace("ro_", "")
        receivers = parcels_data["receiver"].split(",")
        values = parcels_data["ro_value"].split(",")
        sp = scn.parcels.where(Parcel.name == sender_parcel_name).first()
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
                    rp = scn.parcels.where(Parcel.name == receiver_name).first()
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
        nve = new_parcel.get_volume_element(ve_name)
        if not nve:
            nve = VolumeElementService.get_or_create(name=ve_name,
                                                     parcel=new_parcel,
                                                     top=ve["top"],
                                                     bottom=ve["bottom"])
        for c_name, c in ve["Compartments"].items():
            # Create standard compartments linking them to default volume elements and media for each compartment
            nc = new_parcel.get_compartment(c_name)
            if not nc:
                this_media = CompartmentService.media.get(name = c["media_name"])
                nc = CompartmentService.get_or_create(name=c_name,
                                                      volume_element=nve,
                                                      media=this_media)
            initialize_compartment_custom_parameters(nc)
    ParameterService.commit()


# This is for parameters of new compartments whose default value cannot be used and will need custom parameters defined
# at the time of creation of new compartment.
def initialize_compartment_custom_parameters(nc):
    # Add in custom parameters for new compartments using the self.id = <id of new compartment>
    this_parcel = nc.volume_element.parcel
    if nc.name == "Soil_Surface":
        # Default Total Erosion Rate
        ter_val = calc_default_erosion_rate_sdr(this_parcel)
        add_compartment_custom_parameters(nc, "TotalErosionRate", ter_val, "kg/m^2/day")
        # add Total Runoff Rate
        # using Groundwater seepage fraction and precipitation to calculate runoff
        trr_val = (1 - nc.GroundwaterSeepageFraction) * (nc.volume_element.parcel.scenario.Rain).magnitude
        add_compartment_custom_parameters(nc, "TotalRunoffRate", trr_val, "m^3/m^2/day")

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

    # elif nc.name == "Surface_water" or nc.name == "Sediment":


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
    for c in pcl.compartments:
        if not c.media.isa("Surface_Soil"):
            continue
        unit_soil_loss = c.parameters["unitSoilLoss"].default_value
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
        slope_coef = c.parameters["sedimentDeliveryRatioSlopeCoef"].default_value
        sed_delivery_ratio = intercept_coef * (pcl.area ** (-1 * slope_coef))
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


def delete_parcel_contents(del_parcel):
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

        # THIS IS A TERRIBLE WAY TO DELETE A CUSTOM PARAMETER!!! self.id may be for a different domain
        #  and it will be deleted!!!
        # custom_params = ParameterService.get_all(requirements=f'(self.id == {comp_id})')
        # for cp in custom_params:
        #     ParameterService.delete(cp, False)

        # This is much better!
        custom_params = [cp for _, cp in c.parameters.items() if isinstance(cp, CustomParameter)]
        for cp in custom_params:
            ParameterService.delete(cp, False)

        # Delete Compartments
        CompartmentService.delete(c, False)
        # Delete compartment id from formulas with custom values for give compartment (from legacy Trim)
        formulas = ["MethylationRate", "DemethylationRate", "ReductionRate"]
        for t in formulas:
            ins = ParameterService.definitions.get(variable_name=t).instances
            par = [i for i in ins if i.scenario.id == scenario_id]
            if not par:
                continue
            par = par[0]
            eq = par.formula.equation
            del_id = c.id
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
            ParameterService.commit()
    # Delete Volume Elements
    for ve in del_parcel.volume_elements:
        VolumeElementService.delete(ve, False)


# Some parameters just not have any default values or any values to be referenced at the time of the
# initialization/creation of the entity (i.e. compartment). In these cases we can get the default values from
# the relevant flask form template (json) from the frontend.
def get_default_value_from_json_form(form_name, parameter_name):
    json_forms = {
        'Abiotic_Air': ScenarioAbioticPropertiesForm.__getattribute__(ScenarioAbioticPropertiesForm, "AirAbioticTable"),
        'Abiotic_Surface_Soil': ScenarioAbioticPropertiesForm.__getattribute__(ScenarioAbioticPropertiesForm, "SurfaceSoilAbioticTable"),
        'Abiotic_Tilled_Soil': ScenarioAbioticPropertiesForm.__getattribute__(ScenarioAbioticPropertiesForm, "SurfaceSoilAbioticTable"),
        'Abiotic_Root_Zone': ScenarioAbioticPropertiesForm.__getattribute__(ScenarioAbioticPropertiesForm, "RootSoilAbioticTable"),
        'Abiotic_Vadose_Zone': ScenarioAbioticPropertiesForm.__getattribute__(ScenarioAbioticPropertiesForm, "VadoseSoilAbioticTable"),
        'Abiotic_Groundwater': ScenarioAbioticPropertiesForm.__getattribute__(ScenarioAbioticPropertiesForm, "GWSoilAbioticTable")
    }
    form_obj = json_forms[form_name]
    form_class = form_obj.kwargs['form_class']
    def_val = form_class.__getattribute__(form_class, parameter_name).kwargs["default"]
    return def_val


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
        c_surfsoil.media_id = [m.id for m in CompartmentService.media.get_all() if m.name == "Tilled_Soil"][0]
        init_tillage_default_params('Tilled_Soil')
        update_tillage_formula_media('Tilled_Soil')
        c_surfsoil.soilTillage = 1
        thickness_before = c_surfsoil.volume_element.height.magnitude
        c_surfsoil.volume_element.bottom = c_surfsoil.volume_element.top - 0.20
        thickness_now = abs(c_surfsoil.volume_element.bottom - c_surfsoil.volume_element.top)
        delta_thickness = thickness_now - thickness_before
        for soil_comp in ["Soil_Root_Zone", "Soil_Vadose_Zone", "Groundwater", "DryVaporSource", "WetVaporSource",
                          "DryParticleSource", "WetParticleSource"]:
            p.get_compartment(soil_comp).volume_element.top = \
                (-1 * delta_thickness) + p.get_compartment(soil_comp).volume_element.top
            p.get_compartment(soil_comp).volume_element.bottom = \
                (-1 * delta_thickness) + p.get_compartment(soil_comp).volume_element.bottom
            print(f"New top/bottom for {soil_comp}:\ntop: {p.get_compartment(soil_comp).volume_element.top}"
                  f" bottom: {p.get_compartment(soil_comp).volume_element.bottom}")
    elif parcels_data['landUse'] == 'Untilled Soil':
        c_surfsoil.media_id = [m.id for m in CompartmentService.media.get_all() if m.name == "Untilled_Soil"][0]
        init_tillage_default_params('Untilled_Soil')
        update_tillage_formula_media('Untilled_Soil')
        c_surfsoil.soilTillage = 0
        thickness_before = c_surfsoil.volume_element.height.magnitude
        c_surfsoil.volume_element.bottom = c_surfsoil.volume_element.top - 0.01
        thickness_now = abs(c_surfsoil.volume_element.bottom - c_surfsoil.volume_element.top)
        delta_thickness = thickness_now - thickness_before
        for soil_comp in ["Soil_Root_Zone", "Soil_Vadose_Zone", "Groundwater", "DryVaporSource", "WetVaporSource",
                          "DryParticleSource", "WetParticleSource"]:
            p.get_compartment(soil_comp).volume_element.top = \
                (-1 * delta_thickness) + p.get_compartment(soil_comp).volume_element.top
            p.get_compartment(soil_comp).volume_element.bottom = \
                (-1 * delta_thickness) + p.get_compartment(soil_comp).volume_element.bottom
            print(f"New top/bottom for {soil_comp}:\ntop: {p.get_compartment(soil_comp).volume_element.top}"
                  f" bottom: {p.get_compartment(soil_comp).volume_element.bottom}")
    elif parcels_data['landUse'] == 'Impervious':
        c_surfsoil.media_id = [m.id for m in CompartmentService.media.get_all() if m.name == "Impervious"][0]
        custom_param_erosion.value = 0
    elif parcels_data['landUse'] == 'Coniferous Forest':
        new_comps.append(CompartmentService.create(name="Leaf_Coniferous_Forest", volume_element=ve_surfsoil,
                                                   media=[m for m in CompartmentService.media.get_all() if m.isa('Coniferous_Leaf')][0]))
        new_comps.append(CompartmentService.create(name="Leaf_Particle_Coniferous_Forest", volume_element=ve_surfsoil,
                                                   media=[m for m in CompartmentService.media.get_all() if m.isa('Coniferous_Leaf_Particle')][0]))
    elif parcels_data['landUse'] == 'Deciduous Forest':
        new_comps.append(CompartmentService.create(name="Leaf_Deciduous_Forest", volume_element=ve_surfsoil,
                                                   media=[m for m in CompartmentService.media.get_all() if m.isa('Deciduous_Leaf')][0]))
        new_comps.append(CompartmentService.create(name="Leaf_Particle_Deciduous_Forest", volume_element=ve_surfsoil,
                                                   media=[m for m in CompartmentService.media.get_all() if m.isa('Deciduous_Leaf_Particle')][0]))
    elif parcels_data['landUse'] == 'Grasses/Herbs':
        new_comps.append(CompartmentService.create(name="Leaf_Grasses_Herbs", volume_element=ve_surfsoil,
                                                   media=[m for m in CompartmentService.media.get_all() if m.isa('Grass_Leaf')][0]))
        new_comps.append(CompartmentService.create(name="Leaf_Particle_Grasses_Herbs", volume_element=ve_surfsoil,
                                                   media=[m for m in CompartmentService.media.get_all() if m.isa('Grass_Leaf_Particle')][0]))
        new_comps.append(CompartmentService.create(name="Stem_Grasses_Herbs", volume_element=ve_surfsoil,
                                                   media=[m for m in CompartmentService.media.get_all() if m.isa('Grass_Stem')][0]))
        new_comps.append(CompartmentService.create(name="Root_Grasses_Herbs", volume_element=ve_surfsoil,
                                                   media=[m for m in CompartmentService.media.get_all() if m.isa('Grass_Root')][0]))
    elif parcels_data['landUse'] == 'Agriculture (General)':
        new_comps.append(CompartmentService.create(name="Leaf_Agriculture", volume_element=ve_surfsoil,
                                                   media=[m for m in CompartmentService.media.get_all() if m.isa('Agriculture_Leaf')][0]))
        new_comps.append(CompartmentService.create(name="Leaf_Particle_Agriculture", volume_element=ve_surfsoil,
                                                   media=[m for m in CompartmentService.media.get_all() if m.isa('Agriculture_Leaf_Particle')][0]))
        new_comps.append(CompartmentService.create(name="Stem_Agriculture", volume_element=ve_surfsoil,
                                                   media=[m for m in CompartmentService.media.get_all() if m.isa('Agriculture_Stem')][0]))
        new_comps.append(CompartmentService.create(name="Root_Agriculture", volume_element=ve_surfsoil,
                                                   media=[m for m in CompartmentService.media.get_all() if m.isa('Agriculture_Root')][0]))
    CompartmentService.update(c_surfsoil)
    for nc in new_comps:
        initialize_compartment_custom_parameters(nc)
    CompartmentService.commit()


def init_tillage_default_params(till_media_name):
    media_id = [m.id for m in CompartmentService.media.get_all() if m.name == till_media_name][0]
    domain_id = [d.id for d in ParameterService.domains.get_all()
                 if d.requirements == f'self.media_id == {media_id}'][0]
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
        print(f'old formula: {f.equation}\nnew formula: {nf}\n')
        f.equation = nf
    FormulaService.commit()


def create_new_parameter_defs_for_domain(comp_name):
    domain_id = [d.id for d in CompartmentService.get(name=comp_name).domains if d.requirements][0]
    med_par_defs = [pd for pd in ParameterService.definitions.get_all() if pd.domain_id == domain_id]
    # TODO Complete this for affinity
    pass


def compute_watershed_areas(runoff_matrix, area_parcels):
    # function to compute watershed areas by markov chain estimation. Only works if lakes runoff 100% to themselves.
    # Land parcel do not have watersheds and will tend to zero but lake parcel watersheds will be accurate.
    # runoff_matrix is a square nxn matrix that must not include sinks and must include lakes in both rows and columns.
    # Lakes must run off 100% to themselves. n is a large number like 200 or 300 that will enable the markov chain to
    # reach steady state. area_parcels is a single matrix with areas of all parcels in the same order as the rows/cols
    # of the runoff_matrix.
    # Note: the transpose is required because of the arrangement of the matrix such that row are senders and cols are
    # receivers. When multiplying by area matrix to estimate watershed, the rows must be receivers, so transpose.
    m = np.matrix(runoff_matrix)  # convert to np matrix

    # raise M to a large number (markov chain estimation of probabilities of endpoint of flow)
    m_n = np.linalg.matrix_power(m, 500)

    m_n_t = m_n.T  # transpose of M_n so that it can be multiplied as a dot product with

    runoff_areas = m_n_t @ area_parcels  # this is the dot product

    return runoff_areas


def get_watershed_area(pcl):
    # Compute watershed area using Markoff chain approach
    # 1. get runoff fractions matrix (rom) and parcel areas as vector (pav)
    ro_array = get_surface_runoff(pcl.scenario)
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
    wsa_matrix = compute_watershed_areas(rom, pav)
    # 3. get the watershed area specific to this surface water parcel
    pcl_watershed = wsa_matrix[pcl_names.index(pcl.name)]
    return pcl_watershed[0, 0]
