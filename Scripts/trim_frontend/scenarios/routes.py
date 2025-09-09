import json
import os
import re
import time
import pint
import types
from datetime import datetime
from pathlib import Path

import boto3
import pandas as pd
from flask import Blueprint, request, render_template, redirect, url_for
from flask_security import login_required, current_user
from flask_api import ApiException, ApiResult
from datetime import datetime
from trim_db.schema import ScenarioLoadRunProc, \
    CustomParameter, ParameterDefinition
from trim_db.services import ScenarioService, ChemicalService, \
    ParcelService, CompartmentService, VolumeElementService, \
    ParameterService, FormulaService
from trim_frontend import api, db
from trim_frontend.parcels.routes import delete_parcel_contents
from .defaults import *
from .forms import *
from .utils import *
from ..utils.logging import make_logger
from ..utils.file_io import MiscAssociatedFileVariety, associated_file_helper
from ..parcels.utils import calculate_receptor_grid_points_for_parcel
from trim_core.algorithms.full_model_run import run_full_model
# from trim_core.algorithms.GetFlow.getflow import run_getflow_v7_for_scenario_id
# from sqlalchemy import inspect

import traceback

scenario = Blueprint('scenario', __name__)


@scenario.route('/scenario', methods=['GET'])
@login_required
def view_scenarios():
    scenarios = current_user.active_scenarios
    scenario_form = ScenarioDefinitionForm()

    return render_template(
        'scenarios/view_all.html', scenarios=scenarios,
        scenario_form=scenario_form,
        logged_in_user=current_user
    )


@scenario.route('/scenario/<int:id>', methods=['GET'])
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

    init_first_time_default_param_values()

    # Save the scenario
    ScenarioService.commit()

    return redirect(url_for('scenario.edit_scenario', id=s.id))


@scenario.route('/scenario/<int:id>/edit', methods=['GET'])
@login_required
def edit_scenario(id):
    s = ScenarioService.get(id)

    return render_template('scenarios/editor.html', scenario=s)


scenario_api = Blueprint('scenario_api', __name__)
api.use_api_errors(scenario_api)


@scenario_api.route('/api/scenario/<int:id>', methods=['GET'])
@login_required
def get_scenario(id):
    logger = make_logger('scenario_api_get')
    try:
        s = ScenarioService.get(id)
        start_time = time.time()
        s = s.as_serializable()
        logger.info(f"Acquired scenario in {time.time() - start_time} seconds")
    except Exception as e:
        logger.error(traceback.format_exc())
        return ApiException(repr(e))
    return ApiResult({'scenario': s})


@scenario_api.route(
    '/api/scenario/<int:scenario_id>/chemical', methods=['GET']
)
@login_required
def get_scenario_chemicals(scenario_id):
    s = ScenarioService.get(scenario_id)
    if not s:
        return ApiException("Unknown Scenario")
    chems = [c.as_serializable() for c in s.chemicals]
    return ApiResult({
        'chemicals': chems
    })


@scenario_api.route('/api/scenario/<int:scenario_id>/meteorology/', methods=['GET'])
@login_required
def get_scenario_met_data(scenario_id):
    logger = make_logger('scenario_met_api_get')
    s = ScenarioService.get(scenario_id)
    start_time = time.time()
    try:
        met = get_met_data(s)
    except Exception as e:
        logger.info(e)
        met = {}
    logger.info(f"Acquired meteorology in {time.time() - start_time} seconds")
    return ApiResult({'meteorology': met})


@scenario_api.route('/api/scenario/<int:scenario_id>/seasonal_dynamics/', methods=['GET'])
@login_required
def get_scenario_seasonal_dynamics(scenario_id):
    logger = make_logger('scenario_seasonal_dynamics_api_get')
    s = ScenarioService.get(scenario_id)
    start_time = time.time()
    met = get_seasonal_dynamics(s)
    logger.info(f"Acquired seasonal dynamics in {time.time() - start_time} seconds")
    return ApiResult({'seasonal_dynamics': met})


@scenario_api.route('/api/scenario/<int:scenario_id>/runoff_matrix/', methods=['GET'])
@login_required
def get_scenario_runoff_matrix(scenario_id):
    logger = make_logger('scenario_runoff_matrix_api_get')
    try:
        s = ScenarioService.get(scenario_id)
        start_time = time.time()
        runoff_matrix = ScenarioService(s).get_surface_runoff()
        logger.info(f"Acquired runoff matrix in {time.time() - start_time} seconds")
    except Exception as e:
        logger.error(traceback.format_exc())
        return ApiException(repr(e))
    return ApiResult({'runoff_matrix': runoff_matrix})


@scenario_api.route(
    '/api/scenario/<int:scenario_id>/parameter',
    methods=['GET']
)
@login_required
def get_parameters(scenario_id):
    s = ScenarioService.get(scenario_id)
    if not s:
        return ApiException("Unknown Scenario")

    logger = make_logger('scenario_parameter_get')
    try:
        params = request.args.getlist('parameter')
        s_params = dict(s.parameters)
        r = {}
        for x in params:
            param = s_params.get(x)
            if param is not None:
                if param not in db.session:
                    db.session.merge(param)
                param = param.as_serializable()
            r[x] = param

        ScenarioService.commit() # required because of session update
    except Exception as e:
        logger.error(traceback.format_exc())
        return ApiException(repr(e))
    return ApiResult({'parameters': r})


