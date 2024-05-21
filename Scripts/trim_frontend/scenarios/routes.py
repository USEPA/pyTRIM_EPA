import json
import os
import time
from datetime import datetime

import boto3
import pandas as pd
from flask import Blueprint, request, render_template, redirect, url_for
from flask_security import login_required, current_user
from flask_api import ApiResult
from datetime import datetime
from trim_db import ScenarioService, ParcelService, \
    CompartmentService, VolumeElementService, ParameterService, ChemicalService, FormulaService, ScenarioLoadRunProc
from trim_frontend import api
from trim_frontend.parcels.routes import delete_parcel_contents
from .forms import *
from ..utils.logging import make_logger
from trim_core.algorithms.full_model_run import run_full_model
# from sqlalchemy import inspect

import traceback

scenario = Blueprint('scenario', __name__)

param_map = {
    'meteo': {
        'meteo_ambient_air_static_value': 'AirTemperature',
        'meteo_ambient_air_field_name_TS': 'AirTemperature',
        'meteo_wind_speed_static_value': 'horizontalWindSpeed',
        'meteo_wind_speed_field_name_TS': 'horizontalWindSpeed',
        'meteo_wind_direction_static_value': 'windDirection',
        'meteo_wind_direction_field_name_TS': 'windDirection',
        'meteo_mixing_height_static_value': 'mixingHeight',
        'meteo_mixing_height_field_name_TS': 'mixingHeight',
        'meteo_daytime_indicator_static_value': 'isDay_Dynamic',
        'meteo_daytime_indicator_field_name_TS': 'isDay_Dynamic',
        'meteo_precipitation_static_value_rate': 'Rain',
        'meteo_precipitation_field_name_TS': 'Rain',
        'meteo_interception_fractions_static_deciduous': ['Deciduous_Leaf', 'WetDepInterceptionFraction_UserSupplied'],
        'meteo_interception_fractions_static_grass': ['Grass_Leaf', 'WetDepInterceptionFraction_UserSupplied'],
        'meteo_interception_fractions_static_coniferous': ['Coniferous_Leaf', 'WetDepInterceptionFraction_UserSupplied'],
        'meteo_interception_fractions_static_agriculture': ['Agriculture_Leaf', 'WetDepInterceptionFraction_UserSupplied'],
        'meteo_interception_fractions_calculated_deciduous': ['Deciduous_Leaf', 'CalculateWetDepInterceptionFraction'],
        'meteo_interception_fractions_calculated_grass': ['Grass_Leaf', 'CalculateWetDepInterceptionFraction'],
        'meteo_interception_fractions_calculated_coniferous': ['Coniferous_Leaf', 'CalculateWetDepInterceptionFraction'],
        'meteo_interception_fractions_calculated_agriculture': ['Agriculture_Leaf', 'CalculateWetDepInterceptionFraction']
    },
    'seasonal': {
        'seasonal_deciduous_forest_static_value_litterfall': ['Deciduous_Leaf', 'LitterFallRate'],
        'seasonal_deciduous_forest_field_name_litterfall_TS': ['Deciduous_Leaf', 'LitterFallRate'],
        'seasonal_deciduous_forest_static_value_allow_exchange': ['Deciduous_Leaf', 'AllowExchange_Dynamic'],
        'seasonal_deciduous_forest_field_name_allow_exchange_TS': ['Deciduous_Leaf', 'AllowExchange_Dynamic'],
        'seasonal_coniferous_forest_static_value_litterfall': ['Coniferous_Leaf', 'LitterFallRate'],
        'seasonal_coniferous_forest_field_name_litterfall_TS': ['Coniferous_Leaf', 'LitterFallRate'],
        'seasonal_coniferous_forest_static_value_allow_exchange': ['Coniferous_Leaf', 'AllowExchange_Dynamic'],
        'seasonal_coniferous_forest_field_name_allow_exchange_TS': ['Coniferous_Leaf', 'AllowExchange_Dynamic'],
        'seasonal_grasses_herbs_static_value_litterfall': ['Grass_Leaf', 'LitterFallRate'],
        'seasonal_grasses_herbs_field_name_litterfall_TS': ['Grass_Leaf', 'LitterFallRate'],
        'seasonal_grasses_herbs_static_value_allow_exchange': ['Grass_Leaf', 'AllowExchange_Dynamic'],
        'seasonal_grasses_herbs_field_name_allow_exchange_TS': ['Grass_Leaf', 'AllowExchange_Dynamic'],
        'seasonal_agriculture_static_value_litterfall': ['Agriculture_Leaf', 'LitterFallRate'],
        'seasonal_agriculture_field_name_litterfall_TS': ['Agriculture_Leaf', 'LitterFallRate'],
        'seasonal_agriculture_static_value_allow_exchange': ['Agriculture_Leaf', 'AllowExchange_Dynamic'],
        'seasonal_agriculture_field_name_allow_exchange_TS': ['Agriculture_Leaf', 'AllowExchange_Dynamic'],
    }
}


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
    s = ScenarioService.get(id)
    return ApiResult({'scenario': s.as_serializable()})


