import json
import os
import re
import time
import pint
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
from trim_db.services.parameters import get_or_create_custom_param
from trim_frontend import api, db
from trim_frontend.scenarios.utils import init_first_time_default_param_values, init_erosion_default_params
from trim_frontend.parcels.routes import delete_parcel_contents
from .defaults import *
from .forms import *
from ..utils.logging import make_logger
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
    s = ScenarioService.get(id)
    start_time = time.time()
    s = s.as_serializable()
    init_erosion_default_params()
    logger.info(f"Acquired scenario in {time.time() - start_time} seconds")
    return ApiResult({'scenario': s})


@scenario_api.route(
    '/api/scenario/<int:scenario_id>/chemical', methods=['GET']
)
@login_required
def get_scenario_chemicals(scenario_id):
    s = ScenarioService.get(scenario_id)
    if not s:
        raise ApiException("Unknown Scenario")
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
        print(e)
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
    s = ScenarioService.get(scenario_id)
    start_time = time.time()
    runoff_matrix = get_surface_runoff(s)
    logger.info(f"Acquired runoff matrix in {time.time() - start_time} seconds")
    return ApiResult({'runoff_matrix': runoff_matrix})


@scenario_api.route(
    '/api/scenario/<int:scenario_id>/parameter',
    methods=['GET']
)
@login_required
def get_parameters(scenario_id):
    s = ScenarioService.get(scenario_id)
    if not s:
        raise ApiException("Unknown Scenario")

    params = request.args.getlist('parameter')
    s_params = dict(s.parameters)
    r = {}
    for x in params:
        param = s_params.get(x)
        if param is not None:
            db.session.add(param)
            param = param.as_serializable()
        r[x] = param

    ScenarioService.commit() # required because of session update
    return ApiResult({'parameters': r})


@scenario_api.route('/api/scenario/<int:scenario_id>/results/', methods=['GET'])
@login_required
def get_last_results(scenario_id):
    logger = make_logger('scenario_last_results_api_get')
    s = ScenarioService.get(scenario_id)
    start_time = time.time()
    latest_run_info = get_latest_run_info(s)
    logger.info(f"Acquired scenario results in {time.time() - start_time} seconds")
    return ApiResult({'latest_run_info': latest_run_info})


