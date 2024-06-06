from flask import Blueprint, request, render_template
from flask_security import login_required
from flask_api import ApiResult,  ApiException
from trim_db.services import *
from trim_frontend import api
from .defaults import *
from .forms import *
from ..utils.logging import make_logger

import traceback
import re
import json
import time

parcels_api = Blueprint('parcels_api', __name__)
api.use_api_errors(parcels_api)


@parcels_api.route(
    '/api/scenario/<int:scenario_id>/parcel', methods=['POST']
)
@login_required
def create_parcel(scenario_id):
    s = ScenarioService.get(scenario_id)
    if not s:
        raise ApiException("Unknown Scenario")

    logger = make_logger('parcels_api_create')
    # form = ScenarioParcelsForm()
    try:
        parcels_data = request.form.to_dict()
        # if not parcels_data:
        #    raise ApiException("No parcels defined")

        # Create a new parcel with the form data
        p = ParcelService.create(no_commit=True)
        # form.populate_obj(p)

        if not parcels_data['name']:
            raise AssertionError("Parcel name cannot be blank.")

        p.name = parcels_data['name']
        p.description = parcels_data['desc']
        p.scenario_id = scenario_id
        p.vertices = json.loads(parcels_data['geom'])

        # Save the scenario
        ParcelService.commit()
        # Add default compartments, media and parameters
        initialize_parcel_contents(p)
        media = LAND_USE_TYPES
    except Exception as e:
        logger.error(traceback.format_exc())

    return ApiResult({'scenario': p.as_serializable(), 'media': media})


@parcels_api.route(
    '/api/scenario/<int:scenario_id>/parcel', methods=['GET']
)
@login_required
def get_parcels(scenario_id):
    logger = make_logger('parcels_api_get')
    try:
        s = ScenarioService.get(scenario_id)
        if not s:
            raise ApiException("Unknown Scenario")
        p = ParcelService.get_all(scenario_id=scenario_id)
        m = LAND_USE_TYPES
        parcels = []
        media = m

        if p is not None:
            sh = s.as_serializable()
            total_start = time.time()
            for this_p in p:
                start_time = time.time()
                parcels.append(this_p.as_serializable())
                logger.info(f"Acquired parcel {this_p.name} in {time.time() - start_time} seconds")
            logger.info(f"Acquired all parcels in {time.time() - total_start} seconds")
    except Exception as e:
        logger.error(traceback.format_exc())

    sh["runoff_matrix"] = get_surface_runoff(scenario_id)

    return ApiResult({'scenario_head': sh, 'scenario': parcels, 'media': media})


