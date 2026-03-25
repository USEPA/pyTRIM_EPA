import boto3
import json
import time
from datetime import datetime
import os
import pandas as pd
import pint
import numpy as np
from pathlib import Path
from trim_frontend.external_API.routes import SoilData, get_soil_boundaries
from trim_db.schema import CustomParameter, ParameterDefinition
from trim_db.services import *
from trim_db.services.parameters import get_or_create_custom_param, update_custom_param_value
from .defaults import *
from ..utils.logging import make_logger


def set_param_default_val(kwargs, val):
    try:
        default_params = ParameterService.definitions.get_all(**kwargs)
        for param in default_params:
            if not param.default_value:
                param.default_value = val
                ParameterService.definitions.update(param)
    except Exception as e:
        print('error setting param:', e)


def init_first_time_default_param_values():
    # fmt: off
    default_params = [
        # Meteorology
        {"kwargs": {"variable_name":"AirTemperature", "default_unit":"K"}, "value": 298},
        {"kwargs": {"variable_name":"horizontalWindSpeed"}, "value": 1.6},
        {"kwargs": {"variable_name":"windDirection"}, "value": 270},
        {"kwargs": {"variable_name":"isDay_Dynamic"}, "value": 0.5},
        {"kwargs": {"variable_name":"Rain"}, "value": 0.0041}, # Precipitation

        # Water Body Properties
        {"kwargs": {"variable_name": "WaterTemperature", "default_unit":"K"}, "value": 298},
        {"kwargs": {"variable_name": "pH"}, "value": 7.3},
        {"kwargs": {"variable_name": "AlgaeDensityInWaterColumn"}, "value": 0.0025},
        {"kwargs": {"variable_name": "ChlorideConcentration"}, "value": 8},
        {"kwargs": {"variable_name": "ChlorophyllConcentration"}, "value": 0.0029},
        {"kwargs": {"variable_name": "OrganicCarbonContent"}, "value": 0.02},
        {"kwargs": {"variable_name": "SuspendedSedimentConcentration"}, "value": 0.05},
        {"kwargs": {"variable_name": "ExternalSedimentInflow"}, "value": 0},
        {"kwargs": {"variable_name": "SedimentDepositionVelocity"}, "value": 2},
        {"kwargs": {"variable_name": "waterEvaporationRate"}, "value": 0.7}

        # Aquatic Food Web
        # {"kwargs": {"variable_name": "FoodIngestionRate"}, "value": 0},
    ]
    # fmt: on

    for obj in default_params:
        set_param_default_val(obj["kwargs"], obj["value"])
    ParameterService.commit()


def init_parameter_definitions(kwarg_list, check_subtypes=False):
    for kwargs in kwarg_list:
        if check_subtypes:
            default_param = ParameterService.definitions.get(**kwargs)
        else:
            default_param = ParameterService.definitions.get(full_name=kwargs["full_name"])
        if not default_param:
            ParameterService.definitions.create(**kwargs, no_commit=True)
    ParameterService.commit()


def use_local_model_run():
    # in dev/prod, we execute an AWS StepFunction to run the model via Docker/ECS. Locally,
    # we just run the model directly.
    trim_env_profile = os.environ.get("TRIM_ENV_PROFILE", "").lower()
    return (trim_env_profile not in ["test", "dev", "devgetflow", "prod"])


def start_state_machine_model_run(scen):
    sfn_client = boto3.client("stepfunctions")
    state_machine_arn = os.environ.get("TRIM_DOCKERIZED_RUNMODEL_STATEMACHINE_ARN")
    if state_machine_arn is None:
        print('ERROR: No ARN found for state machine; unable to run model')
        return None  # Nothing to do
    try:
        resp = sfn_client.start_execution(
            stateMachineArn=state_machine_arn,
            input=json.dumps({
                "scenarioId": str(scen.id),
                "generateFakeResults": "false"
            })
        )
        return resp["executionArn"]
    except Exception:
        print('ERROR: Unable to start model run on state machine')
        import traceback; traceback.print_exc()
        return None  # Nothing to do


