from flask import Blueprint, request, render_template, redirect, url_for
from flask_security import login_required, current_user
from flask_api import ApiResult
from datetime import datetime
from trim_db import ScenarioService, ParcelService, \
    CompartmentService, VolumeElementService, ParameterService, ChemicalService
from trim_frontend import api
from trim_frontend.parcels.routes import delete_parcel_contents
from .forms import *
from ..utils.logging import make_logger

import traceback

scenario = Blueprint('scenario', __name__)


@scenario.route('/scenario')
@login_required
def view_scenarios():
    scenarios = current_user.active_scenarios
    scenario_form = ScenarioDefinitionForm()

    return render_template(
        'scenarios/view_all.html', scenarios=scenarios,
        scenario_form=scenario_form,
        logged_in_user = current_user
    )


@scenario.route('/scenario/<int:id>')
@login_required
def view_scenario(id):
    s = ScenarioService.get(id=id)
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
    return ApiResult({'scenario': s.as_serializable()})


@scenario_api.route('/api/scenario/update', methods=['POST'])
@login_required
def update_scenario():
    logger = make_logger('scenario_api_update')
    try:
        scenario_data = request.form.to_dict()
        if not scenario_data['id']:
            raise AssertionError("Scenario ID cannot be blank.")
        # Get the specified parcel
        s = ScenarioService.get(int(scenario_data['id']))

        # Update the specified property
        field_name = scenario_data["field"]
        if field_name == "erosionRateCalcSource":
            ercs = scenario_data["erosionRateCalcSource"]
            ercs_obj = [pp for pp in ParameterService.definitions.get_all() if pp.full_name == "erosionRateCalcSource"]
            ercs_cp = ParameterService.get_or_create(definition_id=ercs_obj[0].id, scenario_id=scenario_data['id'])
            ercs_cp.value = ercs
            # for cp in s.custom_params:
            #     if cp.definition.variable_name == "erosionRateCalcSource":
            #         cp.value = ercs
            ParameterService.commit()
    except Exception as e:
        logger.error(traceback.format_exc())
    ScenarioService.update(s)
    return "success"


@scenario_api.route('/api/scenario/copy/', methods=['POST'])
@login_required
def copy_scenario():
    scenario_data = request.form.to_dict()
    if not scenario_data.get('user_id'):
        raise AssertionError("User ID cannot be blank.")
    if not scenario_data.get('scenario_id'):
        raise AssertionError("Scenario ID cannot be blank.")
    
    scenario_id = int(scenario_data['scenario_id'])
    user_id = int(scenario_data['user_id'])
    s = ScenarioService.get(scenario_id)
    res = "Fail"

    try:
        # Create new Scenario
        # Version counter
        if len(s.name) >= 120:
            new_name = f"{s.name[:114]}"
        else:
            new_name = s.name

        rname = new_name[::-1]
        ridx = rname.find("#V_")
        if ridx == -1:
            new_name = f"{new_name}_V#1"
        else:    
            version = int(rname[:ridx][::-1])
            new_name = rname.replace(rname[:ridx], "", 1)
            new_name = new_name[::-1] + str(version + 1)
             
        ns = ScenarioService.create(name=new_name, description=f'Copy of {s.name} on {datetime.now()}', creator_id=user_id)
        ScenarioService.commit()

        # Add scenario chemicals
        for sc in s.chemicals:
            ns.chemicals.append(sc)
        ScenarioService.commit()

        # Create new parcels
        cmp_map = {}
        for prc in s.parcels.all():
            np = ParcelService.create(name=prc.name, description=prc.description, scenario_id=ns.id, vertices=prc.vertices)
            ParcelService.commit()
            # Create new volume elements
            for ve in prc.volume_elements:
                nve = VolumeElementService.create(name=ve.name, parcel_id=np.id, top=ve.top, bottom=ve.bottom)
                VolumeElementService.commit()
                # Create new volume compartments
                for cmp in ve.compartments:
                    ncmp = CompartmentService.create(name=cmp.name, volume_element_id=nve.id, media_id=cmp.media_id)
                    cmp_map[cmp.id] = ncmp.id
                    CompartmentService.commit()
                    # Create new custom parameters for compartments
                    for parn, cpar in cmp.parameters.items():
                        if cpar.__tablename__ == "custom_parameter":
                            ParameterService.create(definition_id=cpar.definition_id, scenario_id=ns.id,
                                                    requirements=f"(self.id == {ncmp.id})", value=cpar.value,
                                                    unit=cpar.unit, formula_id=cpar.formula_id)
                            ParameterService.commit()

        # Create the compartment links using the compartment id map
        for lnk in CompartmentService.links.get_all():
            if lnk.sender_id in cmp_map.keys():
                CompartmentService.links.create(sender_id=cmp_map[lnk.sender_id], receiver_id=cmp_map[lnk.receiver_id])
        CompartmentService.commit()
        res = "Success"
    except Exception as e:
        print(e)
        print("Failed to copy scenario...")

    # return ApiResult({'result': res})
    return redirect(request.referrer)


@scenario_api.route('/api/scenario/delete/', methods=['POST'])
@login_required
def delete_scenario():
    scenario_data = request.form.to_dict()
    if not scenario_data.get('scenario_id'):
        raise AssertionError("Scenario ID cannot be blank.")
    
    scenario_id = int(scenario_data['scenario_id'])
    s = ScenarioService.get(scenario_id)

    try:
        # Delete all parcels and contents
        for parcel in s.parcels.all():
            delete_parcel_contents(parcel)
            ParcelService.delete(parcel.id)

        # Delete scenario chemicals
        for sc in s.chemicals:
            ChemicalService.delete(sc.id)

        # Delete scenario
        ScenarioService.delete(s.id)
    except Exception as e:
        print(e)
        print("Failed to delete scenario...")

    return redirect(request.referrer)
