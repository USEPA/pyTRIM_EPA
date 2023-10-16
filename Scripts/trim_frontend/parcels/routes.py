from flask import Blueprint, request, render_template
from flask_security import login_required
from flask_api import ApiResult,  ApiException
from trim_db import ScenarioService, ParcelService, \
    CompartmentService, VolumeElementService, ParameterService
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
        media = CompartmentService.media.land_use_media_list
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
        m = CompartmentService.media.land_use_media_list
        parcels = []
        media = m

        if p is not None:
            sh = s.as_serializable()
            for this_p in p:
                start_time = time.time()
                parcels.append(this_p.as_serializable())
                logger.info(f"Acquired parcel {this_p.name} in {time.time() - start_time} seconds")
    except Exception as e:
        logger.error(traceback.format_exc())

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
                if not parcels_data['landUse'] == p.land_use:
                    create_base_land_compartments(parcels_data, p)
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
            if parcels_data['hasFarmFoodChain'] == "Yes":
                if p.get_volume_element("SurfSoil"):
                    ve = p.get_volume_element("SurfSoil")
                    c = CompartmentService.get_or_create(name="Farm", volume_element_id=ve.id, media_id=53)
                if not p.get_volume_element("SurfSoil"):
                    raise ValueError("Cannot create or get Farm Compartment")
            if parcels_data['hasFarmFoodChain'] == "No":
                if p.get_volume_element("SurfSoil"):
                    ve = p.get_volume_element("SurfSoil")
                    if ve.get_compartment("Farm"):
                        cmp = ve.get_compartment("Farm")
                        CompartmentService.delete(cmp, False)
        if field_name == "hasFishFoodWeb":
            biotic_ve = dict(Water_Parcel_VolElem_defaults)
            biotic_ve["Sed"]["Compartments"] = dict(Aquatic_Biota_Sed_Compartment_defaults["Compartments"])
            biotic_ve["SW"]["Compartments"] = dict(Aquatic_Biota_SW_Compartment_defaults["Compartments"])
            if parcels_data['hasFishFoodWeb'] == "Yes":
                if p.get_volume_element("SW"):
                    # ve = p.get_volume_element("SW")
                    # c = CompartmentService.get_or_create(name="Fish", volume_element_id=ve.id, media_id=54)
                    initialize_parcel_contents(p, biotic_ve)
                if not p.get_volume_element("SW"):
                    raise ValueError("Cannot create or get Fish Compartment")
            if parcels_data['hasFishFoodWeb'] == "No":
                for vek, vev in biotic_ve.items():
                    if p.get_volume_element(vek):
                        ve = p.get_volume_element(vek)
                        for k, v in biotic_ve[vek]["Compartments"].items():
                            if ve.get_compartment(v["name"]):
                                cmp = ve.get_compartment(v["name"])
                                logger.info(f"Deleted {cmp.name}")
                                CompartmentService.delete(cmp, False)
        if field_name == "hasWetland":
            if parcels_data['hasWetland'] == "Yes":
                if p.get_volume_element("SurfSoil"):
                    ve = p.get_volume_element("SurfSoil")
                    c = CompartmentService.get_or_create(name="Wetland", volume_element_id=ve.id, media_id=58)
                if not p.get_volume_element("SurfSoil"):
                    raise ValueError("Cannot create or get Wetland Compartment")
            if parcels_data['hasWetland'] == "No":
                if p.get_volume_element("SurfSoil"):
                    ve = p.get_volume_element("SurfSoil")
                    if ve.get_compartment("Wetland"):
                        cmp = ve.get_compartment("Wetland")
                        CompartmentService.delete(cmp, False)
        if field_name == "description":
            p.description = parcels_data['description']
        if field_name == 'totalErosionRate':
            for c in p.compartments:
                if c.media.isa('Surface_Soil'):
                    par = c.parameters.get('TotalErosionRate')
                    par.value = parcels_data['totalErosionRate']

        Air_params = [('dustLoad', "DustLoad"),
                      ("dustDensity", "DustDensity"),
                      ("airDensity", "AirDensity"),
                      ("fractionOrganicMatteronParticulates", "FractionOrganicMatteronParticulates")]
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

        # Update record
        ParcelService.update(p)

    except Exception as e:
        logger.error(traceback.format_exc())
    return "success"


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
                                                     value=new_parcel.calc_default_erosion_rate_sdr(),
                                                     unit="kg/m^2/day")
           # elif nc.name == "Surface_water" or nc.name == "Sediment":