@parcels_api.route(
    '/api/scenario/<int:scenario_id>/parcel/<int:id>/update', methods=['POST']
)
@login_required
def update_parcel(id, scenario_id):
    logger = make_logger('parcels_api_update')
    try:
        # Get the specified parcel
        p = ParcelService.get(id)
        parcels_data = request.form.to_dict()

        land_use = get_land_use(p)

        Air_params = [('dustLoad', "DustLoad"),
                      ("dustDensity", "DustDensity"),
                      ("airDensity", "AirDensity"),
                      ("fractionOrganicMatterOnParticulates", "FractionOrganicMatterOnParticulates")]

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
                land_and_air_parcel_vol_elem_defaults = dict(Land_Parcel_VolElem_defaults)
                land_and_air_parcel_vol_elem_defaults.update(Air_Parcel_VolElem_defaults)
                # add standard Land & Air Volume element and compartments
                initialize_parcel_contents(p, land_and_air_parcel_vol_elem_defaults)
            if parcels_data['parcelType'] == "Water & Air":
                # concat Water and Air defaults
                water_and_air_parcel_vol_elem_defaults = dict(Water_Parcel_VolElem_defaults)
                water_and_air_parcel_vol_elem_defaults.update(Air_Parcel_VolElem_defaults)
                # add standard Water & Air Volume element and compartments
                initialize_parcel_contents(p, water_and_air_parcel_vol_elem_defaults)

        if field_name == "landUse":
            if parcels_data['landUse'] in ['Coniferous Forest', 'Deciduous Forest', 'Agriculture - General',
                                           'Grasses/Herbs', 'Tilled Soil', 'Untilled Soil', 'Impervious']:
                # COMPARTMENT CHANGE
                if not parcels_data['landUse'] == land_use:
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
            biotic_ve = dict(Land_Parcel_VolElem_defaults)
            biotic_ve["SurfSoil"]["Compartments"] = dict(Farm_Biota_SurfSoil_Compartment_defaults["Compartments"])
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
            biotic_ve = dict(Water_Parcel_VolElem_defaults)
            biotic_ve["Sed"]["Compartments"] = dict(Aquatic_Biota_Sed_Compartment_defaults["Compartments"])
            biotic_ve["SW"]["Compartments"] = dict(Aquatic_Biota_SW_Compartment_defaults["Compartments"])
            if parcels_data['hasFishFoodWeb'] == "Yes":
                sw = p.get_volume_element("SW")
                if sw:
                    initialize_parcel_contents(p, biotic_ve)
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
                    m = CompartmentService.media.get_or_create(category='Surface_Soil|Wetland')
                    c = CompartmentService.get_or_create(name="Wetland", volume_element_id=ve.id, media_id=m.id)
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
        if field_name in [k for k, v in Air_params]:
            par_name = [v for k, v in Air_params if k == field_name][0]
            # TODO the below part generates error due to missing par for dustLoad, dustDensity etc...
            cmp = [c for c in p.compartments if "Air in Air_" in c.standard_name][0]
            par = cmp.parameters.get(par_name)
            par.value = parcels_data[field_name]
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
        if field_name == "vadoseZoneSoilThick":
            thickness_before = p.get_compartment("Soil_Vadose_Zone").volume_element.height
            p.get_compartment("Soil_Vadose_Zone").volume_element.bottom = \
                p.get_compartment("Soil_Vadose_Zone").volume_element.top + \
                (-1 * float(parcels_data['vadoseZoneSoilThick']))
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
                    # par = c.parameters.get('soilTillage')
                    par_obj = [pp for pp in ParameterService.definitions.get_all() if
                               pp.full_name == "soilTillage"]
                    req_comp = f'(self.id == {c.id})'
                    par = ParameterService.get_or_create(definition_id=par_obj[0].id, requirements=req_comp,
                                                         scenario_id=p.scenario_id)
                    if parcels_data['tillage'] == "Yes":
                        par.value = 1
                    elif parcels_data['tillage'] == "No":
                        par.value = 0

        if field_name in ['flush_rate', 'suspended_sed_conc', 'algae_density', 'chloride_conc', 'chlorophyll_conc',
                          'mean_depth', 'evaporation_rate', 'suspended_organic_carbon', 'water_ph',
                          'sed_deposition_vel', 'water_temp', 'sed_inflow']:
            par_name = {'flush_rate': "Flushes",
                        'suspended_sed_conc': "SuspendedSedimentConcentration",
                        'algae_density': "AlgaeDensityInWaterColumn",
                        'chloride_conc': "ChlorideConcentration",
                        'chlorophyll_conc': "ChlorophyllConcentration",
                        'mean_depth': "MeanWaterDepth",
                        'evaporation_rate': "waterEvaporationRate",
                        'suspended_organic_carbon': "OrganicCarbonContent",
                        'water_ph': "pH",
                        'sed_deposition_vel': "SedimentDepositionVelocity",
                        'water_temp': "WaterTemperature",
                        'sed_inflow': "ExternalSedimentInflow"}
            comp = p.get_compartment("Surface_water")
            par = comp.parameters.get(par_name[field_name])
            if par:
                if par.__tablename__ == "custom_parameter":
                    par.value = parcels_data[field_name]
                else:
                    par_obj = [pp for pp in ParameterService.definitions.get_all() if
                               pp.full_name == par_name[field_name]]
                    req_comp = f'(self.id == {comp.id})'
                    par = ParameterService.get_or_create(definition_id=par_obj[0].id, requirements=req_comp,
                                                         scenario_id=p.scenario_id, unit=par.default_unit)
                    par.value = parcels_data[field_name]
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
                if par.__tablename__ == "custom_parameter":
                    par.value = parcels_data[field_name]
                else:
                    par_obj = [pp for pp in ParameterService.definitions.get_all() if
                               pp.full_name == par_name[field_name]]
                    req_comp = f'(self.id == {comp.id})'
                    par = ParameterService.get_or_create(definition_id=par_obj[0].id, requirements=req_comp,
                                                         scenario_id=p.scenario_id, unit=par.default_unit)
                    par.value = parcels_data[field_name]
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
                this_comp.parameters[param].value = parcels_data[param]

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
                    print(f"{field_name} ---> {base_name} this comp {this_comp}")
                    print(f'{prop} ---> {parcels_data[field_name]} current val {this_comp.parameters[prop].value}')
                    if this_comp.parameters.get(prop).__tablename__ == "parameter_definition":
                        this_req_comp = f'(self.id == {this_comp.id})'
                        ParameterService.get_or_create(definition_id=this_comp.parameters.get(prop)[0].id,
                                                       scenario_id=p.scenario_id,
                                                       requirements=this_req_comp,
                                                       value=float(parcels_data[field_name]),
                                                       unit=this_comp.parameters.get(prop)[0].default_unit)
                    else:
                        this_comp.parameters.get(prop).value = float(parcels_data[field_name])
        if field_name in ["pH", "rho", "AverageVerticalVelocity", "FractionSand", "OrganicCarbonContent",
                          "VolumeFraction_Liquid", "VolumeFraction_Vapor", "Porosity", "AirSoilBoundaryThickness",
                          "Fractionofareaavailableforerosion", "FractionofAreaAvailableforRunoff",
                          "Fractionofareaavailableforverticaldiffusion", "TotalRunoffRate"]:
            this_par = p.get_compartment(name=parcels_data["comp_name"]).parameters.get(parcels_data["field"])
            this_par.value = float(parcels_data[field_name])
        if field_name == "emission":
            src_comp = [c for c in p.compartments if c.name == parcels_data["compartment_name"]][0]
            src_par = [par for parn, par in src_comp.parameters.items() if parn == "surfaceDepositionRate"]
            chem = ChemicalService.get(name=parcels_data["chemical_name"])
            if len(src_par) > 0:
                src_par = src_par[0]
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
            scn = ScenarioService.get(id=parcels_data["id"])
            sender_parcel_name = parcels_data["sender"].replace("ro_", "")
            receivers = parcels_data["receiver"].split(",")
            values = parcels_data["ro_value"].split(",")
            sp = scn.parcels.where(Parcel.name == sender_parcel_name).first()
            sender_comp = sp.get_compartment("Soil_Surface")
            sender_par = [sender_comp.parameters.get("FractionOfTotalRunoff")]
            if len(sender_par) > 0:
                sender_par = sender_par[0]
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
                    entity_name = "receiver"
                    formula_entity = receiver_comp
                    # this pattern captures integers, decimals and/or numbers with scientific notations that may or may
                    # not be in parentheses
                    val_pattern = re.compile(r"\(?(\d+(?:\.\d+(?:[eE][+\-]?\d+)?))\)?")
                    # We have the receiver compartment in the formula
                    # TODO #1 Update formula only if the sender_comp.connects_to(receiver_comp) == True. if there is no
                    #   connection (this means no custom link and
                    #   sender_comp.volume_element.interface_with(sender_comp.volume_element) == False), either create
                    #   a custom link or send error back to be shown as a validation error using async await in api call
                    if not sender_comp.connects_to(receiver_comp):
                        return ApiResult({
                            'message': f'{sender_comp.standard_name} does not connect to {receiver_comp.standard_name}'
                            })
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

    except Exception as e:
        logger.error(traceback.format_exc())
    return ApiResult({'message': 'success'})