def get_latest_run_info(scen, allow_debug=False):
    run_info = {
        'has_run': scen.has_process_hist,
        "lastest_run_date": "",
        "execution_arn": "",
        "run_status": "run tm 0",
        "run_has_results": False,
        "run_results": {}
    }

    if run_info["has_run"]:
        proc_info = scen.latest_proc_status
        run_info["lastest_run_date"] = proc_info.run_datetime.strftime('%Y-%m-%d "%H:%M:%S"')
        run_info["execution_arn"] = proc_info.execution_arn or ""
        run_info["run_status"] = proc_info.run_status or "run tm 0"
        run_info["run_has_results"] = (
            True if proc_info.run_status == 'run fin 100' else False
        )
        is_local_run = use_local_model_run()
        if run_info["run_has_results"]:
            if is_local_run:
                run_info["run_results"] = get_local_results(proc_info)
            elif proc_info.execution_arn:
                run_info["run_results"] = get_step_function_results(proc_info.execution_arn)

        if (not is_local_run) and proc_info.execution_arn:
            if (not run_info["run_has_results"]) or ('err ' in proc_info.run_status):
                if allow_debug:
                    debug_messages = fetch_output_for_step_function_execution(
                        proc_info.execution_arn
                    )
                else:
                    debug_messages = [
                        "debug output disabled for external users"
                    ]
                run_info['debug_messages'] = debug_messages

    return run_info


def process_model_data(data):
    if data is None:
        return None
    parsed = json.loads(data)
    restrung = json.dumps(parsed, sort_keys=True, default=str)
    processed = json.loads(f'{{{json.loads(restrung)}}}')
    return processed


def get_local_results(proc_info):
    def aws_or_local(f):
        if f is None:
            return None
        return f if ".s3.amazonaws.com" in f else Path(f).name

    run_results = {
        "mass_results": process_model_data(proc_info.result_nt),
        "mass_results_file": aws_or_local(proc_info.result_file_nt),
        "conc_results": process_model_data(proc_info.result_conc),
        "conc_results_file": aws_or_local(proc_info.result_file_conc)
    }
    if hasattr(proc_info, 'result_file_tm'):
        run_results["tm_results_file"] = aws_or_local(proc_info.result_file_tm)

    return run_results


def get_step_function_results(execution_arn):
    sfn_results = {}

    object_to_fname = {
        "outputMass": 'mass_results_file',
        "outputConc": 'conc_results_file',
        "outputTM": 'tm_results_file'
    }

    sfn_client = boto3.client("stepfunctions")
    desc_resp = sfn_client.describe_execution(executionArn=execution_arn)
    if desc_resp["status"] == "SUCCEEDED":
        output = json.loads(desc_resp["output"])
        bucket = output['bucket']
        uuid = output['uuid']

        s3_resource = boto3.resource("s3")
        content_object = s3_resource.Object(bucket, f"{uuid}/model_output.json")
        file_content = content_object.get()["Body"].read().decode("utf-8")
        json_content = json.loads(file_content)

        sfn_results = {
            'mass_results': process_model_data(json.dumps(json_content['mass'], default=str)),
            'conc_results': process_model_data(json.dumps(json_content['conc'], default=str))
        }

        s3_client = boto3.client("s3")
        for obj, fname in object_to_fname.items():
            full_key = f"{uuid}/{obj}.xlsx"
            response = s3_client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": bucket,
                    "Key": full_key
                },
                ExpiresIn=(60 * 60 * 6)  # == 6 hours
            )
            sfn_results[fname] = response
    return sfn_results


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
        if not ecs_task_event:
            return []
        # re-parse the details/output, included as a JSON string in the boto3 reply...
        output = json.loads(ecs_task_event.get("taskSubmittedEventDetails", {}).get("output", "{}"))
        if not output:
            return []

        # get the ECS task id
        tasks = output.get("Tasks", [])

        task = tasks[0] if len(tasks) > 0 else None
        if not task:
            return []

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


