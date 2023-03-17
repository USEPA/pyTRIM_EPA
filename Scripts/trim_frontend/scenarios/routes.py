from flask import Blueprint, request, render_template, redirect, url_for
from flask_security import login_required, current_user
from custom.flask_api import ApiResult,  ApiException
from trim_db import ScenarioService, ParcelService, CompartmentService, VolumeElementService, ParameterService
from trim_frontend import api
from .forms import *
from trim_db import Scenario, Parcel
from ..utils.logging import make_logger

import traceback
import re
import json

scenario = Blueprint('scenario', __name__)

Air_Parcel_VolElem_defaults = {
    'Air': {
        'name': 'Air',
        'top': 800,
        'bottom': 0,
        'Compartments': {
            'Air': {
                'name': 'Air',
                'media_id': 2
            },
            'Degradation_Reaction_Sink': {
                'name': 'Degradation_Reaction_Sink',
                'media_id': 15
            }
        }
    },
    'UpperAir': {
        'name': 'UpperAir',
        'top': 1000,
        'bottom': 800,
        'Compartments': {
            'Air': {
                'name': 'Air',
                'media_id': 2
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
                'media_id': 7
            },
            'Degradation_Reaction_Sink': {
                'name': 'Degradation_Reaction_Sink',
                'media_id': 15
            },
            'Leaf_Grasses_Herbs': {
                'name': 'Leaf_Grasses_Herbs',
                'media_id': 40
            },
            'Leaf_Particle_Grasses_Herbs': {
                'name': 'Leaf_Particle_Grasses_Herbs',
                'media_id': 44
            },
            'Stem_Grasses_Herbs': {
                'name': 'Stem_Grasses_Herbs',
                'media_id': 42
            },
            'Root_Grasses_Herbs': {
                'name': 'Root_Grasses_Herbs',
                'media_id': 45
            },
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
                'media_id': 4
            },
            'Degradation_Reaction_Sink': {
                'name': 'Degradation_Reaction_Sink',
                'media_id': 15
            },
            'Flush_Rate_Sink': {
                'name': 'Flush_Rate_Sink',
                'media_id': 18
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
                'media_id': 5
            },
            'Degradation_Reaction_Sink': {
                'name': 'Degradation_Reaction_Sink',
                'media_id': 15
            }
        }
    }
}


@scenario.route('/scenario')
@login_required
def view_scenarios():
    scenarios = current_user.active_scenarios
    scenario_form = ScenarioDefinitionForm()

    return render_template(
        'scenarios/view_all.html', scenarios=scenarios,
        scenario_form=scenario_form
    )


@scenario.route('/scenario/<int:id>')
@login_required
def view_scenario(id):
    s = Scenario.query.filter_by(id=id).first()
    return render_template('scenarios/view_single.html', scenario=s)


@scenario.route('/scenario', methods=['POST'])
@login_required
def create_scenario():
    form = ScenarioDefinitionForm()
    if not form.validate_on_submit():
        redirect(url_for('scenario.view_scenarios'))

    # Create a new scenario with the form data
    s = ScenarioService.create(no_commit=True)
    form.populate_obj(s)
    if not s.name:
        raise AssertionError("Scenario name cannot be blank.")

    # Set the current_user as the form creator
    s.creator = current_user

    # Save the scenario
    ScenarioService.commit()

    return redirect(url_for('scenario.edit_scenario', id=s.id))


@scenario.route('/scenario/<int:id>/edit')
@login_required
def edit_scenario(id):
    s = ScenarioService.get(id)

    return render_template('scenarios/editor.html', scenario=s)


scenario_api = Blueprint('scenario_api', __name__)
api.use_api_errors(scenario_api)


@scenario_api.route('/api/scenario/<int:id>')
@login_required
def get_scenario(id):
    s = ScenarioService.get(id)

    if s is not None:
        s = s.as_serializable()
        s['emissions_sources'] = [
            {'name': 'alpha', 'chemicals': [{'rate': 100}]},
            {'name': 'beta', 'chemicals': [{'chemical': 'Chromium'}]}
        ]

    return ApiResult({'scenario': s})