@scenario_api.route('/api/scenario/update', methods=['POST'])
@login_required
def update_scenario():
    logger = make_logger('scenario_api_update')
    ret_val = ''

    def create_new_custom_param_meteo(scen, comp, par_name):
        print(f"\n{par_name}\n")
        default_param = ParameterService.definitions.get_all(variable_name=par_name)
        
        if par_name == "AirTemperature":
            default_param = ParameterService.definitions.get(variable_name=par_name, default_unit="K")
        elif par_name == "WetDepInterceptionFraction_UserSupplied":
            default_param = ParameterService.definitions.get_all(variable_name=par_name, 
                                                                 domain=ParameterService.domains.get(name="Compartment"))
            default_param = default_param[0]
        elif len(default_param) > 1: 
            print(f"\tTried to create new custom parameter but multiple defaults found!\n{default_param}")
            default_param = default_param[0]
        else:
            default_param = default_param[0]

        return get_or_create_custom_param(
            default_param,
            {"requirements": f"(self.id == {comp.id})", "scenario_id": scen.id},
        )

    def create_litterfallrate_custom_param(scen, comps, par_name):
        # FIXME shouldn't use this eventually, maybe just create for all media?
        # step 1 grab the right compartments by media name, using a hardcoded map
        comp_media = [
            "Leaf_Grasses_Herbs", # Grass
            "Leaf_Deciduous_Forest" # Deciduous forest
        ]
        filtered_comps = [c for c in comps if c.name in comp_media]
        if not filtered_comps:
            filtered_comps = comps

        # step 2 grab the correct default param
        default_param = ParameterService.definitions.get(variable_name=par_name, 
                                                            domain=ParameterService.domains.get(name="Compartment"))
        
        # step 3 create new custom param for each of the identified compartments (per parcel)
        custom_params = []
        for comp in filtered_comps:
            custom_params.append(
                get_or_create_custom_param(
                    default_param,
                    {"requirements": f"(self.id == {comp.id})", "scenario_id": scen.id},
                    no_commit=True
                )
            )
        ParameterService.commit()
        return custom_params

    def update_custom_param(scen, comp, par_name, par_val, create_if_dne = False):
        par_list = [p for p in scen.custom_params if
                    p.definition.variable_name == par_name and f'self.id == {comp.id}' in p.requirements]
        
        if not par_list and create_if_dne:
            par_list.append(create_new_custom_param_meteo(scen, comp, par_name))

        for c_p in par_list:
            c_p.value = par_val
            ParameterService.update(c_p)
        ParameterService.commit()

    def update_assumed_all_comp_fixed_params(scen, comps, par_name, par_val):
        # media_name = comp.media.name
        # c_par_list = [c.parameters.get(par_name) for c in scen.compartments if c.media.isa(media_name)]
        ParameterService.commit() # for some reason gets open instance errors otherwise
        c_par_list = set(c.parameters.get(par_name) for c in comps if c.parameters.get(par_name))
        c_par_list = [par for par in c_par_list if isinstance(par, CustomParameter)]

        if not c_par_list:
            c_par_list = create_litterfallrate_custom_param(scen, comps, par_name)

        for c_p in c_par_list:
            try:                
                c_p.value = par_val
                ParameterService.update(c_p)
            except AttributeError as e:
                print(e)
        ParameterService.commit()

    def meteo_wgt_avg_value_from_timeseries(par_dat, param_type):
        import pandas as pd
        from numpy import timedelta64

        par_dat = json.loads(par_dat)
        df_met = pd.DataFrame.from_dict(par_dat, orient='columns')

        df_met['dlist'] = df_met['Date'].str.split('/')  # split date column into list
        df_met = df_met[df_met.dlist.str.len() == 3]  # drop rows that have less than three elements
        df_met[['Month', 'Day', 'Year']] = df_met.Date.str.split("/", expand=True)
        df_met['Month'] = pd.to_numeric(df_met['Month'], errors='coerce')
        df_met['Day'] = pd.to_numeric(df_met['Day'], errors='coerce')
        df_met['Year'] = pd.to_numeric(df_met['Year'], errors='coerce')
        hour_col_name = 'xHour' if param_type == "MET" else 'Hour'
        df_met['Hour'] = pd.to_numeric(df_met[hour_col_name], errors='coerce')
        df_met = df_met.loc[
            (df_met.Month < 13) & (df_met.Day < 32) & (df_met.Year < 2100)]  # drop faulty

        if param_type == "MET":
            df_met = df_met.loc[(df_met.Hour < 25)]  # drop faulty
            metcol_dict = {'Rain': (0, 1), 'AirTemperature': (200, 373), 'HorizontalWindSpeed': (0, 100),
                           'WindDirection': (-360, 360), 'MixingHeight': (0, 1000), 'isDay': (0, 1),
                           'CumulativeRain': (0, 1.6)}  # k, v represent name and min-max
            for k, v in metcol_dict.items():
                if 'k' in df_met.columns:
                    df_met['metcol'] = pd.to_numeric(df_met[k], errors='coerce')
                    df_met = df_met[
                        (df_met['metcol'] <= v[1]) & (df_met['metcol'] >= v[0])]  # keep rows within min max bounds

            df_met['DT'] = list(pd.to_datetime(df_met[['Year', 'Month', 'Day', 'Hour']], errors='coerce'))
        else:
            # Ignored hour resolution.
            df_met['DT'] = list(pd.to_datetime(df_met[['Year', 'Month', 'Day']], errors='coerce'))

        df_met.sort_values(by='DT', inplace=True)
        df_met['date_delta'] = (df_met['DT'] - df_met['DT'].min()) / timedelta64(1, 'D')
        df_met['time_delta'] = df_met['date_delta'].diff()
        # shift up the column 1 so that applicability of met condition is aligned to duration
        df_met['time_delta'] = df_met['time_delta'].shift(-1)

        # Clean up non sequential dates
        df_met['DT_Check'] = df_met.DT >= (df_met.DT.shift())
        df_met = df_met[df_met['DT_Check']]

        # Get time-weighted averages
        met_dict = {}
        if param_type == "MET":
            for k, v in metcol_dict.items():
                if k in df_met.columns:
                    df_met['metcol'] = pd.to_numeric(df_met[k], errors='coerce')
                    df_met['prod'] = df_met['metcol'] * df_met['time_delta']
                    wt_ave = df_met['prod'].sum() / df_met['time_delta'].sum()
                    met_dict['wt_av_' + k] = wt_ave

            if 'Rain' in df_met.columns:
                df_met['Rain'] = pd.to_numeric(df_met['Rain'], errors='coerce')
                df_met['is_Rain'] = [1 if x > 0 else 0 for x in df_met['Rain']]
                df_met['RainTime'] = df_met['is_Rain'] * df_met['time_delta']
                rain_frac_time = df_met['RainTime'].sum() / df_met['time_delta'].sum()
                met_dict['frac_time_rain'] = rain_frac_time
        if param_type == "AE":
            # process AE.
            df_met['ae'] = pd.to_numeric(df_met['AllowExchange'], errors='coerce')
            df_met['prod_ae'] = df_met['ae'] * df_met['time_delta']
            wt_ave = df_met['prod_ae'].sum() / df_met['time_delta'].sum()
            met_dict['wt_av_allowexchange'] = wt_ave
        elif param_type == "LF":
            # process LF
            df_met['lf'] = pd.to_numeric(df_met['LitterfallRate'], errors='coerce')
            df_met['prod_lf'] = df_met['lf'] * df_met['time_delta']
            wt_ave = df_met['prod_lf'].sum() / df_met['time_delta'].sum()
            met_dict['wt_av_litterfallrate'] = wt_ave

        return met_dict

    try:
        scenario_data = request.form.to_dict()
        print(scenario_data)
        if not scenario_data['id']:
            raise AssertionError("Scenario ID cannot be blank.")
        # Get the specified parcel
        s = ScenarioService.get(int(scenario_data['id']))

        # Update the specified property
        field_name = scenario_data["field"]
        if field_name == "erosionRateCalcSource":  # Data from erosion tab
            ercs = scenario_data["erosionRateCalcSource"]
            default_ercs = ParameterService.definitions.get(full_name="erosionRateCalcSource")
            ercs_cp = ParameterService.get_or_create(definition=default_ercs, scenario_id=s.id)
            ercs_cp.value = ercs
            # for cp in s.custom_params:
            #     if cp.definition.variable_name == "erosionRateCalcSource":
            #         cp.value = ercs
            ParameterService.commit()
        elif field_name.startswith("meteo_"):  # Data from the meteorology tab
            if "_interception_" in field_name:
                param_media = param_map["meteo"].get(field_name)[0]
                param_name = param_map["meteo"].get(field_name)[1]
                comp_list = [c for c in s.compartments if c.media.isa(param_media)]
                for c in comp_list:
                    # TODO Why is this not working???
                    # c.parameters.get(param_name).value = scenario_data[field_name]
                    # CompartmentService.update(c)
                    update_custom_param(s, c, param_name, scenario_data[field_name], create_if_dne=True)
            else:
                param_name = param_map["meteo"].get(field_name)
                param_data = scenario_data[field_name]
                if "_static_" in field_name:
                    update_custom_param(s, s, param_name, param_data, create_if_dne=True)
                elif field_name.endswith("_TS"):
                    ret_val = meteo_wgt_avg_value_from_timeseries(param_data, "MET")
                    if isinstance(ret_val, dict) and "wt_av_Rain" in ret_val.keys():
                        param_value = ret_val["wt_av_Rain"]
                    elif isinstance(ret_val, dict) and "wt_av_CumulativeRain" in ret_val.keys():
                        param_value = ret_val["wt_av_CumulativeRain"]
                    else:
                        param_value = list(ret_val.values())[0]
                    update_custom_param(s, s, param_name, param_value, create_if_dne=True)

        elif field_name.startswith("seasonal_"):  # Data from the seasonal dynamics tab
            param_media = param_map["seasonal"].get(field_name)[0]
            param_name = param_map["seasonal"].get(field_name)[1]
            param_data = scenario_data[field_name]
            comp_list = [c for c in s.compartments if c.media.isa(param_media)]
            if "_static_" in field_name:
                # update_custom_param(s, comp_list[0], param_name, param_data)
                update_assumed_all_comp_fixed_params(s, comp_list, param_name, param_data)
            elif field_name.endswith("_TS"):
                ret_type = "LF" if field_name.find("_litterfall_") > 0 else "AE"
                ret_type_name = "wt_av_litterfallrate" if field_name.find("_litterfall_") > 0 else \
                    "wt_av_allowexchange" if field_name.find("_allowexchange_") > 0 else "None"
                ret_val = meteo_wgt_avg_value_from_timeseries(param_data, ret_type)
                if ret_type != "None":
                    update_assumed_all_comp_fixed_params(s, comp_list, param_name, ret_val[ret_type_name])
        elif field_name == "simulation_start_date" or field_name == "simulation_end_date":
            date_parts = scenario_data[field_name].split("-")
            date_obj = datetime(int(date_parts[0]), int(date_parts[1]), int(date_parts[2]))
            ts_date = time.mktime(date_obj.timetuple())
            par_name = "simulationBeginDateTime" if field_name == "simulation_start_date" else "simulationEndDateTime"
            par_list = {par_k: par for par_k, par in s.parameters.items() if par_k == par_name}
            this_param = par_list.get(par_name)
            if this_param is None:
                s.parameters.add(par_name, value=ts_date)
            elif this_param.__tablename__ != "custom_parameter":
                ParameterService.create(definition_id=this_param.id, scenario_id=s.id,
                                        requirements=f"(self.id == {s.id})", value=ts_date)
            else:
                this_param.value = ts_date
                ParameterService.update(this_param)
            ParameterService.commit()
        elif field_name == "chemical": # emission settings, add/remove chemicals from a scenario
            new_chem = ChemicalService.get(name=scenario_data["chemical"])
            if new_chem in s.chemicals:
                s.chemicals.remove(new_chem)
            else:
                s.chemicals.append(new_chem)

    except Exception as e:
        logger.error(traceback.format_exc())
    ScenarioService.update(s)
    if ret_val:
        return ApiResult(ret_val)
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
                    par_dict.setdefault(par.id, {"par": par, "frm": f})
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
                    cpar_map[s_par.id] = ns_par.id
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
                        cpar_map[c_par.id] = nc_par.id
                    formulas_with_comp_ids = check_for_comp_ids(formulas_with_comp_ids, c_par)
                    # ParameterService.commit()
        logger.info(f'Copied chemical parameters in {time.time() - chem_par_start_time} seconds')

        logger.info(f'Finding static compartment ids in parameter formulas')
        chk_par_start_time = time.time()
        # check volume element parameters for hardwired ids.
        for ve in s.volume_elements:
            for vpr_name, vpr in ve.parameters.items():
                formulas_with_comp_ids = check_for_comp_ids(formulas_with_comp_ids, vpr)

        # check compartment parameters for hardwired ids.
        for cmp in s.compartments:
            for pr_name, pr in cmp.parameters.items():
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
                        cpar_map[ve_par.id] = nve_par.id
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
                            cpar_map[cpar.id] = ncpar.id
                            # ParameterService.commit()

                logger.info(f"Finished copying {ve.name} for {prc.name}")
            logger.info(f"{5*'<'} Finished copying {prc.name} in {time.time() - start_time} seconds {5*'>'}\n")
        logger.info(f"Copied all components in {time.time() - cp_all_start_time} seconds\n")

        # Check if we have a parameter with formula that has the hardwired ids found above.
        logger.info("Fixing Formulas with Static Compartment ids ...")
        fix_par_start_time = time.time()
        for old_par_id in formulas_with_comp_ids:
            new_par_id = cpar_map[old_par_id]
            # replace all old compartment ids with new compartment ids
            old_formula = formulas_with_comp_ids[old_par_id]["frm"].equation
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
        logger.info("Copying Compartment Links ...")
        lnk_cp_start_time = time.time()
        for lnk in CompartmentService.links.get_all():
            if lnk.sender_id in cmp_map.keys():
                CompartmentService.links.create(sender_id=cmp_map[lnk.sender_id], receiver_id=cmp_map[lnk.receiver_id])
        logger.info(f'Copied compartment links in {time.time() - lnk_cp_start_time} seconds')
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
    print(f"Clearing Last Model Run for {scn.name} {[v for v in scn.proc_status][0].run_datetime}...")
    data_resp = {"success": "success"}
    try:
        if len(scn.proc_status.all()) > 0:
            scn.proc_status.delete()
    except Exception as e:
        print([v for v in scn.proc_status][0])
        print(f'problem deleting {e}')
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
            print(f"Starting Model Run ({datetime.now()}...")
            json_n_avg, json_c_avg, output_file_n, output_file_c = run_full_model(s)

            data_resp = {"mass": json_n_avg, "conc": json_c_avg, "outputMass": output_file_n, "outputConc": output_file_c}
    except Exception as e:
        print(e)
        data_resp = {"error": e}

    print(f"Model Run Finished ({datetime.now()}...")

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
        fin_stat = [v for v in s.proc_status][0].run_status
        run_date = [v for v in s.proc_status][0].run_datetime
        output_file_n = Path([v for v in s.proc_status][0].result_file_nt).name
        output_file_c = Path([v for v in s.proc_status][0].result_file_conc).name
        json_n_avg = [v for v in s.proc_status][0].result_nt
        json_c_avg = [v for v in s.proc_status][0].result_conc

        result_resp = json.loads(json.dumps({"mass": json.loads(json_n_avg), "conc": json.loads(json_c_avg), "final_status": fin_stat, "run_date": run_date, "outputMass": output_file_n, "outputConc": output_file_c}, indent=4, sort_keys=True, default=str))
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
    if [v for v in s.proc_status][0].is_run_error:
        run_status = "err"
        run_percent = "err"
    else:
        run_status, run_percent = [v for v in s.proc_status][0].run_step
    return ApiResult({'status': run_status, 'percent': run_percent})