def compile_mirc_data(scen, latest_model_run, logger=None):
    if not logger:
        logger = make_logger('compile_mirc_data')
    logger.info(f"Compiling required MIRC data for scenario {scen.name}...")
    
    if latest_model_run and not latest_model_run.is_run_error:
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
        return {"trim_data": trim_data}
    else:
        return {"trim_data": {"message": "No valid data found"}}


def compile_mirc_parcel_data(scen, chems, conc, timestamps, logger):
    parcels = []
    for parcel in scen.parcels:
        logger.info(f"Compiling parcel data for {parcel.name}...")
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
                    if filtered_key not in conc:
                        continue
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


def handle_scenario_update(s, scenario_data):
    logger = make_logger('handle_scenario_update')

    ret_val = None

    # Update the specified property
    field_name = scenario_data["field"]
    if field_name == "erosionRateCalcSource":  # Data from erosion tab
        ercs = scenario_data["erosionRateCalcSource"]
        default_ercs = ParameterService.definitions.get(full_name="erosionRateCalcSource")
        ercs_cp = ParameterService.get_or_create(definition=default_ercs, scenario_id=s.id)
        ercs_cp.value = ercs

        for c in s.compartments:
            if c.media.isa('Surface_Soil'):
                par = c.parameters.get('TotalErosionRate')
                if isinstance(par, CustomParameter):
                    ParameterService.delete(par, no_commit=True)

        ParameterService.commit()

    elif field_name == "name":  # Scenario Name
        s.name = scenario_data["name"]
        ParameterService.commit()

    elif field_name == "description":  # Scenario Description
        s.description = scenario_data["description"]
        ParameterService.commit()

    elif field_name.startswith("meteo_"):  # Data from the meteorology tab
        if "_interception_" in field_name:
            param_media = param_map["meteo"].get(field_name)[0]
            param_name = param_map["meteo"].get(field_name)[1]
            comp_list = [c for c in s.compartments if c.media.isa(param_media)]
            for c in comp_list:
                update_custom_param(s, c, param_name, scenario_data[field_name], create_if_dne=True)
        else:
            param_name = param_map["meteo"].get(field_name)
            param_data = scenario_data[field_name]
            if "_static_" in field_name:
                update_custom_param(s, s, param_name, param_data, create_if_dne=True)
            elif field_name.endswith("_TS"):
                param_type = "SFC" if scenario_data.get("is_sfc") == 'true' else "MET"
                ret_val = meteo_wgt_avg_value_from_timeseries(param_data, param_type)
                if isinstance(ret_val, dict) and "wt_av_Rain" in ret_val.keys():
                    param_value = ret_val["wt_av_Rain"]
                elif isinstance(ret_val, dict) and "wt_av_CumulativeRain" in ret_val.keys():
                    param_value = ret_val["wt_av_CumulativeRain"]
                else:
                    param_value = list(ret_val.values())[0]
                update_custom_param(s, s, param_name, param_value, create_if_dne=True)

        if "_precipitation_" in field_name:
            update_dynamic_params(s)

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
            # The condition below assures that we do not utilize the value from the file for Coniferous forest leaf
            # If not set via custom parameter, it defaults to the desired value of 0.0021.
            if not (ret_type_name == "wt_av_litterfallrate" and param_media == 'Coniferous_Leaf'):
                ret_val = meteo_wgt_avg_value_from_timeseries(param_data, ret_type)
                if ret_type != "None":
                    update_assumed_all_comp_fixed_params(s, comp_list, param_name, ret_val[ret_type_name])

    elif field_name == "simulation_start_date" or field_name == "simulation_end_date":
        date_parts = scenario_data[field_name].split("-")
        date_obj = datetime(int(date_parts[0]), int(date_parts[1]), int(date_parts[2]))
        ts_date = time.mktime(date_obj.timetuple())
        par_name = "simulationBeginDateTime" if field_name == "simulation_start_date" else "simulationEndDateTime"
        param = s.parameters.get(par_name)
        param = get_or_create_custom_param(
            param,
            {"requirements": f"(self.id == {s.id})", "scenario_id": s.id},
        )
        param.value = ts_date
        ParameterService.update(param)

    elif field_name == "chemical": # emission settings, add/remove chemicals from a scenario
        opt = scenario_data["operation"]

        # group all mercuries
        if 'Mercury' in scenario_data["chemical"] and opt in ['add', 'remove']:
            chems = [
                ChemicalService.get(name="Divalent Mercury"),
                ChemicalService.get(name="Elemental Mercury"),
                ChemicalService.get(name="MethylMercury"),
            ]
        else:
            chems = [ChemicalService.get(name=scenario_data["chemical"])]

        for chem in chems:
            if chem in s.chemicals and opt == 'reset':
                reset_emissions_and_concentrations(s, chem, ic_reset=True)
            elif chem in s.chemicals and opt == 'remove':
                reset_emissions_and_concentrations(s, chem)
                s.chemicals.remove(chem)
            elif chem not in s.chemicals and opt == 'add':
                s.chemicals.append(chem)

    elif field_name == "soil_api":
        update_soil_from_api(s, logger)

    ScenarioService.update(s)

    return ret_val