@parcels_api.route('/api/scenario/<int:scenario_id>/parcel/<int:id>/delete', methods=['POST'])
@login_required
def delete_parcel(id, scenario_id):
    logger = make_logger('parcels_api_delete')
    try:
        p = ParcelService.get(id)
        # Delete Contents
        delete_parcel_contents(p)

        # Delete the specified parcel
        p = ParcelService.delete(id, no_commit=True)

        # Save the scenario
        ParcelService.commit()
    except Exception as e:
        logger.error(traceback.format_exc())

    return "success"


def get_land_use(pcl):
    land = False
    land_use = 'Impervious'
    for comp in pcl.compartments:
        if comp.media.isa('Surface_Soil'):
            land = True
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
    return land_use


def initialize_parcel_contents(new_parcel, vol_elem_defaults=None):
    if vol_elem_defaults is None:
        vol_elem_defaults = dict(Land_Parcel_VolElem_defaults)
    else:
        vol_elem_defaults = dict(vol_elem_defaults)
    # Add the Sources
    vol_elem_defaults.update(Wet_Dry_Source_VolElem_defaults)

    for ve in vol_elem_defaults.items():
        # Create standard volume elements
        if new_parcel.get_volume_element(ve[1]["name"]):
            nve = new_parcel.get_volume_element(ve[1]["name"])
        else:
            nve = VolumeElementService.get_or_create(name=ve[1]["name"], parcel_id=new_parcel.id, top=ve[1]["top"],
                                                     bottom=ve[1]["bottom"])
        for c in ve[1]["Compartments"].items():
            # Create standard compartments linking them to default volume elements and media for each compartment
            media_id = [m.id for m in CompartmentService.media.get_all() if m.name == c[1]["media_name"]][0]

            if new_parcel.get_compartment(c[1]["name"]):
                nc = new_parcel.get_compartment(c[1]["name"])
            else:
                nc = CompartmentService.get_or_create(name=c[1]["name"], volume_element_id=nve.id,
                                                      media_id=media_id)
            # Add in custom parameters for new compartments using the self.id = <id of new compartment>
            if nc.name == "Soil_Surface":
                # Default Total Erosion Rate
                ter_obj = [pp for pp in ParameterService.definitions.get_all() if pp.full_name == "TotalErosionRate"]
                ter = ParameterService.get_or_create(definition_id=ter_obj[0].id, scenario_id=new_parcel.scenario_id,
                                                     requirements=f'(self.id == {nc.id})',
                                                     value=calc_default_erosion_rate_sdr(new_parcel),
                                                     unit="kg/m^2/day")
           # elif nc.name == "Surface_water" or nc.name == "Sediment":