parcels_api = Blueprint('parcels_api', __name__)
api.use_api_errors(parcels_api)


@parcels_api.route('/api/parcels', methods=['POST'])
@login_required
def create_parcels():
    logger = make_logger('parcels_api_create')
    # form = ScenarioParcelsForm()
    # if not form.validate_on_submit():
    #    redirect(url_for('parcel.view_parcels'))
    try:
        parcels_data = request.form.to_dict()
        from_url = request.referrer
        this_scenario_id = int(re.findall('/scenario/(\d+)/', from_url)[0])
        if not this_scenario_id:
            raise ApiException("No Scenario defined")
        # if not parcels_data:
        #    raise ApiException("No parcels defined")

        # Create a new parcel with the form data
        p = ParcelService.create(no_commit=True)
        # form.populate_obj(p)

        if not parcels_data['name']:
            raise AssertionError("Parcel name cannot be blank.")

        p.name = parcels_data['name']
        p.description = parcels_data['desc']
        p.scenario_id = this_scenario_id
        p.vertices = json.loads(parcels_data['geom'])

        # Save the scenario
        ParcelService.commit()
        # Add default compartments, media and parameters
        initialize_parcel_contents(p)
        media = CompartmentService.media.land_use_media_list
    except Exception as e:
        logger.error(traceback.format_exc())

    return ApiResult({'scenario': p.as_serializable(), 'media': media})


@parcels_api.route('/api/parcels/', methods=['GET'])
@login_required
def get_parcels():
    logger = make_logger('parcels_api_get')
    try:
        from_url = request.referrer
        this_scenario_id = int(re.findall('/scenario/(\d+)/', from_url)[0])
        if not this_scenario_id:
            raise ApiException("No Scenario defined")
        p = ParcelService.get_all(scenario_id=this_scenario_id)
        m = CompartmentService.media.land_use_media_list
        s = ScenarioService.get(this_scenario_id)
        parcels = []
        media = m
        if p is not None:
            sh = s.as_serializable()
            for this_p in p:
                parcels.append(this_p.as_serializable())
    except Exception as e:
        logger.error(traceback.format_exc())

    return ApiResult({'scenario_head': sh, 'scenario': parcels, 'media': media})