@scenario_api.route('/api/scenario/update', methods=['POST'])
@login_required
def update_scenario():
    logger = make_logger('scenario_api_update')
    ret_val = ''

    def update_custom_param(scen, comp, par_name, par_val):
        par_list = [p for p in scen.custom_params if
                    p.definition.variable_name == par_name and f'self.id == {comp.id}' in p.requirements]
        for c_p in par_list:
            c_p.value = par_val
            ParameterService.update(c_p)

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

        if param_type == "MET":
            df_met = df_met.loc[
                (df_met.Month < 13) & (df_met.Day < 32) & (df_met.Year < 2100) & (df_met.Hour < 25)]  # drop faulty
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
        if not scenario_data['id']:
            raise AssertionError("Scenario ID cannot be blank.")
        # Get the specified parcel
        s = ScenarioService.get(int(scenario_data['id']))

        # Update the specified property
        field_name = scenario_data["field"]
        if field_name == "erosionRateCalcSource":  # Data from erosion tab
            ercs = scenario_data["erosionRateCalcSource"]
            ercs_obj = [pp for pp in ParameterService.definitions.get_all() if pp.full_name == "erosionRateCalcSource"]
            ercs_cp = ParameterService.get_or_create(definition_id=ercs_obj[0].id, scenario_id=scenario_data['id'])
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
                    update_custom_param(s, c, param_name, scenario_data[field_name])
            else:
                param_name = param_map["meteo"].get(field_name)
                param_data = scenario_data[field_name]
                if "_static_" in field_name:
                    update_custom_param(s, s, param_name, param_data)
                elif field_name.endswith("_TS"):
                    ret_val = meteo_wgt_avg_value_from_timeseries(param_data, "MET")
                    update_custom_param(s, s, param_name, list(ret_val.values())[0])
        elif field_name.startswith("seasonal_"):  # Data from the seasonal dynamics tab
            param_media = param_map["seasonal"].get(field_name)[0]
            param_name = param_map["seasonal"].get(field_name)[1]
            param_data = scenario_data[field_name]
            comp_list = [c for c in s.compartments if c.media.isa(param_media)]
            if "_static_" in field_name:
                update_custom_param(s, comp_list[0], param_name, param_data)
            elif field_name.endswith("_TS"):
                ret_type = "LF" if field_name.endswith("_litterfall_TS") else "AE"
                ret_type_name = "wt_av_litterfallrate" if field_name.endswith("_litterfall_TS") else \
                    "wt_av_allowexchange" if field_name.endswith("_allow_exchange_TS") else "None"
                ret_val = meteo_wgt_avg_value_from_timeseries(param_data, ret_type)
                if ret_type != "None":
                    update_custom_param(s, comp_list[0], param_name, ret_val[ret_type_name])
        elif field_name == "startDate" or field_name == "endDate":
            date_parts = scenario_data[field_name].split("-")
            date_obj = datetime(int(date_parts[0]), int(date_parts[1]), int(date_parts[2]))
            ts_date = time.mktime(date_obj.timetuple())
            par_name = "simulationBeginDateTime" if field_name == "startDate" else "simulationEndDateTime"
            par_list = {par_k: par for par_k, par in s.parameters.items() if par_k == par_name}
            this_param = par_list[par_name]
            if this_param.__tablename__ != "custom_parameter":
                ParameterService.create(definition_id=this_param.id, scenario_id=s.id,
                                        requirements=f"(self.id == {s.id})", value=ts_date)
            else:
                this_param.value = ts_date
                ParameterService.update(this_param)
            ParameterService.commit()

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

        # Add scenario properties/parameters
        logger.info("Adding scenario Properties")
        for s_par_name, s_par in s.parameters.items():
            if s_par.__tablename__ == "custom_parameter" and s_par.scenario.id == s.id:
                ParameterService.create(definition_id=s_par.definition_id, scenario_id=ns.id,
                                        requirements=f"(self.id == {ns.id})", value=s_par.value,
                                        unit=s_par.unit, formula_id=s_par.formula_id)
                # ParameterService.commit()

        # Add scenario chemicals
        logger.info("Adding scenario Chemicals")
        for sc in s.chemicals:
            ns.chemicals.append(sc)
            # ScenarioService.commit()
            # Add Chemical properties/parameters
            for c_par_name, c_par in sc.parameters.items():
                if c_par.__tablename__ == "custom_parameter" and c_par.scenario.id == s.id:
                    ParameterService.create(definition_id=c_par.definition_id, scenario_id=ns.id,
                                            requirements=f"(self.id == {sc.id})", value=c_par.value,
                                            unit=c_par.unit, formula_id=c_par.formula_id)
                    # ParameterService.commit()


        # Create new parcels
        cmp_map = {}
        for prc in s.parcels:
            np = ParcelService.create(name=prc.name, description=prc.description, scenario_id=ns.id, vertices=prc.vertices)
            start_time = time.time()
            # ParcelService.commit()
            # Create new volume elements
            for ve in prc.volume_elements:
                nve = VolumeElementService.create(name=ve.name, parcel_id=np.id, top=ve.top, bottom=ve.bottom)
                # VolumeElementService.commit()
                # Create new volume compartments
                for cmp in ve.compartments:
                    ncmp = CompartmentService.create(name=cmp.name, volume_element_id=nve.id, media_id=cmp.media_id)
                    cmp_map[cmp.id] = ncmp.id
                    # CompartmentService.commit()
                    # Create new custom parameters for compartments
                    for parn, cpar in cmp.parameters.items():
                        if cpar.__tablename__ == "custom_parameter" and cpar.scenario.id == s.id:
                            ParameterService.create(definition_id=cpar.definition_id, scenario_id=ns.id,
                                                    requirements=f"(self.id == {ncmp.id})", value=cpar.value,
                                                    unit=cpar.unit, formula_id=cpar.formula_id)
                            # ParameterService.commit()
                logger.info(f"Finished copying {ve.name} for {prc.name}")
            logger.info(f"{5*'<'} Finished copying {prc.name} in {time.time() - start_time} seconds {5*'>'}\n")

        # Create the compartment links using the compartment id map
        logger.info("Copying Compartment Links ...")
        for lnk in CompartmentService.links.get_all():
            if lnk.sender_id in cmp_map.keys():
                CompartmentService.links.create(sender_id=cmp_map[lnk.sender_id], receiver_id=cmp_map[lnk.receiver_id])
        # CompartmentService.commit()
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
    scenario_data = request.form.to_dict()
    if not scenario_data.get('scenario_id'):
        raise AssertionError("Scenario ID cannot be blank.")
    
    scenario_id = int(scenario_data['scenario_id'])
    s = ScenarioService.get(scenario_id)

    try:
        # Delete chemical custom parameters
        for sc in s.chemicals:
            for c_par_name, c_par in sc.parameters.items():
                if c_par.__tablename__ == "custom_parameter" and c_par.scenario.id == s.id:
                    ParameterService.delete(c_par)
            # Remove the scenario chemical
            s.chemicals.remove(sc)
            # ScenarioService.commit()
        # Delete scenario custom parameters
        for s_par_name, s_par in s.parameters.items():
            if s_par.__tablename__ == "custom_parameter" and s_par.scenario.id == s.id:
                ParameterService.delete(s_par)
        # ParameterService.commit()

        # Delete all parcels and contents
        for parcel in s.parcels:
            delete_parcel_contents(parcel)
            ParcelService.delete(parcel.id)
        # ParcelService.commit()

        # Delete scenario
        ScenarioService.delete(s.id)
        # ScenarioService.commit()
    except Exception as e:
        print(e)
        print("Failed to delete scenario...")
    finally:
        ScenarioService.commit()

    return redirect(request.referrer)

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
        if trim_env_profile in [ "dev", "prod" ]:
            sfn_client = boto3.client("stepfunctions")
            state_machine_arn = os.environ.get("TRIM_DOCKERIZED_STATEMACHINE_ARN")

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
        output_file_n = [v for v in s.proc_status][0].result_file_nt
        output_file_c = [v for v in s.proc_status][0].result_file_conc
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