@scenario_api.route('/api/scenario/<int:scenario_id>/results/', methods=['GET'])
@login_required
def get_last_results(scenario_id):
    logger = make_logger('scenario_last_results_api_get')
    try:
        s = ScenarioService.get(scenario_id)
        start_time = time.time()
        latest_run_info = get_latest_run_info(s)
        logger.info(f"Acquired scenario results in {time.time() - start_time} seconds")
    except Exception as e:
        logger.error(traceback.format_exc())
        return ApiException(repr(e))
    return ApiResult({'latest_run_info': latest_run_info})


@scenario_api.route('/api/scenario/<int:scenario_id>/update', methods=['POST'])
@login_required
def update_scenario(scenario_id):
    logger = make_logger('scenario_api_update')

    try:
        # Get the specified scenario
        s = ScenarioService.get(int(scenario_id))
        scenario_data = request.form.to_dict()
        # print(f"updating with {scenario_data}")

        rv = None
        try:
            rv = handle_scenario_update(s, scenario_data)
        except Exception as e:
            print(f"exception while updating scenario {s} with {scenario_data}:\n")
            print(traceback.format_exc())
            return ApiException(repr(e))

        if rv is not None:
            return ApiResult(rv)
    except Exception as e:
        logger.error(traceback.format_exc())
        return ApiException(repr(e))
    return "success"