def reset_emissions_and_concentrations(s, chem, ic_reset=False):
    # Just reset to 0
    from trim_frontend.parcels.utils import handle_parcel_update
    for comp in s.compartments:
        pcl = comp.volume_element.parcel
        src_param = comp.parameters.get('surfaceDepositionRate')
        ic_param = comp.parameters.get('initialConcentration')

        if (
            isinstance(src_param, CustomParameter)
            and f"chemical.id == {str(chem.id)}" in src_param.formula.equation
            and not ic_reset
        ):
            handle_parcel_update(
                pcl,
                {
                    "chemical_name": chem.name,
                    "compartment_name": comp.name,
                    "emission_value": "0",
                    "field": "emission",
                    "id": pcl.id,
                    "ve_name": comp.volume_element.name,
                },
            )
        if (
            isinstance(ic_param, CustomParameter)
            and f"chemical.id == {str(chem.id)}" in ic_param.formula.equation
        ):
            handle_parcel_update(
                pcl,
                {
                    "chemical_name": chem.name,
                    "compartment_name": comp.name,
                    "initial_concentration_value": "0",
                    "field": "initial concentration",
                    "id": pcl.id,
                    "ve_name": comp.volume_element.name,
                },
            )


def update_dynamic_params(scen, skip_existing=False):
    def update_param(param, comp, val):
        if isinstance(param, ParameterDefinition):
            get_or_create_custom_param(
                param,
                {
                    "requirements": f"(self.id == {comp.id})",
                    "scenario_id": scen.id,
                    "value": val,
                },
            )
        elif skip_existing: # skip custom params
            return
        # User hasn't submitted a value, so still use formula
        elif isinstance(param, CustomParameter) and param.formula:
            param.value = val
            ParameterService.commit()

    for comp in scen.compartments:
        # AverageVerticalVelocity
        if comp.name in ["Soil_Surface", "Soil_Root_Zone", "Soil_Vadose_Zone"]:
            avg_vertical_velocity = comp.parameters.get('AverageVerticalVelocity')
            val = round(0.2 * scen.Rain.magnitude, 5)
            update_param(avg_vertical_velocity, comp, val)

        # TotalRunoffRate
        if comp.name in ["Soil_Surface"]:
            total_runoff_rate = comp.parameters.get('TotalRunoffRate')
            val = comp.PrecipitationRunoffFraction * scen.Rain.magnitude
            update_param(total_runoff_rate, comp, val)


def update_mixing_height(scen, mixing_height):
    # mixingHeight is just the height of the air volume elements
    for comp in scen.get_compartment(media='Air'):
        if comp.name == "Air":
            comp.volume_element.top = float(mixing_height)
        elif comp.name == "UpperAir":
            comp.volume_element.bottom = float(mixing_height)