def delete_parcel_contents(del_parcel):
    for c in del_parcel.compartments:
        # Delete Links
        lr = CompartmentService.links.get_all(receiver_id=c.id)
        ls = CompartmentService.links.get_all(sender_id=c.id)
        for lnk_r in lr:
            CompartmentService.links.delete(lnk_r)
        for lnk_s in ls:
            CompartmentService.links.delete(lnk_s)
        # Delete Custom Parameters
        custom_params = ParameterService.get_all(requirements=f'(self.id == {c.id})')
        for cp in custom_params:
            ParameterService.delete(cp, False)
        # Delete Compartments
        CompartmentService.delete(c, False)
    # Delete Volume Elements
    for ve in del_parcel.volume_elements:
        VolumeElementService.delete(ve, False)


def create_base_land_compartments(parcels_data, p):
    ve_surfsoil = VolumeElementService.get(name="SurfSoil", parcel_id=p.id)
    c_surfsoil = CompartmentService.get(name="Soil_Surface", volume_element_id=ve_surfsoil.id)
    custom_param_erosion = ParameterService.get(requirements=f'(self.id == {c_surfsoil.id})',
                                                definition_id=517)
    # delete existing compartments
    if p.land_use in ['Tilled Soil', 'Untilled Soil', 'Impervious']:
        # Revert Soil_surface compartment to default media (Surface_Soil [id = 7])
        c_surfsoil.media_id = 7  # Surface Soil
        # if switching from Impervious, calculate Total erosion rate
        if p.land_use == 'Impervious':
            custom_param_erosion.value = p.calc_default_erosion_rate_sdr()
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
                                  media_id=36)
        CompartmentService.create(name="Leaf_Particle_Coniferous_Forest", volume_element_id=ve_surfsoil.id,
                                  media_id=52)
    elif parcels_data['landUse'] == 'Deciduous Forest':
        CompartmentService.create(name="Leaf_Deciduous_Forest", volume_element_id=ve_surfsoil.id,
                                  media_id=38)
        CompartmentService.create(name="Leaf_Particle_Deciduous_Forest", volume_element_id=ve_surfsoil.id,
                                  media_id=43)
    elif parcels_data['landUse'] == 'Grasses/Herbs':
        CompartmentService.create(name="Leaf_Grasses_Herbs", volume_element_id=ve_surfsoil.id,
                                  media_id=40)
        CompartmentService.create(name="Leaf_Particle_Grasses_Herbs", volume_element_id=ve_surfsoil.id,
                                  media_id=44)
        CompartmentService.create(name="Stem_Grasses_Herbs", volume_element_id=ve_surfsoil.id,
                                  media_id=42)
        CompartmentService.create(name="Root_Grasses_Herbs", volume_element_id=ve_surfsoil.id,
                                  media_id=45)
    elif parcels_data['landUse'] == 'Agriculture - General':
        CompartmentService.create(name="Leaf_Agriculture", volume_element_id=ve_surfsoil.id,
                                  media_id=34)
        CompartmentService.create(name="Leaf_Particle_Agriculture", volume_element_id=ve_surfsoil.id,
                                  media_id=50)
        CompartmentService.create(name="Stem_Agriculture", volume_element_id=ve_surfsoil.id,
                                  media_id=41)
        CompartmentService.create(name="Root_Agriculture", volume_element_id=ve_surfsoil.id,
                                  media_id=51)
    CompartmentService.update(c_surfsoil)