def get_surface_runoff(scenario_id):
    scenario = ScenarioService.get(id=scenario_id)
    soil_comps = [c for c in scenario.compartments if c.media.isa("Surface_Soil")]
    water_comps = [c for c in scenario.compartments if c.media.isa("Surface_Water")]
    sink_comps = [c for c in scenario.compartments if
                  c.media.isa("Sink") & c.media.isa("Advection") & (not c.media.isa("Flush$"))]
    runoffs = {}
    for send in soil_comps:
        sending_parcel = send.volume_element.parcel.name
        runoffs[sending_parcel] = {}
        runoffs[sending_parcel]['sink'] = 0
        for recv in soil_comps + sink_comps + water_comps:
            receiving_parcel = recv.volume_element.parcel.name
            if recv in sink_comps:
                runoffs[sending_parcel]['sink'] += send.FractionOfTotalRunoff(receiver=recv)
            else:
                runoffs[sending_parcel][receiving_parcel] = send.FractionOfTotalRunoff(receiver=recv)
    return runoffs


def calc_default_erosion_rate_sdr(pcl):
    for c in pcl.compartments:
        if not c.media.isa("Soil_Surface"):
            continue
        unit_soil_loss = c.parameters["unitSoilLoss"].default_value
        area_in_sq_mile = (pcl.area / 1E6) / 2.58998811
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
        return unit_soil_loss * sed_delivery_ratio


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
        custom_params = ParameterService.get_all(requirements=f'(self.id == {comp_id})')
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
                new_complist = [str(int(i.strip())) for i in complist if int(i.strip()) != del_id]
                sub_parts[0] = " , ".join(new_complist)
                eq_parts[i] = "}".join(sub_parts)
            new_eq = 'compartment.id in {'.join(eq_parts)
            ParameterService.get(par.id).formula.equation = new_eq
            ParameterService.commit()
    # Delete Volume Elements
    for ve in del_parcel.volume_elements:
        VolumeElementService.delete(ve, False)