@scenario_api.route('/api/scenario/copy', methods=['POST'])
@login_required
def copy_scenario():
    logger = make_logger('scenario_copy_process')
    scenario_data = request.form.to_dict()
    if not scenario_data.get('user_id'):
        raise AssertionError("User ID cannot be blank.")
    if not scenario_data.get('scenario_id'):
        raise AssertionError("Scenario ID cannot be blank.")

    scenario_id = int(scenario_data['scenario_id'])
    user_id = int(scenario_data['user_id'])
    s = ScenarioService.get(scenario_id)

    try:
        copy_start_time = time.time()
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
            rname = new_name[::-1]
            ridx = rname.find("#V_")

        existing_scenario = ScenarioService.get(name=new_name)
        while existing_scenario:
            print(f"The Scenario name {new_name} exists... Generating new name...")
            version = int(rname[:ridx][::-1])
            new_name = rname.replace(rname[:ridx], "", 1)
            new_name = new_name[::-1] + str(version + 1)
            print(f"The new name is {new_name}")
            rname = new_name[::-1]
            ridx = rname.find("#V_")
            existing_scenario = ScenarioService.get(name=new_name)

        ns = ScenarioService.create(name=new_name, description=f'Copy of {s.name} on {datetime.now()}', creator_id=user_id)
        # ScenarioService.commit()

        # Keep track of formulas with hardwired compartment ids. New formulas need to be generated for these with the
        # new compartment ids.
        formulas_with_comp_ids = {}

        # Check formulas for specific compartment ids
        def check_for_comp_ids(par_dict, par):
            if isinstance(par, ParameterDefinition):
                this_formula = par.default_formula
            elif isinstance(par, CustomParameter):
                this_formula = par.formula
            else:
                this_formula = None
            if this_formula:
                f = this_formula
                if f.equation.find("compartment.id") > -1 \
                        or f.equation.find("receiver.id") > -1 \
                        or f.equation.find("sender.id") > -1:
                    par_dict.setdefault(str(par.id), {"par": par, "frm": f})
            return par_dict

        # Add scenario properties/parameters
        cpar_map = {}
        scen_par_start_time = time.time()
        logger.info("Adding scenario Properties")
        for s_par_name, s_par in s.parameters.items():
            if isinstance(s_par, CustomParameter) and s_par.scenario.id == s.id:
                if s_par.id not in cpar_map:
                    ns_par = ParameterService.create(definition=s_par.definition, scenario=ns,
                                        requirements=f"(self.id == {ns.id})", value=s_par.value,
                                        unit=s_par.unit, formula=s_par.formula)
                    cpar_map[str(s_par.id)] = ns_par.id
                formulas_with_comp_ids = check_for_comp_ids(formulas_with_comp_ids, s_par)
                # ParameterService.commit()
        logger.info(f'Copied scenario parameters in {time.time() - scen_par_start_time} seconds')

        # Add scenario chemicals
        logger.info("Adding scenario Chemicals")
        chem_par_start_time = time.time()
        for sc in s.chemicals:
            ns.chemicals.append(sc)
            # ScenarioService.commit()
            # Add Chemical properties/parameters
            for c_par_name, c_par in sc.parameters.items():
                if isinstance(c_par, CustomParameter) and c_par.scenario.id == s.id:
                    if c_par.id not in cpar_map:
                        nc_par = ParameterService.create(definition=c_par.definition, scenario=ns,
                                            requirements=f"(self.id == {sc.id})", value=c_par.value,
                                            unit=c_par.unit, formula=c_par.formula)
                        cpar_map[str(c_par.id)] = nc_par.id
                    formulas_with_comp_ids = check_for_comp_ids(formulas_with_comp_ids, c_par)
                    # ParameterService.commit()
        logger.info(f'Copied chemical parameters in {time.time() - chem_par_start_time} seconds')

        logger.info(f'Finding static compartment ids in parameter formulas')
        chk_par_start_time = time.time()
        # check volume element parameters for hardwired ids.
        for ve in s.volume_elements:
            for vpr_name, vpr in ve.parameters.items():
                if isinstance(vpr, CustomParameter) and vpr.scenario.id == s.id:
                    formulas_with_comp_ids = check_for_comp_ids(formulas_with_comp_ids, vpr)

        # check compartment parameters for hardwired ids.
        for cmp in s.compartments:
            for pr_name, pr in cmp.parameters.items():
                if isinstance(pr, CustomParameter) and pr.scenario.id == s.id:
                    formulas_with_comp_ids = check_for_comp_ids(formulas_with_comp_ids, pr)
        logger.info(f'Found static compartment ids in {len(formulas_with_comp_ids)} parameter formulas in {time.time() - chk_par_start_time} seconds')

        # Create new parcels
        cmp_map = {}
        cp_all_start_time = time.time()
        for prc in s.parcels:
            np = ParcelService.create(name=prc.name, description=prc.description, scenario_id=ns.id, vertices=prc.vertices)
            start_time = time.time()
            # ParcelService.commit()
            # Create new volume elements
            for ve in prc.volume_elements:
                nve = VolumeElementService.create(name=ve.name, parcel_id=np.id, top=ve.top, bottom=ve.bottom)
                # VolumeElementService.commit()
                # Create new volume element parameters
                for ve_parn, ve_par in ve.parameters.items():
                    if isinstance(ve_par, CustomParameter) and ve_par.id not in cpar_map:
                        nve_par = ParameterService.create(definition=ve_par.definition, scenario=ns,
                                                requirements=f"(self.id == {nve.id})", value=ve_par.value,
                                                unit=ve_par.unit, formula=ve_par.formula)
                        cpar_map[str(ve_par.id)] = nve_par.id
                # Create new compartments
                for cmp in ve.compartments:
                    ncmp = CompartmentService.create(name=cmp.name, volume_element=nve, media=cmp.media)
                    cmp_map[str(cmp.id)] = str(ncmp.id)
                    # CompartmentService.commit()
                    # Create new custom parameters for compartments

                    # custom_comp_objects = {}
                    # for cp_obj in [cpar_obj for cpar_name, cpar_obj in cmp.parameters.items() if isinstance(cpar_obj, CustomParameter) and cpar_obj.id not in cpar_map]:
                    #     formula_id = cp_obj.formula.id if cp_obj.formula else None
                    #     new_cp_obj = {'ncpar': CustomParameter(definition=cp_obj.definition,
                    #                                            definition_id=cp_obj.definition.id,
                    #                                            scenario=ns,
                    #                                            scenario_id=ns.id,
                    #                                            requirements=f"(self.id == {ncmp.id})",
                    #                                            value=cp_obj.value,
                    #                                            unit=cp_obj.unit,
                    #                                            formula=cp_obj.formula,
                    #                                            formula_id=formula_id),
                    #                   'cp_id': cp_obj.id}
                    #     custom_comp_objects[str(new_cp_obj['ncpar'].id)] = new_cp_obj
                    #
                    # # Fast bulk insert new custom parameter rows
                    # db.session.bulk_save_objects([obj['ncpar'] for _, obj in custom_comp_objects.items()])
                    #
                    # for nc_id, cpar in custom_comp_objects.items():
                    #     cpar_map[cpar['cp_id']] = nc_id

                    # Slow insert new custom parameter rows one-by-one
                    for parn, cpar in cmp.parameters.items():
                        if isinstance(cpar, CustomParameter) and cpar.id not in cpar_map and cpar.scenario.id == s.id:
                            ncpar = ParameterService.create(definition=cpar.definition, scenario=ns,
                                                            requirements=f"(self.id == {ncmp.id})", value=cpar.value,
                                                            unit=cpar.unit, formula=cpar.formula)
                            cpar_map[str(cpar.id)] = ncpar.id
                            # ParameterService.commit()

                logger.info(f"Finished copying {ve.name} for {prc.name}")
            logger.info(f"{5*'<'} Finished copying {prc.name} in {time.time() - start_time} seconds {5*'>'}\n")
        logger.info(f"Copied all components in {time.time() - cp_all_start_time} seconds\n")

        # Check if we have a parameter with formula that has the hardwired ids found above.
        logger.info("Fixing Formulas with Static Compartment ids ...")
        fix_par_start_time = time.time()

        for old_par_id in formulas_with_comp_ids:
            new_par_id = cpar_map[str(old_par_id)]
            # replace all old compartment ids with new compartment ids
            old_formula = formulas_with_comp_ids[str(old_par_id)]["frm"].equation
            # regular expression to find the id lists in the formula
            regex = re.compile("(?:(?:receiver|compartment|sender)\.id\sin\s{([\,\s\d+]+))")
            old_id_lists = regex.findall(old_formula)
            r_map = []
            for ol in old_id_lists:
                nl = ol
                for old_cmp_id in cmp_map:
                    # iteratively find and replace old ids with new ids in id-list string
                    nl = re.sub(r'(,\s' + str(old_cmp_id) + '\s,)', ", " + str(cmp_map[old_cmp_id]) + " ,", nl)
                    nl = re.sub(r'(^' + str(old_cmp_id) + '\s,)', str(cmp_map[old_cmp_id]) + " ,", nl)
                    nl = re.sub(r'(, ' + str(old_cmp_id) + '$)', ", " + str(cmp_map[old_cmp_id]), nl)
                    nl = re.sub(r'(^' + str(old_cmp_id) + '$)', str(cmp_map[old_cmp_id]), nl)
                    # if str(old_cmp_id) == ol:  # in case we encounter a case like compartment.id in {12}
                    #     nl = nl.replace(f'{str(old_cmp_id)}', f'{str(cmp_map[old_cmp_id])}')
                # print(f'old list is {ol}\nnew list is {nl}')
                r_map.append((ol, nl))

            # create new formula to be used next
            new_formula = old_formula
            for rm in r_map:
                new_formula = new_formula.replace(rm[0], rm[1])
            # print(f'{40*"*"}\nOLD FORMULA: {old_formula}\nNEW FORMULA: {new_formula}')
            new_formula_obj = FormulaService.create(equation=new_formula)
            # assign new formula to the new parameter
            new_par = ParameterService.get(id=new_par_id)
            # print(f'New par: {new_par}\nNew par_id: {new_par.id}\n{40 * "*"}')
            new_par.formula_id = new_formula_obj.id
        logger.info(f'Fixed static compartment ids in parameters in {time.time() - fix_par_start_time} seconds')
        ParameterService.commit()

        # Create the compartment links using the compartment id map
        # logger.info("Copying Compartment Links ...")
        # lnk_cp_start_time = time.time()
        # for lnk in CompartmentService.links.get_all():
        #     if lnk.sender_id in cmp_map.keys():
        #         CompartmentService.links.create(sender_id=cmp_map[lnk.sender_id], receiver_id=cmp_map[lnk.receiver_id])
        # logger.info(f'Copied compartment links in {time.time() - lnk_cp_start_time} seconds')
        # CompartmentService.commit()

        ll = {c.standard_name: {'sender': c,
                                'receiver': c.custom_linked_compartments,
                                'clinks': [
                                    CompartmentService.links.get(sender_id=c.id, receiver_id=cc.id) for cc in c.custom_linked_compartments
                                ]
                                } for c in s.compartments if len(c.custom_linked_compartments) > 0}

        for l, ld in ll.items():
            sender_1 = [c for c in ns.compartments if c.standard_name == l][0]
            for r1 in ld['receiver']:
                receiver_1 = [c for c in ns.compartments if c.standard_name == r1.standard_name][0]
                ccl = CompartmentService.links.get(sender_id=sender_1.id, receiver_id=receiver_1.id)
                if not ccl:
                    print(f'CREATING A NEW LINK in SCENARIO {receiver_1.volume_element.parcel.scenario.name} with sender_id:{sender_1.id} and receiver_id {receiver_1.id}')
                    CompartmentService.links.create(sender_id=sender_1.id, receiver_id=receiver_1.id)
                else:
                    print(
                        f'A CUSTOM LINK ALREADY EXISTS in SCENARIO {receiver_1.volume_element.parcel.scenario.name} with sender_id:{sender_1.id} and receiver_id {receiver_1.id}')
            CompartmentService.commit()

    except Exception as e:
        logger.error(traceback.format_exc())
        logger.error(e)
        logger.info("Failed to copy scenario...")
    finally:
        logger.info(f"Copy operation {s.name} -> {ns.name} completed in {time.time() - copy_start_time} seconds!")
        ScenarioService.commit()

    # return ApiResult({'result': res})
    return redirect(request.referrer)