@scenario_api.route('/api/scenario/poll/', methods=['POST'])
@login_required
def reset_poll_model_run_scenario():
    scenario_data = request.form.to_dict()
    if not scenario_data.get('scenario_id'):
        raise AssertionError("Scenario ID cannot be blank.")
    scenario_id = int(scenario_data['scenario_id'])
    s = ScenarioService.get(scenario_id)
    if s.has_process_hist:
        [v for v in s.proc_status][0].run_status = 'run null null'
    else:
        new_proc = ScenarioLoadRunProc(scenario=s, load_status='load 100', run_status='run null null')
        [s.proc_status][0].add(new_proc)
    ScenarioService.commit()
    return "success"

@scenario_api.route('/api/scenario/check_execution_completion/', methods=['POST'])
@login_required
def check_execution_completion():
    req_data = request.form.to_dict()
    if not req_data.get('execution_arn'):
        raise AssertionError("execution ARN cannot be blank.")

    execution_arn = req_data['execution_arn']

    sfn_client = boto3.client("stepfunctions")

    desc_resp = sfn_client.describe_execution(executionArn=execution_arn)
    if desc_resp["status"] == "SUCCEEDED":
        resp = {
            "success": True,
            "sfn_output": json.loads(desc_resp["output"])
        }
    else:
        # success should still be True b/c we didn't fail; we're just not done yet...
        # calling client will just wait and retry.
        resp = {
            "success": True,
            "sfn_output": False
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

    for f in ["outputMass", "outputConc"]:
        full_key = f"{uuid}/{f}.xlsx"
        response = s3_client.generate_presigned_url("get_object",
                                                    Params={
                                                        "Bucket": bucket,
                                                        "Key": full_key
                                                    },
                                                    ExpiresIn=600) # expires in 10 minute(s)

        resp[f] = response


    return ApiResult(resp)


@scenario_api.route('/api/scenario/<int:scenario_id>/export/mirc', methods=['GET'])
# TODO: Need some way for MIRC *app* to authenticate?
@login_required
def export_for_mirc(scenario_id):
    scen = ScenarioService.get(scenario_id)
    if not scen:
        raise ApiException("Unknown Scenario")

    logger = make_logger('mirc_exporter')
    logger.info(f"Compiling required MIRC data for scenario {scen.name}...")
    try:
        latest_model_run = [v for v in scen.proc_status if not v.is_run_error]
        if len(latest_model_run) == 0:
            return ApiResult({
                'trim_data': {"message": "No valid data found"}
            })
        latest_model_run = latest_model_run[0]

        mass = json.loads(latest_model_run.result_nt)
        mass = json.loads("{"+mass+"}")
        conc = json.loads(latest_model_run.result_conc)
        conc = json.loads("{"+conc+"}")

        logger.info(f"Model run found, using run with id [{latest_model_run.id}]...")

        chems = {c.name : c for c in scen.chemicals}
        timestamps = [f"01/01/{year} 00:00:00 EST" for year in mass['year'].values()]

        trim_data = {
            'scenario_name': scen.name,
            'chemicals': list(chems.keys()),
            'timestamps': timestamps,
        }

        trim_data["parcels"] = compile_mirc_parcel_data(scen, chems, conc, timestamps, logger)
    except Exception as e:
        logger.error(e)
        traceback.print_exc()
        trim_data = {"error": "No valid data found"}

    return ApiResult({
        'trim_data': trim_data
    })

def compile_mirc_parcel_data(scen, chems, conc, timestamps, logger):
    logger.info(f"Compiling parcel data for...")
    parcels = []
    for parcel in scen.parcels:
        logger.info(f"{parcel.name}")
        p = {
            "name": parcel.name,
            "vertices": parcel.vertices,
            "volume_elements": [],
        }
        for volume_element in parcel.volume_elements:
            ve = {
                "name": volume_element.name,
                "compartments": [],
            }
            for compartment in volume_element.compartments:
                c = {
                    "name": compartment.name,
                    "properties": {},
                }

                # properties not relevant for a given compartment can be skipped
                for chem_name in chems.keys():
                    props = {}
                    filtered_key = f'{chem_name}_{compartment.standard_name}'
                    filtered_conc = list(conc[filtered_key].values())
                    filtered_conc_units = list(conc[filtered_key+"_units"].values())

                    # constants
                    if "air" in c["name"].lower():
                        props["rho_a"] = {
                            "value": compartment.rho.magnitude,
                            "unit": str(compartment.rho.units), # "g/cm^3"
                        }

                    chem_kd = chems[chem_name].Kd(compartment=compartment)
                    props["Kd"] = {
                        "value": chem_kd.magnitude,
                        "unit": str(chem_kd.units), # "L/kg"
                    }

                    chem_fmd = chems[chem_name].FractionMass_Dissolved(compartment=compartment)
                    if chem_fmd:
                        if isinstance(chem_fmd, pint.Quantity):
                            props["FMD"] = chem_fmd.magnitude
                        else:
                            props["FMD"] = chem_fmd
    
                    chem_fv = chems[chem_name].FractionMass_Vapor(compartment=compartment)
                    if chem_fv:
                        if isinstance(chem_fv, pint.Quantity):
                            props["Fv"] = chem_fv.magnitude
                        else:
                            props["Fv"] = chem_fv


                    # timestamp values
                    props["C"] = {}  # concentration

                    chem_wet = chems[chem_name].ParticleVolumetricWetDepositionRate(compartment=compartment)
                    props["Drwp"] = {}  # deposition rate wet particle

                    chem_dry = chems[chem_name].ParticleVolumetricDRYDepositionRate(compartment=compartment)
                    props["Drdp"] = {}  # deposition rate dry particle
                    for i, timestamp in enumerate(timestamps):
                        if isinstance(filtered_conc_units[0], str):
                            props["C"][timestamp] = {
                                "value": filtered_conc[i],
                                "unit": filtered_conc_units[i] # "ug/g"
                            }
                        props["Drwp"][timestamp] = {
                            "value": chem_wet.magnitude,
                            "unit": str(chem_wet.units) # "g/day/m^2"
                        }
                        props["Drdp"][timestamp] = {
                            "value": chem_dry.magnitude,
                            "unit": str(chem_dry.units) # "g/day/m^2"
                        }

                    c["properties"][chem_name] = props
                ve["compartments"].append(c)
            p["volume_elements"].append(ve)
        parcels.append(p)
    return parcels


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
        raise ApiException("Unknown Scenario")

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
        print(e)
        data_resp = {"error": e}

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