@parcels_api.route('/api/parcels/update', methods=['POST'])
@login_required
def update_parcel():
    logger = make_logger('parcels_api_update')
    try:
        parcels_data = request.form.to_dict()
        if not parcels_data['id']:
            raise AssertionError("Parcel ID cannot be blank.")
        # Get the specified parcel
        p = ParcelService.get(int(parcels_data['id']))

        # Update the specified property
        field_name = parcels_data["field"]
        if field_name == "parcelType":
            # Delete all compartments and volume elements
            delete_parcel_contents(p)
            if parcels_data['parcelType'] == "Air Only":
                # add standard Air Volume element and compartments
                initialize_parcel_contents(p, "Air")
            if parcels_data['parcelType'] == "Water Only":
                # add standard Water Volume element and compartments
                initialize_parcel_contents(p, "Water")
            if parcels_data['parcelType'] == "Land Only":
                # add standard Land Volume element and compartments
                initialize_parcel_contents(p, "Land")
            if parcels_data['parcelType'] == "Land & Air":
                # add standard Air Volume element and compartments
                initialize_parcel_contents(p, "Air")
                # add standard Land Volume element and compartments
                initialize_parcel_contents(p, "Land")
            if parcels_data['parcelType'] == "Water & Air":
                # add standard Air Volume element and compartments
                initialize_parcel_contents(p, "Air")
                # add standard Water Volume element and compartments
                initialize_parcel_contents(p, "Water")

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
            if parcels_data['hasFishFoodWeb'] == "Yes":
                if p.get_volume_element("SW"):
                    ve = p.get_volume_element("SW")
                    c = CompartmentService.get_or_create(name="Fish", volume_element_id=ve.id, media_id=54)
                if not p.get_volume_element("SW"):
                    raise ValueError("Cannot create or get Fish Compartment")
            if parcels_data['hasFishFoodWeb'] == "No":
                if p.get_volume_element("SW"):
                    ve = p.get_volume_element("SW")
                    if ve.get_compartment("Fish"):
                        cmp = ve.get_compartment("Fish")
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
        if field_name == "dustLoad":
            for c in p.compartments:
                if c.name == "Air":
                    par = c.parameters.get("DustLoad")
                    par.value = parcels_data['dustLoad']
        if field_name == "dustDensity":
            for c in p.compartments:
                if c.name == "Air":
                    par = c.parameters.get("DustDensity")
                    par.value = parcels_data['dustDensity']
        if field_name == "airDensity":
            for c in p.compartments:
                if c.name == "Air":
                    par = c.parameters.get("AirDensity")
                    par.value = parcels_data['airDensity']
        if field_name == "fractionOrganicMatteronParticulates":
            for c in p.compartments:
                if c.name == "Air":
                    par = c.parameters.get("FractionOrganicMatteronParticulates")
                    par.value = parcels_data['fractionOrganicMatteronParticulates']
        if field_name == "fractionOrganicMatteronParticulates":
            for c in p.compartments:
                if c.name == "Air":
                    par = c.parameters.get("FractionOrganicMatteronParticulates")
                    par.value = parcels_data['fractionOrganicMatteronParticulates']
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
            for soil_comp in ["Groundwater", "DryVaporSource", "WetVaporSource",
                              "DryParticleSource", "WetParticleSource"]:
                p.get_compartment(soil_comp).volume_element.top = \
                    (-1 * delta_thickness) + p.get_compartment(soil_comp).volume_element.top
                p.get_compartment(soil_comp).volume_element.bottom = \
                    (-1 * delta_thickness) + p.get_compartment(soil_comp).volume_element.bottom
        if field_name == "tillage":
            for c in p.compartments:
                if c.name == 'Soil_Surface':
                    par = c.parameters.get('soilTillage')
                    if parcels_data['tillage'] == "Yes":
                        par.value = 1
                    elif parcels_data['tillage'] == "No":
                        par.value = 0
        # Update record
        ParcelService.update(p)

    except Exception as e:
        logger.error(traceback.format_exc())
    return "success"


@parcels_api.route('/api/parcels/delete', methods=['POST'])
@login_required
def delete_parcels():
    logger = make_logger('parcels_api_delete')
    try:
        parcels_data = request.form.to_dict()
        if not parcels_data['parcelid']:
            raise AssertionError("Parcel ID cannot be blank.")

        del_parcel = ParcelService.get(id=int(parcels_data['parcelid']))
        # Delete Contents
        delete_parcel_contents(del_parcel)

        # Delete the specified parcel
        p = ParcelService.delete(int(parcels_data['parcelid']), no_commit=True)

        # Save the scenario
        ParcelService.commit()
    except Exception as e:
        logger.error(traceback.format_exc())

    return "success"


def initialize_parcel_contents(new_parcel, parcel_type="Land"):
    if parcel_type == "Land":
        parcel_defaults = Land_Parcel_VolElem_defaults
    elif parcel_type == "Water":
        parcel_defaults = Water_Parcel_VolElem_defaults
    elif parcel_type == "Air":
        parcel_defaults = Air_Parcel_VolElem_defaults

    for ve in parcel_defaults.items():
        # Create standard volume elements
        nve = VolumeElementService.get_or_create(name=ve[1]["name"], parcel_id=new_parcel.id, top=ve[1]["top"],
                                                 bottom=ve[1]["bottom"])
        for c in ve[1]["Compartments"].items():
            # Create standard compartments linking them to default volume elements and media for each compartment
            nc = CompartmentService.get_or_create(name=c[1]["name"], volume_element_id=nve.id,
                                                  media_id=c[1]["media_id"])
            # Add in custom parameters for new compartments using the self.id = <id of new compartment>
            if nc.name == "Soil_Surface":
                # Default Total Erosion Rate
                ter = ParameterService.get_or_create(definition_id=517, scenario_id=new_parcel.scenario_id,
                                                     requirements=f'(self.id == {nc.id})',
                                                     value=new_parcel.calc_default_erosion_rate_sdr(),
                                                     unit="kg/m^2/day")


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