@scenario_api.route('/api/scenario/delete/', methods=['POST'])
@login_required
def delete_scenario():
    logger = make_logger('scenario_delete_process')
    scenario_data = request.form.to_dict()
    if not scenario_data.get('scenario_id'):
        raise AssertionError("Scenario ID cannot be blank.")

    scenario_id = int(scenario_data['scenario_id'])
    s = ScenarioService.get(scenario_id)

    try:
        # Delete compartment custom parameters
        for cmp in s.compartments:
            for cmp_par_name, cmp_par in cmp.parameters.items():
                if isinstance(cmp_par, CustomParameter):
                    ParameterService.delete(cmp_par)
                    logger.info(f'Deleted custom par {cmp_par_name} for {cmp.name}...')

        # Delete chemical custom parameters
        for sc in s.chemicals:
            sc.current_scenario(s)
            # TODO: Currently the chemical parameters are not correctly acquired with sc.parameters (it gets the first
            #  custom parameter from the list of custom parameters for that parameter definition. That is the parameter
            #  for a different scenario!!! Apparently, setting current scenario for the chemical does not help to get
            #  desired custom parameter belonging to the correct scenario...
            for c_par_name, c_par in sc.parameters.items():
                if isinstance(c_par, CustomParameter):
                    # NOTE: below is a workaround for the chemical.current_scenario problem described above
                    par = ParameterService.get(scenario_id=s.id, definition_id=c_par.definition.id,
                                               requirements=f'(self.id == {sc.id})')
                    if par:
                        ParameterService.delete(par)
                        logger.info(f'Deleted chemical custom par {par.definition.name} for {sc.name}...')

            # Remove the scenario chemical
            s.chemicals.remove(sc)
            # ScenarioService.commit()

        # Delete scenario custom parameters
        for s_par_name, s_par in s.parameters.items():
            if isinstance(s_par, CustomParameter) and s_par.scenario.id == s.id:
                ParameterService.delete(s_par)
                logger.info(f'Deleted scenario custom par {s_par_name} for {s.name}...')
        # ParameterService.commit()

        # Delete all parcels and contents
        for parcel in s.parcels:
            for c in parcel.compartments:
                # Delete Links
                comp_id = c.id
                lr = CompartmentService.links.get_all(receiver_id=comp_id)
                ls = CompartmentService.links.get_all(sender_id=comp_id)
                for lnk_r in lr:
                    CompartmentService.links.delete(lnk_r)
                for lnk_s in ls:
                    CompartmentService.links.delete(lnk_s)

                # Delete Compartments
                CompartmentService.delete(c, False)

            # Delete volume elements
            for ve in parcel.volume_elements:
                VolumeElementService.delete(ve, False)

            # Delete some custom parameters that may be left behind for this scenario
            # (they may be for domains other than compartment)
            scen_custom_params = [p for p in ParameterService.get_all() if p.scenario.id == s.id]
            for s_cp in scen_custom_params:
                ParameterService.delete(s_cp)

            # Delete parcel
            ParcelService.delete(parcel.id)
            logger.info(f'Deleted parcel {parcel.name} for {s.name}...')
        # ParcelService.commit()

        # Delete scenario Proc info
        s_proc = [sp for sp in s.proc_status]
        if len(s_proc) > 0:
            for sp in s_proc:
                logger.info(f'Deleted result {sp.id} for {s.name}...')
                ScenarioService.db.session.delete(sp)

        # Delete scenario
        ScenarioService.delete(s.id)
        logger.info(f'Deleted scenario {s.name}...')
        # ScenarioService.commit()
    except Exception as e:
        print(e)
        print("Failed to delete scenario...")
    finally:
        ScenarioService.commit()

    return redirect(request.referrer)