def create_new_custom_param_meteo(scen, comp, par_name):
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
    if par_name == 'mixingHeight':
        update_mixing_height(scen, par_val)
        return

    par_list = [p for p in scen.custom_params.all() if
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
            print('update assumed all comp fixed params error:', e)
    ParameterService.commit()


def true_wind_wt_ave(df_met, col, fallback=None):
    """
    Break down WS/WD into its components
        u = east-west wind speed
        u_bar = average u across all u values in time
        v = north-south wind speed
        v_bar = average v across all v values in time
    """
    from trim_frontend.utils.file_io import vset
    
    def u_calc(WS, WD):
        return -1 * WS * np.sin(np.radians(WD))

    def v_calc(WS, WD):
        return -1 * WS * np.cos(np.radians(WD))

    try:
        df_met['u'] = vset(df_met, u_calc, ["HorizontalWindSpeed", "WindDirection"])
        u_bar = (df_met['u'] * df_met['time_delta']).sum() / df_met['time_delta'].sum()

        df_met['v'] = vset(df_met, v_calc, ["HorizontalWindSpeed", "WindDirection"])
        v_bar = (df_met['v'] * df_met['time_delta']).sum() / df_met['time_delta'].sum()

        if col == "HorizontalWindSpeed":
            return np.sqrt(u_bar**2 + v_bar**2)
        elif col == "WindDirection":
            if u_bar <= 0 and v_bar <= 0:
                x_adjustment = 0
            elif u_bar > 0 and v_bar < 0:
                x_adjustment = 360
            else:
                x_adjustment = 180
            return np.degrees(np.arctan(u_bar/v_bar)) + x_adjustment
    except Exception as e:
        print(e)
        return fallback


def meteo_wgt_avg_value_from_timeseries(par_dat, param_type):
    par_dat = json.loads(par_dat)
    df_met = pd.DataFrame.from_dict(par_dat, orient='columns')

    df_met['dlist'] = df_met['Date'].str.split('/')  # split date column into list
    df_met = df_met[df_met.dlist.str.len() == 3]  # drop rows that have less than three elements
    df_met[['Month', 'Day', 'Year']] = df_met.Date.str.split("/", expand=True)
    df_met['Month'] = pd.to_numeric(df_met['Month'], errors='coerce')
    df_met['Day'] = pd.to_numeric(df_met['Day'], errors='coerce')
    df_met['Year'] = pd.to_numeric(df_met['Year'], errors='coerce')
    hour_col_name = 'xHour' if param_type in ["MET", "SFC"] else 'Hour'
    df_met['Hour'] = pd.to_numeric(df_met[hour_col_name], errors='coerce')
    df_met = df_met.loc[
        (df_met.Month < 13) & (df_met.Day < 32) & (df_met.Year < 2100)]  # drop faulty

    if param_type in ["MET", "SFC"]:
        df_met = df_met.loc[(df_met.Hour < 25)]  # drop faulty
        metcol_dict = {'Rain': (0, 1), 'AirTemperature': (200, 373), 'HorizontalWindSpeed': (0, 100),
                       'WindDirection': (-360, 360), 'mixingHeight': (0, 10000), 'IsDay': (0, 1),
                       'CumulativeRain': (0, 1.6)}  # k, v represent name and min-max
        for k, v in metcol_dict.items():
            if k in df_met.columns:
                df_met['metcol'] = pd.to_numeric(df_met[k], errors='coerce')
                df_met = df_met[
                    (df_met['metcol'] <= v[1]) & (df_met['metcol'] >= v[0])]  # keep rows within min max bounds

        df_met['DT'] = list(pd.to_datetime(df_met[['Year', 'Month', 'Day', 'Hour']], errors='coerce'))
    else:
        # Ignored hour resolution.
        df_met['DT'] = list(pd.to_datetime(df_met[['Year', 'Month', 'Day']], errors='coerce'))

    df_met.sort_values(by='DT', inplace=True)
    df_met['date_delta'] = (df_met['DT'] - df_met['DT'].min()) / np.timedelta64(1, 'D')
    df_met['time_delta'] = df_met['date_delta'].diff()
    # shift up the column 1 so that applicability of met condition is aligned to duration
    df_met['time_delta'] = df_met['time_delta'].shift(-1)

    # Clean up non sequential dates
    df_met['DT_Check'] = df_met.DT >= (df_met.DT.shift())
    df_met = df_met[df_met['DT_Check']]

    # Get time-weighted averages
    met_dict = {}
    if param_type in ["MET", "SFC"]:
        for k, v in metcol_dict.items():
            if k in df_met.columns:
                df_met['metcol'] = pd.to_numeric(df_met[k], errors='coerce')
                df_met['prod'] = df_met['metcol'] * df_met['time_delta']
                wt_ave = df_met['prod'].sum() / df_met['time_delta'].sum()
                
                if k in ["HorizontalWindSpeed", "WindDirection"]:
                    if k == par_dat[0].get("_selected"):
                        met_dict['wt_av_' + k] = true_wind_wt_ave(df_met, k, fallback=wt_ave)
                else:
                    met_dict['wt_av_' + k] = wt_ave

        if 'Rain' in df_met.columns:
            df_met['Rain'] = pd.to_numeric(df_met['Rain'], errors='coerce')
            df_met['is_Rain'] = [1 if x > 0 else 0 for x in df_met['Rain']]
            df_met['RainTime'] = df_met['is_Rain'] * df_met['time_delta']
            rain_frac_time = df_met['RainTime'].sum() / df_met['time_delta'].sum()
            met_dict['frac_time_rain'] = rain_frac_time

        if param_type == "SFC":
            avg_wind_speed = met_dict.get("wt_av_HorizontalWindSpeed")
            avg_mixing_height = met_dict.get("wt_av_mixingHeight")
            if avg_wind_speed:
                met_dict["wt_av_HorizontalWindSpeed"] = max(avg_wind_speed, 0.75)     
            if avg_mixing_height:
                met_dict["wt_av_mixingHeight"] = max(avg_mixing_height, 20)

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


def update_soil_from_api(s, logger):
    def calculate_layer_vals(pcl, data, layer):
        idx = [k for k,v in data['layer'].items() if v == layer][0]
        param_map = {
            "pH": data['ph1to1h2o_r'][idx],
            "OrganicCarbonContent": (data['om_r'][idx] / 100) / 1.72,
            "VolumeFraction_Liquid": data['awc_r'][idx], # water content
            "FractionSand": data['sandtotal_r'][idx] / 100,
        }

        comp = None
        if layer == "surface":
            comp = pcl.get_compartment("Soil_Surface")
        elif layer == "root":
            comp = pcl.get_compartment("Soil_Root_Zone")
        elif layer == "vadose":
            comp = pcl.get_compartment("Soil_Vadose_Zone")

        if not comp: # water / air parcels
            return

        for param_name, val in param_map.items():
            param = comp.parameters.get(param_name)
            param = get_or_create_custom_param(
                param,
                {"requirements": f"(self.id == {comp.id})", "scenario_id": pcl.scenario_id},
            )
            update_custom_param_value(param, val)

    logger.info("Obtaining parcel soil data from USDA.gov")
    if not s.parcels:
        return
    
    parcels = {}
    parcel_layers = {}
    parcel_tillage = {}
    for this_p in s.parcels:
        this_parcel_data = this_p.as_serializable()
        parcels[this_parcel_data['name']] = [(t[1], t[0]) for t in this_parcel_data['vertices']]
        parcel_layers[this_parcel_data['name']] = get_soil_boundaries(this_p)
        parcel_tillage[this_parcel_data['name']] = (this_parcel_data['soilTillage'] == 'Yes')

    sd = SoilData(vert_dict=parcels, pcl_layers=parcel_layers)
    sd.run()
    
    for pcl_name, is_tilled in parcel_tillage.items():
        logger.info(f"Calculating layer values for [{pcl_name}]")
        pcl = ParcelService.get(name=pcl_name, scenario_id=s.id)
        if is_tilled:
            soil_data = json.loads(sd.scenario_tilled_results[pcl_name])
        else:
            soil_data = json.loads(sd.scenario_no_till_results[pcl_name])

        calculate_layer_vals(pcl, soil_data, "surface")
        calculate_layer_vals(pcl, soil_data, "root")
        calculate_layer_vals(pcl, soil_data, "vadose")
