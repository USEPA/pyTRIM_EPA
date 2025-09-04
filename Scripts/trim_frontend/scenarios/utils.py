import pandas as pd
import pint
from numpy import timedelta64
from trim_db.schema import CustomParameter
from trim_db.services import *
from trim_db.services.parameters import get_or_create_custom_param
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
        {"kwargs": {"variable_name":"isDay_Dynamic"}, "value": 1},
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

    ScenarioService.update(s)

    return ret_val


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


def meteo_wgt_avg_value_from_timeseries(par_dat, param_type):
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
                       'WindDirection': (-360, 360), 'mixingHeight': (0, 1000), 'isDay': (0, 1),
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