@scenario_api.route('/api/scenario/clearresult/', methods=['POST'])
@login_required
def clear_old_result():
    exec_data = request.form.to_dict()
    if not exec_data.get('scenario_id'):
        raise AssertionError("Scenario ID cannot be blank.")
    scenario_id = int(exec_data['scenario_id'])
    scn = ScenarioService.get(scenario_id)

    data_resp = {"success": "success"}
    try:
        if scn.has_process_hist:
            print(f"Clearing Last Model Run for {scn.name} {scn.proc_status.all()[-1].run_datetime}...")
            scn.proc_status.remove(scn.latest_proc_status)
            ScenarioService.commit()
    except Exception as e:
        print(f'problem deleting {e}')
        return ApiException(f"Problem deleting {repr(e)}")
    
    print(f"Model Result deleted for {scn.name}")
    ScenarioService.commit()
    return ApiResult(data_resp)


@scenario_api.route('/api/scenario/run/', methods=['POST', 'GET'])
@login_required
def run_result_scenario():
    trim_env_profile = os.environ.get("TRIM_ENV_PROFILE", "").lower()

    exec_data = request.form.to_dict()
    if not exec_data.get('scenario_id'):
        raise AssertionError("Scenario ID cannot be blank.")
    scenario_id = int(exec_data['scenario_id'])

    try:
        # in dev/prod, we execute an AWS StepFunction to run the model via Docker/ECS. Locally,
        # we just run the model directly.
        if trim_env_profile in [ "dev", "devgetflow", "prod" ]:
            sfn_client = boto3.client("stepfunctions")
            state_machine_arn = os.environ.get("TRIM_DOCKERIZED_RUNMODEL_STATEMACHINE_ARN")

            if state_machine_arn is not None:
                resp = sfn_client.start_execution(
                    stateMachineArn=state_machine_arn,
                    input=json.dumps({ "scenarioId": str(scenario_id), "generateFakeResults": "false" })
                )
                data_resp = { "executionArn": resp["executionArn"] }
            else:
                data_resp = { "error": "Missing required variable to run re-architected model" }
        else:
            s = ScenarioService.get(scenario_id)
            print(f"Starting Model Run ({datetime.now()}) ...")
            json_n_avg, json_c_avg, output_file_n, output_file_c, output_file_tm = run_full_model(s)
            data_resp = {"mass": json_n_avg, "conc": json_c_avg, "outputMass": output_file_n,
                         "outputConc": output_file_c, "outputTM": output_file_tm}
    except Exception as e:
        print('scenario run error:', e)
        data_resp = {"error": e}

    print(f"Model Run Finished ({datetime.now()}) ...")

    return ApiResult(data_resp)


@scenario_api.route('/api/scenario/getresults/', methods=['POST'])
@login_required
def get_result_scenario():
    logger = make_logger('scenario_get_results_process')
    exec_data = request.form.to_dict()
    if not exec_data.get('scenario_id'):
        raise AssertionError("Scenario ID cannot be blank.")
    scenario_id = int(exec_data['scenario_id'])
    s = ScenarioService.get(scenario_id)

    try:
        logger.info(f'Getting Model Run Results for scenario {s.name}...')
        fin_stat = s.latest_proc_status.run_status
        run_date = s.latest_proc_status.run_datetime
        output_file_n = Path(s.latest_proc_status.result_file_nt).name
        output_file_c = Path(s.latest_proc_status.result_file_conc).name
        output_file_t = Path(s.latest_proc_status.result_file_tm).name
        json_n_avg = s.latest_proc_status.result_nt
        json_c_avg = s.latest_proc_status.result_conc
        trim_data = compile_mirc_data(s, s.latest_proc_status, logger)
        result_resp = json.loads(json.dumps({
            "mass": json.loads(json_n_avg), 
            "conc": json.loads(json_c_avg), 
            "final_status": fin_stat, 
            "run_date": run_date, 
            "outputMass": output_file_n, 
            "outputConc": output_file_c, 
            "outputTM": output_file_t,
            "trim_data": trim_data
        }, indent=4, sort_keys=True, default=str))

    except Exception as e:
        logger.info(f"Error when attempting to get results: {e}")
        result_resp = {"error": e}
    try:
        resp = ApiResult(result_resp)
    except Exception as e:
        resp = ""
        logger.error(f'Api result conversion error: {e}')
    return resp