def create_base_land_compartments(parcels_data, p, land_use):
    ve_surfsoil = VolumeElementService.get(name="SurfSoil", parcel_id=p.id)
    c_surfsoil = CompartmentService.get(name="Soil_Surface", volume_element_id=ve_surfsoil.id)
    custom_param_erosion = ParameterService.get(requirements=f'(self.id == {c_surfsoil.id})',
                                                definition_id=596)
    # delete existing compartments
    if land_use in ['Tilled Soil', 'Untilled Soil', 'Impervious']:
        # Revert Soil_surface compartment to default media (Surface_Soil [id = 7])
        c_surfsoil.media_id = 7  # Surface Soil
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
                # Remove compartments
                CompartmentService.delete(c, False)
                # Remove custom_parameters with the requirement self.id = c.id
                custom_params = ParameterService.get_all(requirements=f'(self.id == {c.id})')
                for cp in custom_params:
                    ParameterService.delete(cp, False)
    # Create the base compartments for the new land use/ land cover
    if parcels_data['landUse'] == 'Tilled Soil':
        c_surfsoil.media_id = 55
    elif parcels_data['landUse'] == 'Untilled Soil':
        c_surfsoil.media_id = 56
    elif parcels_data['landUse'] == 'Impervious':
        c_surfsoil.media_id = 57
        custom_param_erosion.value = 0
    elif parcels_data['landUse'] == 'Coniferous Forest':
        CompartmentService.create(name="Leaf_Coniferous_Forest", volume_element_id=ve_surfsoil.id,
                                  media_id=[m for m in CompartmentService.media.get_all() if m.isa('Coniferous_Leaf')][0].id)
        CompartmentService.create(name="Leaf_Particle_Coniferous_Forest", volume_element_id=ve_surfsoil.id,
                                  media_id=[m for m in CompartmentService.media.get_all() if m.isa('Coniferous_Leaf_Particle')][0].id)
    elif parcels_data['landUse'] == 'Deciduous Forest':
        CompartmentService.create(name="Leaf_Deciduous_Forest", volume_element_id=ve_surfsoil.id,
                                  media_id=[m for m in CompartmentService.media.get_all() if m.isa('Deciduous_Leaf')][0].id)
        CompartmentService.create(name="Leaf_Particle_Deciduous_Forest", volume_element_id=ve_surfsoil.id,
                                  media_id=[m for m in CompartmentService.media.get_all() if m.isa('Deciduous_Leaf_Particle')][0].id)
    elif parcels_data['landUse'] == 'Grasses/Herbs':
        CompartmentService.create(name="Leaf_Grasses_Herbs", volume_element_id=ve_surfsoil.id,
                                  media_id=[m for m in CompartmentService.media.get_all() if m.isa('Grass_Leaf')][0].id)
        CompartmentService.create(name="Leaf_Particle_Grasses_Herbs", volume_element_id=ve_surfsoil.id,
                                  media_id=[m for m in CompartmentService.media.get_all() if m.isa('Grass_Leaf_Particle')][0].id)
        CompartmentService.create(name="Stem_Grasses_Herbs", volume_element_id=ve_surfsoil.id,
                                  media_id=[m for m in CompartmentService.media.get_all() if m.isa('Grass_Stem')][0].id)
        CompartmentService.create(name="Root_Grasses_Herbs", volume_element_id=ve_surfsoil.id,
                                  media_id=[m for m in CompartmentService.media.get_all() if m.isa('Grass_Root')][0].id)
    elif parcels_data['landUse'] == 'Agriculture - General':
        CompartmentService.create(name="Leaf_Agriculture", volume_element_id=ve_surfsoil.id,
                                  media_id=[m for m in CompartmentService.media.get_all() if m.isa('Agriculture_Leaf')][0].id)
        CompartmentService.create(name="Leaf_Particle_Agriculture", volume_element_id=ve_surfsoil.id,
                                  media_id=[m for m in CompartmentService.media.get_all() if m.isa('Agriculture_Leaf_Particle')][0].id)
        CompartmentService.create(name="Stem_Agriculture", volume_element_id=ve_surfsoil.id,
                                  media_id=[m for m in CompartmentService.media.get_all() if m.isa('Agriculture_Stem')][0].id)
        CompartmentService.create(name="Root_Agriculture", volume_element_id=ve_surfsoil.id,
                                  media_id=[m for m in CompartmentService.media.get_all() if m.isa('Agriculture_Root')][0].id)
    CompartmentService.update(c_surfsoil)