@scenario_api.route('/api/scenario/poll/<int:id>', methods=['GET'])
@login_required
def poll_model_run_scenario(id):
    s = ScenarioService.get(id)
    if s.has_process_hist:
        if s.latest_proc_status.is_run_error:
            run_status = "err"
            run_percent = "err"
        else:
            run_status, run_percent = [v for v in s.proc_status][0].run_step
        print(f"Poll status for scenario {s.name} is {run_status} at {run_percent}%")
        return ApiResult({'status': run_status, 'percent': run_percent})
    print(f"Poll status for scenario {s.name} is 'tm' at 0%")
    return ApiResult({'status': "tm", 'percent': "0"})


@scenario_api.route('/api/scenario/poll/', methods=['POST'])
@login_required
def reset_poll_model_run_scenario():
    scenario_data = request.form.to_dict()
    if not scenario_data.get('scenario_id'):
        raise AssertionError("Scenario ID cannot be blank.")
    scenario_id = int(scenario_data['scenario_id'])
    s = ScenarioService.get(scenario_id)
    if s.has_process_hist:
        s.latest_proc_status.run_status = 'run null null'
    else:
        new_proc = ScenarioLoadRunProc(scenario=s, load_status='load 100', run_status='run null null')
        s.proc_status.add(new_proc)
    ScenarioService.commit()
    return "success"


def get_complete_logs_from_group_and_stream(log_group, log_stream):
    logs_client = boto3.client("logs")

    # retrieve logs from CloudWatch.
    # note this does NOT do anything smart with pagination -- just returns everything in one shot
    # nice future enhancement might be to return a subset of this that we've deemed fit for public consumption; that could then
    # be something we display to all users, not just internal ICF'ers

    # also note - the pagination on this call is truly strange. According to the docs, you only know that pagination on the response
    # from get_log_events is done if the "nextXToken" in the response is equivalent to the "nextToken" passed in in your request. (the next/prev
    # tokens that are returned are never null).
    #
    # In my tests I was seeing things like:
    # 1. make first call, get all the logs
    # 2. make second call with the "nextToken" from call 1 (have to, as programatically I don't know that's the end). This returns empty array - but a non-matching end token
    # 3. make third call with "nextToken" from call 2 (since they didn't match). Again, empty array, but this time they match and I can stop.
    #
    # Adding a sanity check just in case, to break after some number of attempts

    sanity = 0
    rv = []
    next_token = None
    while True:
        if sanity > 10:
            break

        params = {
            "logGroupName": log_group,
            "logStreamName": log_stream,
            "startFromHead": True,
        }

        if next_token is not None:
            params["nextToken"] = next_token

        print(f"CALL ITERATION {sanity} w/ params {params}...")

        logs_response = logs_client.get_log_events(**params)
        log_events = logs_response["events"]

        for e in log_events:
            rv.append({
                "timestamp": e["timestamp"],
                "message": e["message"]
            })

        if next_token is not None and logs_response["nextForwardToken"] == next_token:
            print(f"safe to break; got same token we passed in...")
            break
        else:
            print(f"need to keep going...")
            next_token = logs_response["nextForwardToken"]

        sanity += 1

    return rv


def fetch_output_for_step_function_execution(execution_arn):
    # build boto3 clients we need
    sfn_client = boto3.client("stepfunctions")
    ecs_client = boto3.client("ecs")

    try:
        # get the details of the execution...
        exec_hist_response = sfn_client.get_execution_history(executionArn=execution_arn)

        # get the specific event relating to kickoff of the Docker container... 
        ecs_task_event = next((e for e in exec_hist_response["events"] if e.get("type") == "TaskSubmitted" and e.get("taskSubmittedEventDetails", {}).get("resourceType") == "ecs"), None)
        # re-parse the details/output, included as a JSON string in the boto3 reply... 
        output = json.loads(ecs_task_event.get("taskSubmittedEventDetails", {}).get("output", "{}"))

        # get the ECS task id
        tasks = output.get("Tasks", [])

        task = tasks[0] if len(tasks) > 0 else None
        task_arn = task.get("TaskArn")
        task_key = task_arn.split("/")[-1]

        taskdef_arn = task.get("TaskDefinitionArn")
        def_resp = ecs_client.describe_task_definition(
            taskDefinition=taskdef_arn,
            include=[ 'TAGS', ]
        )

        # construct log group/stream relating to this execution
        log_group=def_resp["taskDefinition"]["containerDefinitions"][0]["logConfiguration"]["options"]["awslogs-group"]
        log_stream=f"ecs/{def_resp['taskDefinition']['containerDefinitions'][0]['name']}/{task_key}"

        print(f"let's use {log_group=} / {log_stream=}...")

        return get_complete_logs_from_group_and_stream(log_group, log_stream)
    except Exception as e:
        return [ f"Error fetching logs: {e}" ]


@scenario_api.route('/api/scenario/check_execution_completion/', methods=['POST'])
@login_required
def check_execution_completion():
    req_data = request.form.to_dict()
    if not req_data.get('execution_arn'):
        raise AssertionError("execution ARN cannot be blank.")

    execution_arn = req_data['execution_arn']

    sfn_client = boto3.client("stepfunctions")

    debug_messages = fetch_output_for_step_function_execution(execution_arn) if current_user.email.lower().endswith("@icf.com") else [ "debug output disabled for external users" ]

    desc_resp = sfn_client.describe_execution(executionArn=execution_arn)
    if desc_resp["status"] == "SUCCEEDED":
        resp = {
            "success": True,
            "sfn_output": json.loads(desc_resp["output"]),
            "debug_messages": debug_messages
        }
    else:
        # success should still be True b/c we didn't fail; we're just not done yet...
        # calling client will just wait and retry.
        resp = {
            "success": True,
            "sfn_output": False,
            "debug_messages": debug_messages
        }

    return ApiResult(resp)


# downloads the output from a model run and creates presigned url's for the xlsx files
@scenario_api.route('/api/scenario/fetch_run_results/', methods=['POST'])
@login_required
def fetch_run_results():
    req_data = request.form.to_dict()
    if not req_data.get('bucket') or not req_data.get('uuid'):
        raise AssertionError("bucket/uuid cannot be blank.")

    bucket = req_data['bucket']
    uuid = req_data['uuid']

    s3_client = boto3.client("s3")
    s3_resource = boto3.resource("s3")

    content_object = s3_resource.Object(bucket, f"{uuid}/model_output.json")
    file_content = content_object.get()["Body"].read().decode("utf-8")
    json_content = json.loads(file_content)

    resp = {
        "success": True,
        "model_output": json_content
    }

    for f in ["outputMass", "outputConc", "outputTM"]:
        full_key = f"{uuid}/{f}.xlsx"
        response = s3_client.generate_presigned_url("get_object",
                                                    Params={
                                                        "Bucket": bucket,
                                                        "Key": full_key
                                                    },
                                                    ExpiresIn=600) # expires in 10 minute(s)

        resp[f] = response


    return ApiResult(resp)


@scenario_api.route(
    '/api/scenario/<int:scenario_id>/run_getflow', methods=['POST']
)
@login_required
def run_getflow(scenario_id):
    """
    flow is as follows:
    * gui_surface_runoff.html is the template for the url /scenario/{id}/edit?default_runoff_matrix_file=#surface_runoff-tab
    * clicking "Run GetFlow" btn runs a small JavaScript function defined in that html file
    * that function calls api.runGetFlow, defined in api.js. That packages some stuff up and hits
      /api/scenario/{id}/run_getflow
    * that's this function! This now kicks off a Step Function and returns the execution arn or whatever
    """
    trim_env_profile = os.environ.get("TRIM_ENV_PROFILE", "").lower()

    print(f"TOM in run_getflow within routes.py, env==[{trim_env_profile}]...")
    print(f"scenario id is [{scenario_id}] / {type(scenario_id)}")
    print(f"data is ?!?!!?")

    s = ScenarioService.get(scenario_id)
    if not s:
        return ApiException("Unknown Scenario")

    print(f"scenario: {s}")

    print(f"Starting/Kicking Off GetFlow Run ({datetime.now()}...")
    try:
        # unlike runmodel, here we use ECS even when running locally. (getting a working qgis
        # install is non-trivial, but if you wanted to run local you'd need to do that, then
        # modify this section of code to do something like "run_result_scenario".
        if True or trim_env_profile in [ "dev", "devgetflow", "prod" ]:
            sfn_client = boto3.client("stepfunctions")
            state_machine_arn = os.environ.get("TRIM_DOCKERIZED_GETFLOW_STATEMACHINE_ARN")

            print(f"arn is '{state_machine_arn}'")

            if state_machine_arn is not None:
                resp = sfn_client.start_execution(
                    stateMachineArn=state_machine_arn,
                    input=json.dumps({ "scenarioId": str(scenario_id), "generateFakeResults": "false" })
                )
                data_resp = { "executionArn": resp["executionArn"] }
                # data_resp = { "to": "do" }
            else:
                data_resp = { "error": "Missing required envrionment variable to run getflow" }

            print(f"Back (Kicked Off) ({datetime.now()}...")
        else:
            data_resp = {"not": "implemented!"}
    except Exception as e:
        print('getflow kickoff exception:', e)
        data_resp = {"error": repr(e)}

    return ApiResult(data_resp)


@scenario_api.route(
    '/api/stepfxn_check', methods=['POST']
)
@login_required
def check_stepfunction_status():
    print(f"checking stepfxn status...")
    print(request.form.to_dict())

    execution_arn = request.form.to_dict().get("arn")

    if execution_arn is None:
        data_resp = {"error": "no execution arn supplied"}
    else:
        try:
            sfn_client = boto3.client("stepfunctions")
            resp = sfn_client.describe_execution(
                executionArn=execution_arn
            )
            data_resp = {
                "status": resp.get("status")
            }

            if resp.get("status", "").upper() == "SUCCEEDED":
                data_resp["output"] = {}

                stepfxn_output = resp.get("output")
                print(f"RAW OUTPUT: {stepfxn_output}")
                parsed = json.loads(stepfxn_output)
                for key in parsed:
                    data_resp["output"][key] = parsed[key]



        except Exception as e:
            data_resp = {"error": str(e) }

    return ApiResult(data_resp)


@scenario_api.route('/api/scenario/<int:scenario_id>/export/mirc', methods=['GET'])
# TODO: Need some way for MIRC *app* to authenticate?
@login_required
def export_for_mirc(scenario_id):
    scen = ScenarioService.get(scenario_id)
    if not scen:
        return ApiException("Unknown Scenario")

    logger = make_logger('mirc_exporter')
    try:
        latest_model_run = scen.latest_proc_status
        trim_data = compile_mirc_data(scen, latest_model_run, logger)
    except Exception as e:  
        logger.error(e)
        traceback.print_exc()
        trim_data = {"message": "No valid data found"}

    return ApiResult({trim_data})


@scenario_api.route(
    '/api/scenario/<int:scenario_id>/run_receptor_generation', methods=['POST']
)
@login_required
def run_receptor_generation(scenario_id):
    """
    flow is as follows:
    * parcels.html is the template for the url /scenario/{id}/edit#parcels-tab
    * clicking the btn in the "Receptor Spacing" column runs a small JavaScript function defined in that html file
    * that function calls api.runReceptorGeneration, defined in api.js. That packages some stuff up and hits
      /api/scenario/{id}/run_receptor_generation
    * that's this function! This blah blah
    """

    scen = ScenarioService.get(scenario_id)

    try:
        all_calculations = []
        for parcel in scen.parcels:
            grid_points_etc = calculate_receptor_grid_points_for_parcel(parcel)
            all_calculations.append(grid_points_etc)

        fv = MiscAssociatedFileVariety.construct_file_variety("generated_aermod_receptors")
        file_like_obj = fv.convert_grid_point_data_to_binary_geojson(all_calculations)

        data_resp = {}
        
        upload_data = associated_file_helper(scenario_id, "generated_aermod_receptors", "UPLOAD", file_obj = file_like_obj, file_metadata={})
        data_resp = upload_data
    except Exception as e:
        traceback.print_exc()
        return ApiException(repr(e))

    return ApiResult(data_resp)


@scenario_api.route(
    "/api/scenario/<int:scenario_id>/chemical/properties", methods=["GET"]
)
@login_required
def get_chemical_properties(scenario_id):
    logger = make_logger('chemical_properties')
    logger.info("Pulling chemical properties...")

    scen = ScenarioService.get(scenario_id)
    comps = scen.compartments

    chem_properties = {}

    def serialize_value(value, param):
        v = None
        u = None
        if isinstance(value, pint.Quantity):
            v = value.magnitude
            u = param.unit
        else:
            v = value
        if isinstance(v, float):
            # Round value
            if v < 1:
                v = float(f'{v:.12f}')
            else:
                v = float(f'{v:.4f}')

        return {
            "value": v,
            "unit": u
        }

    def get_prop_name(param):
        return param.variable_name

    def add_prop(chem_name, scope, param, value, restriction=None):
        if chem_name not in chem_properties:
            chem_properties[chem_name] = {}
        if scope not in chem_properties[chem_name]:
            chem_properties[chem_name][scope] = {}

        prop_name = get_prop_name(param)

        if prop_name not in chem_properties[chem_name][scope]:
            chem_properties[chem_name][scope][prop_name] = {
                "name": prop_name,
                **serialize_value(value, param)
            }

        if restriction is not None:
            if 'options' not in chem_properties[chem_name][scope][prop_name]:
                chem_properties[chem_name][scope][prop_name]['options'] = {}
            opts = chem_properties[chem_name][scope][prop_name]['options']
            for k, val in restriction.items():
                opts[k] = serialize_value(val, param)

    def get_by_compartment(param, chem, fn=None):
        prop_name = get_prop_name(param)
        var_name = param.variable_name
        chem_name = chem.name
        for comp in comps:
            scope = f'Compartment [{comp.media.name}]'
            if (
                chem_name in chem_properties
                and scope in chem_properties[chem_name]
                and prop_name in chem_properties[chem_name][scope]
            ):
                continue
            try:
                if fn is None:
                    comp_fn = comp.parameters.evaluate(var_name)
                    if isinstance(comp_fn, types.FunctionType):
                        try:
                            val = comp_fn(chem)
                        except Exception as e:
                            # print('\t-', e)
                            continue
                    else:
                        val = comp_fn
                else:
                    val = fn(comp)
                # print('\t>', val)
                add_prop(
                    chem_name, scope, param, val,
                    restriction={comp.standard_name: val}
                )
            except Exception as e:
                # print('\t-', e)
                pass

    def is_recursive(param):
        if param.formula is None:
            return False
        eq = param.formula.equation
        if f'self.{param.variable_name}(' in eq:
            return True
        if f'self.{param.variable_name}.' in eq:
            return True
        if f'self.{param.variable_name} ' in eq:
            return True
        return False

    try:
        for chem in scen.chemicals:
            # print('\n========================================')
            # print(chem)
            # print('----------------------------------')
            chem_name = chem.name
            for param_name, param in chem.parameters.items():
                # print('~', param_name)
                if is_recursive(param):
                    logger.error(
                        f'Chemical Parameter "{param_name}" is recursively defined!'
                    )
                    if param_name == 'initialConcentration':
                        # DISABLED FOR NOW - SEE BELOW
                        # logger.warning(f'Using compartment "{param_name}" instead ...')
                        # get_by_compartment(param, chem)
                        pass
                    else:
                        logger.warning(f'Skipping parameter "{param_name}" ...')
                    continue

                val = chem.parameters.evaluate(param)
                scope = None
                if not isinstance(val, types.FunctionType):
                    # print('\t>', val)
                    add_prop(chem_name, 'Scenario', param, val)
                else:
                    try:
                        val = val()
                        # print('\t>', val)
                        add_prop(chem_name, 'Scenario', param, val)
                        continue
                    except Exception as e:
                        # print('\t-', e)
                        pass
                    # DISABLED FOR NOW - MAYBE LATER?
                    # - we want to figure out a way to display the formulas (too?)
                    # get_by_compartment(param, chem, fn=val)
    except Exception as e:
        import traceback; traceback.print_exc()
    return ApiResult(chem_properties)
