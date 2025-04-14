import os
import pandas as pd
import numpy as np
import json
from scipy.integrate import odeint
from trim_db.schema import *
from trim_db.schema.parameters.equations import evaluated_args, \
    evaluator, NoEval
from trim_db.services import *
from datetime import datetime

__all__ = ['run_full_model']

# os.environ.pop('TEST_DB_SERVERLESS')
# s.environ['TEST_DB_SERVERLESS'] = 'True'
# os.environ.pop('TRANSITION_MATRIX_COMPARTMENTS')
# os.environ['TRANSITION_MATRIX_COMPARTMENTS'] = 'Leaf,DryVapor,WetVapor,DryParticle,WetParticle,Soil'
# os.environ['DEBUG_TRANSITION_MATRIX'] = 'True'
# print(os.environ)

DEBUG = os.getenv('DEBUG_TRANSITION_MATRIX')
RESTRICT_COMPARTMENTS = [
    x.strip()
    for x in str(os.getenv('TRANSITION_MATRIX_COMPARTMENTS', '')).split(',')
    if x.strip()
]

sim_begin_date = "01/01/2020"
sim_end_date = "01/01/2025"

def is_compartment_of_interest(comp):
    if not RESTRICT_COMPARTMENTS:
        return True
    for x in RESTRICT_COMPARTMENTS:
        if x in comp.standard_name:
            return True
    return False


def full_stack():
    import traceback, sys
    exc = sys.exc_info()[0]
    if exc is not None:
        f = sys.exc_info()[-1].tb_frame.f_back
        stack = traceback.extract_stack(f)
    else:
        stack = traceback.extract_stack()[:-1]  # last one would be full_stack()
    trc = 'Traceback (most recent call last):\n'
    stackstr = trc + ''.join(traceback.format_list(stack))
    if exc is not None:
        stackstr += '  ' + traceback.format_exc().lstrip(trc)
    return stackstr


def make_transition_matrix(scenario):
    def full_stack():
        import traceback, sys
        exc = sys.exc_info()[0]
        stack = traceback.extract_stack()[:-1]  # last one would be full_stack()
        if exc is not None:  # i.e. an exception is present
            del stack[-1]  # remove call of full_stack, the printed exception
            # will contain the caught exception caller instead
        trc = 'Traceback (most recent call last):\n'
        stackstr = trc + ''.join(traceback.format_list(stack))
        if exc is not None:
            stackstr += '  ' + traceback.format_exc().lstrip(trc)
        return stackstr

    chem_list = list(sorted(
        scenario.chemicals, key=lambda x: x.name
    ))

    comp_list = list(sorted(
        scenario.compartments, key=lambda x: x.standard_name
    ))

    if DEBUG:
        comp_list = [x for x in comp_list if is_compartment_of_interest(x)]

    n_chem = len(chem_list)
    n_comp = len(comp_list)
    vmu = []

    matrix_dimensions = n_chem * n_comp

    source_matrix = np.zeros(matrix_dimensions, dtype=float)
    ic_matrix = np.zeros(matrix_dimensions, dtype=float)
    ic_units = [''] * matrix_dimensions  # create empty list of c0 units
    transition_matrix = np.zeros(
        (matrix_dimensions, matrix_dimensions), dtype=float
    )

    index_names = ['' for _ in source_matrix]

    chem_indices = {
        c: i for i, c in enumerate(chem_list)
    }

    i_perc = int(100/n_chem)

    def compute_initial_mass(df_c0, df_vmu):  # arguments are the chemical mass array (nt), mass dataframe

        df = df_c0.merge(df_vmu, left_index=True, right_index=True)
        df['n0_g'] = 0
        df.loc[df['initial_concentration_units'] == 'g/m^3', 'n0_g'] = df['initial_concentration'] * df['volume_m3']
        df.loc[df['initial_concentration_units'] == 'g/L', 'n0_g'] = df['initial_concentration'] * df[
            'volume_m3'] * 1000
        df.loc[df['initial_concentration_units'] == 'g/kg', 'n0_g'] = df['initial_concentration'] * df['mass_kg']
        df_n0 = df[['initial_concentration_units', 'n0_g']]

        return (df_n0)

    try:
        for chem_idx, chem in enumerate(chem_list):
            this_perc = i_perc * chem_idx
            [v for v in scenario.proc_status][0].run_status = f'run tm {this_perc}'
            ScenarioService.commit()
            # if chem.name != 'Elemental Mercury':
            #     continue
            print('\n' + '==' * 28)
            print(f'Chemical = {chem.name}')
            print('==' * 28)

            for x, sender in enumerate(comp_list):
                comp_perc = int(this_perc + ((i_perc * x) / n_comp))
                if (x % 50) == 0:
                    [v for v in scenario.proc_status][0].run_status = f'run tm {comp_perc}'
                    ScenarioService.commit()
                tm_x = int(chem_idx * n_comp + x)

                index_names[tm_x] = chem.name + '_' + sender.standard_name

                try:
                    dr = sender.surfaceDepositionRate(chem)
                    if not (str(dr) == 'nan'):
                        source_matrix[tm_x] += dr.magnitude
                except Exception as e:
                    print(f'{"*" * 20} Problem with getting Surface Deposition Rate for compartment={sender.name}, '
                          f'chemical={chem} {"*" * 20}\nException is {e}')
                    pass

                try:
                    ic = sender.initialConcentration(chem)
                    if not (str(ic) == 'nan'):
                        ic_matrix[tm_x] += ic.magnitude
                        if hasattr(ic, "unit"):
                            ic_units[x] = ic.unit.replace(" ", "")
                        else:
                            ic_units[x] = 'g/kg'
                    else:
                        ic_matrix[tm_x] += 0
                        ic_units[x] = 'g/kg'
                except Exception as e_ic:
                    print(f'{"*" * 20} Problem with getting initial concentration for compartment={sender.name}, '
                          f'chemical={chem} {"*" * 20}\nException is {e_ic}')
                    pass

                try:
                    if sender.Volume:  # if sending compartment has volume (m3)
                        vol = sender.Volume.magnitude
                    else:
                        vol = np.nan

                    if sender.TotalMass:  # if sending compartment has mass (kg)
                        mass = sender.TotalMass.magnitude
                    else:
                        mass = np.nan

                    # if sending compartment has concentration output factor
                    if sender.concentrationOutputFactor:
                        try:
                            cof = sender.concentrationOutputFactor.magnitude
                        except AttributeError:
                            cof = sender.concentrationOutputFactor

                        try:
                            cou = str(sender.concentrationOutputFactor.units)
                        except AttributeError:
                            cou = np.nan

                        if not cof:
                            cof = np.nan
                        if not cou:
                            cou = ""
                    else:
                        if sender.media.isa("Root_Zone") or sender.media.isa("Surface_Soil"):
                            cof = chem.concentrationOutputFactor(sender)
                            cou = "g / g"
                        else:
                            cof = np.nan
                            cou = ""

                    denom = "mass"  # default denom is mass
                    # if compartment is abiotic
                    if sender.media.isa("Abiotic"):
                        denom = "volume"  # denominator in concentration calculation must be volume
                    # if compartment is leaf or leaf particle (inferred this based on concentration output factor)
                    if sender.media.isa("$Leaf") or sender.media.isa("$Leaf_Particle"):
                        denom = "volume"  # denominator in concentration calculation must be volume
                    # if compartment is surface water note that denom must be in L
                    if sender.media.isa("Surface_Water"):
                        denom = "volume_L"  # denominator in concentration calculation must be volume
                    # if compartment is groundwater note that denom must be in L
                    if sender.media.isa("Groundwater"):
                        denom = "volume_L"  # denominator in concentration calculation must be volume
                    # tuples of volume, mass, units, output factor, and denominator quantity
                    vmu_tup = (sender.name, vol, mass, cou, cof, denom)
                    vmu.append(vmu_tup)
                except Exception as e:
                    print(f'{"*" * 20} Problem with getting Surface Concentration Output factor for '
                          f'compartment={sender.name}, chemical={chem} {"*" * 20}\nException is {full_stack()}')
                    vol = np.nan
                    mass = np.nan
                    cof = np.nan
                    cou = ""
                    denom = "mass"
                    vmu_tup = (sender.name, vol, mass, cou, cof, denom)
                    vmu.append(vmu_tup)

                # Some media just don't send anything
                if not sender.media.can_emit:
                    continue

                for y, receiver in enumerate(comp_list):
                    # Some media just don't receive anything
                    if not receiver.media.can_absorb:
                        continue

                    # print(sender.standard_name, '>', receiver.standard_name)

                    links = sender.get_links(receiver)
                    if not links:
                        continue

                    tm_y = int(chem_idx * n_comp + y)

                    print_vals = []
                    print_vals.append(
                        f'\n\t{sender.standard_name} >'
                        f' {receiver.standard_name}'
                        f' ({chem_idx + 1}/{n_chem},'
                        f' {x + 1}/{n_comp}, {y + 1}/{n_comp})'
                    )
                    # print_vals.append(links)

                    for link in links:
                        # print(link)
                        for transport_proc in link.transport_processes(chem):
                            # print('\t', transport_proc.name)
                            check_alg = False
                            transfer_factor = np.nan
                            try:
                                transfer_factor = transport_proc.eval(
                                    sender=sender, receiver=receiver,
                                    chemical=chem,
                                    environment=scenario
                                )
                            except Exception as ex:
                                print_vals.append(f'Unable to evaluate {transport_proc.name}')
                                check_alg = True
                                print(f'{"#"*100}\n{ex}\n{"#"*100}\n')
                            # print('\t\ttf =', transfer_factor)
                            try:
                                transfer_factor = transfer_factor.magnitude
                            except Exception:
                                pass
                            print_vals.append(
                                f'\t\t- "{transport_proc.name}"'
                                f' = {transfer_factor}'
                            )

                            try:
                                if pd.isna(transfer_factor):
                                    print_vals.append('\t\t\t Unexpected NAN!')
                                    print_vals.extend([
                                        f'\t\t\t {s}'
                                        for s in check_alg_values(
                                            scenario, chem,
                                            transport_proc.name,
                                            sender.standard_name,
                                            receiver.standard_name
                                        )
                                    ])
                                    continue  # No point in continuing
                                elif not transfer_factor:
                                    continue  # No point in continuing
                            except ValueError:
                                print_vals.extend('\t\t\t Value error!')
                                check_alg = True
                                pass

                            if transport_proc.is_transform:
                                try:
                                    real_chem_idx = chem_indices[
                                        transport_proc.output_chemical
                                    ]
                                except KeyError:
                                    real_chem_idx = -1
                                if real_chem_idx < 0:
                                    tm_y = -1
                                else:
                                    tm_y = int(real_chem_idx * n_comp + x)

                            try:
                                transition_matrix[tm_x][tm_x] -= transfer_factor
                                if tm_y > -1:
                                    transition_matrix[tm_y][tm_x] += (
                                        transfer_factor
                                    )
                            except Exception:
                                print_vals.extend(
                                    '\t\t\t Error updating transfer matrix!'
                                )
                                check_alg = True
                            if check_alg:
                                print_vals.extend([
                                    f'\t\t\t {s}'
                                    for s in check_alg_values(
                                        scenario, chem,
                                        transport_proc.name,
                                        sender.standard_name,
                                        receiver.standard_name
                                    )
                                ])

                    if len(print_vals) > 1:
                        for ln in print_vals:
                            print(ln)
    except KeyboardInterrupt:
        pass

    print(f'{"**"*20} TM Calculation Complete {"**"*20}')

    df_tm = pd.DataFrame(
        transition_matrix, index=index_names,
        columns=index_names
    )

    # ------- THIS IS FOR ARUN'S CHECKS -------
    # ts = datetime.now().strftime('%Y-%m-%d--%H_%M_%S')
    # fname_tm = f'./trim_frontend/static/.output/TM_{scenario.name}_{scenario.creator_id}_{ts}.csv'
    # df_tm.to_csv(fname_tm)
    # ----------- END ARUN'S CHECKS -----------

    try:
        df_sm = pd.DataFrame(
            source_matrix, index=index_names,
            columns=['deposition_rate_g_day-1']
        )

        df_vmu = pd.DataFrame(vmu, index=index_names,
                              columns=['comp_name', 'volume_m3', 'mass_kg', 'concentrationOutputUnits',
                                       'concentrationOutputFactor', 'denominator'])

        df_ic = pd.DataFrame({'initial_concentration': ic_matrix, 'initial_concentration_units': ic_units, }, index=index_names)
        df_n0 = compute_initial_mass(df_ic, df_vmu)  # dataframe of initial masses computed
    except Exception as a:
        print(full_stack())


    return transition_matrix, df_tm, source_matrix, df_sm, df_vmu, df_n0


def ode_sim(tm, sm, df_sm, df_n0, scn):

    tm = np.nan_to_num(tm, copy=True, nan=0.0, posinf=None, neginf=None)  # replace nans with zero
    steps_per_day = 24  # steps per day for integration and output -- will need to be input / argument eventually

    def m(t):  # transition matrix
        m = tm  #
        return m

    def s(t):  # source term
        s = sm
        #s=sm/steps_per_day # adjusts emission rate to g/integration time step
        # --not required odeint understands from the linspace statement that the
        return s

    def dn_dt(n, t):  # derivative function
        n_prime = np.matmul(m(t), n) + s(t)
        return n_prime

    ndim = sm.shape[0]  # number of compartments

    simulation_start_date = scn.sim_begin_end_time[0]
    simulation_end_date = scn.sim_begin_end_time[1]
    time_range_h = pd.date_range(simulation_start_date, simulation_end_date,
                                 freq='H')  # pandas date times series in hours over the simulation period
    time_range_d = pd.date_range(simulation_start_date, simulation_end_date,
                                 freq='D')  # pandas date times series in days over the simulation period
    ndays = len(time_range_d) - 1  # last day is not a full day
    # nhours = len(time_range_h) - 1  # last hour is not modelled
    ts = np.linspace(0, ndays, ndays * 24)  # array of hours to be modelled (in units of days because TFs are in /d)

    # ts = np.linspace(0, 365 * nyear,
    #               365 * nyear * steps_per_day)  # time line in hours for nyear years, tstart and tend should be inputs

    n0 = np.array(df_n0['n0_g'], dtype='float64')  # get initial masses
    n0 = pd.Series(n0).fillna(0).to_numpy()
    nt = odeint(dn_dt, n0, ts, hmax=24)  # mass at time t

    df_nt = pd.DataFrame(nt)
    print(df_nt)
    cols = list(df_sm.index)
    df_nt.columns = cols
    df_nt['time'] = ts
    cols_ordered = ['time'] + cols
    #
    df_nt = df_nt[cols_ordered]

    return nt, df_nt


def compute_concentration(df_nt, df_vmu):  # arguments are the chemical mass array (nt), mass dataframe

    df_vmu['Mass_to_Conc_Conv_Factor'] = np.nan
    index_list = list(df_vmu.index)
    for i in index_list:  # loop over the rows of the compartment volume mass units dataframe
        if df_vmu.loc[i, 'concentrationOutputFactor'] == np.nan:
            pass
        else:
            if 'mass' in df_vmu.loc[i, 'denominator']:
                df_vmu.loc[i, 'Mass_to_Conc_Conv_Factor'] = 1 / df_vmu.loc[i, 'mass_kg'] * df_vmu.loc[
                    i, 'concentrationOutputFactor']
            if 'volume' in df_vmu.loc[i, 'denominator']:
                df_vmu.loc[i, 'Mass_to_Conc_Conv_Factor'] = 1 / df_vmu.loc[i, 'volume_m3'] * df_vmu.loc[
                    i, 'concentrationOutputFactor']
            # need to convert volume from m3 to L for these compartments (surface water and groundwater)
            if 'volume_L' in df_vmu.loc[i, 'denominator']:
                df_vmu.loc[i, 'Mass_to_Conc_Conv_Factor'] = 1 / (df_vmu.loc[i, 'volume_m3'] * 1000) * df_vmu.loc[
                    i, 'concentrationOutputFactor']

    # col_names = [str(ii) for ii in index_list]
    # col_names = col_names + [str(ii) + '_units' for ii in index_list] + ['time', 'year']
    # df_conc = pd.DataFrame(columns=col_names)
    df_conc = pd.DataFrame()
    df_conc['time'] = df_nt['time']  # add time column

    for i in index_list:
        conv_fact = df_vmu.loc[i, 'Mass_to_Conc_Conv_Factor']
        units = df_vmu.loc[i, 'concentrationOutputUnits']
        # col_name=i+'_'+units
        col_name = i
        col_val = np.array(df_nt[i]) * conv_fact
        df_conc[col_name] = col_val
        df_conc[col_name + '_units'] = units

    df_conc = df_conc.replace(np.nan, 0)
    return df_conc


def gen_avg(df_nt, df_conc, inputs):
    # get simulation start and end dates
    start_date, end_date = inputs['simulation_start_date'], inputs['simulation_end_date']
    # convert the start_date and end_date to datetime objects
    start_date = pd.to_datetime(start_date, format='%Y-%m-%d')
    # convert the start_date and end_date to datetime objects
    end_date = pd.to_datetime(end_date, format='%Y-%m-%d')
    # convert the first col (time in d) to datetime objects
    df_nt.iloc[:, 0] = pd.to_datetime(df_nt.iloc[:, 0], origin=start_date, unit='d')
    # convert the first col (time in d) to datetime objects
    df_conc.iloc[:, 0] = pd.to_datetime(df_conc.iloc[:, 0], origin=start_date, unit='d')
    df_nt['year'] = df_nt.iloc[:, 0].dt.year   # create year column
    df_conc['year'] = df_conc.iloc[:, 0].dt.year  # create year column
    # group the data by year and calculate the annual averages
    dfn_avg = df_nt.groupby('year').mean().reset_index()
    # drop last line (just one day)
    dfn_avg = dfn_avg.head(len(dfn_avg)-1)
    # defragment the conc dataframe
    # new_df_conc = df_conc.copy()
    # group the data by year and calculate the annual averages
    # dfc_avg = df_conc.groupby('year').mean().reset_index() # this fails because of all the units (objects) in the df
    dct = {
        'number': 'mean',
        'object': lambda col: col.mode() if col.nunique() == 1 else np.nan,
    }

    groupby_cols = ['year']
    dct = {k: v for i in
           [{col: agg for col in df_conc.select_dtypes(tp).columns.difference(groupby_cols)} for tp, agg in dct.items()] for
           k, v in i.items()}
    dfc_avg = df_conc.groupby(groupby_cols).agg(**{k: (k, v) for k, v in dct.items()})
    # drop last line (just one day)
    dfc_avg = dfc_avg.head(len(dfc_avg)-1)
    return dfn_avg, dfc_avg

def check_alg_values(scenario, chemical, alg, sender, receiver):
    print_vals = []

    print_vals.append('')
    print_vals.append(alg)

    sender = scenario.get_compartment(sender)
    print_vals.append(f'sender = {sender}')
    print_vals.append(f'sender.media.id = {sender.media.id}')
    receiver = scenario.get_compartment(receiver)
    print_vals.append(f'receiver = {receiver}')
    print_vals.append(f'receiver.media.id = {receiver.media.id}')

    print_vals.append('')
    print_vals.append(f'sender.get_links(receiver) = {sender.get_links(receiver)}')

    process = TransportProcessService.get(name=alg)

    applies = process.applies_to(
        sender=sender, receiver=receiver,
        chemical=chemical
    )
    print_vals.append(f'transport_process_applies = {applies}')

    print_vals.extend(print_args(
        process.algorithm.equation, evaluator, new_names={
            'sender': sender,
            'receiver': receiver,
            'chemical': chemical,
            'environment': scenario
        }
    ))

    try:
        transfer_factor = process.eval(
            sender=sender, receiver=receiver,
            chemical=chemical,
            environment=scenario
        )
        print_vals.append(
            f'transfer_factor = {transfer_factor}'
        )
    except TypeError as e:
        if 'Invalid arguments for "' not in str(e):
            raise
        print_vals.append('Cannot evaluate transfer_factor')
    print_vals.append('')
    return print_vals


def run_full_model(scn):
    # get transition matrix and source matrix
    # if none exist create new one
    if scn.has_process_hist:
        [v for v in scn.proc_status][0].run_status = 'run tm 0'
        [v for v in scn.proc_status][0].run_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    else:
        try:
            new_proc = ScenarioLoadRunProc(scenario=scn, load_status='load 100', run_status='run null null',
                                           run_datetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            [scn.proc_status][0].add(new_proc)
        except Exception as e:
            print(e)
    ScenarioService.commit()
    scn = ScenarioService.get(id=scn.id)
    try:
        (tm, df_tm, sm, df_sm, df_vmu, df_n0) = make_transition_matrix(scn)
    except Exception as e:
        print(full_stack())
        return model_err(scn, f"ERRORED WHILE MAKING TRANSITION MATRIX: {e}", 'err tm 0')

    # get result
    [v for v in scn.proc_status][0].run_status = 'run ode 0'
    ScenarioService.commit()
    scn = ScenarioService.get(id=scn.id)
    try:
        (nt, df_nt) = ode_sim(tm, sm, df_sm, df_n0, scn)
        [v for v in scn.proc_status][0].run_status = 'run ode 50'
        ScenarioService.commit()
        # make concentration output
        df_conc = compute_concentration(df_nt, df_vmu)
    except Exception as e:
        print(full_stack())
        return model_err(scn, f"ERRORED WHILE MAKING CONCENTRATION OUTPUT: {e}", 'err ode 0')

    # compute annual average mass and conc time series
    inputs = {
        'simulation_start_date': scn.sim_begin_end_time[0],  # scn.simulationBeginDate,
        'simulation_end_date': scn.sim_begin_end_time[1]  # scn.simulationEndDate
    }
    try:
        dfn_avg, dfc_avg = gen_avg(df_nt, df_conc, inputs)
        json_n_avg = dfn_avg.to_json(orient='columns')[1:-1].replace('},{', '} {')
        json_c_avg = dfc_avg.to_json(orient='columns')[1:-1].replace('},{', '} {')
    except Exception as e:
        return model_err(scn, f"ERRORED WHILE COMPUTING AVERAGES: {e}", 'err ode 0')

    outfile_nt, outfile_conc = "", ""

    # Output components as csv
    # df_tm.to_csv("Transfer_Matrix_test.csv")
    # df_sm.to_csv("Source_Matrix_test.csv")
    # df_nt.to_csv("Result_Matrix_test.csv")
    # df_conc.to_csv("Concentration_Result_Matrix_test.csv")

    [v for v in scn.proc_status][0].run_status = 'run csv 0'
    ScenarioService.commit()
    scn = ScenarioService.get(id=scn.id)
    try:
        outfile_nt, outfile_conc = safe_save_output(dfn_avg, dfc_avg, scn, filetype='excel')
        # safe_save_output(df_nt, df_conc, scn, filetype='excel')
        [v for v in scn.proc_status][0].result_file_nt = outfile_nt
        [v for v in scn.proc_status][0].result_file_conc = outfile_conc
        [v for v in scn.proc_status][0].run_status = 'run fin 100'
        [v for v in scn.proc_status][0].result_nt = json.dumps(json_n_avg, default=str)
        [v for v in scn.proc_status][0].result_conc = json.dumps(json_c_avg, default=str)
    except Exception as e:
        return model_err(scn, f"ERRORED WHILE MAKING CSV: {e}", 'err csv 0')
    ScenarioService.commit()

    return json_n_avg, json_c_avg, outfile_nt, outfile_conc


def model_err(scn, err_msg, status):
    print(err_msg)
    [v for v in scn.proc_status][0].run_status = status
    ScenarioService.commit()
    return {}, {}, "", ""


def safe_save_output(df_nt, df_conc, scn, filetype='csv'):
    try:
        ts = datetime.now().strftime('%Y-%m-%d--%H_%M_%S')
        sim_chems = [c.name for c in scn.chemicals]
        if not os.path.isdir('./trim_frontend/static/.output'):
            os.makedirs('./trim_frontend/static/.output')
        if filetype == 'csv':
            fname_nt = f'./trim_frontend/static/.output/nt_new_{scn.name}_{scn.creator_id}_{ts}.csv'
            fname_conc = f'./trim_frontend/static/.output/conc_new_{scn.name}_{scn.creator_id}_{ts}.csv'
            df_nt.to_csv(fname_nt)
            df_conc.to_csv(fname_conc)
        else:
            path_output_nt = './trim_frontend/static/.output/'
            just_name_nt = f'nt_new_{scn.name}_{scn.creator_id}_{ts}.xlsx'
            fname_nt = os.path.join(path_output_nt, just_name_nt)

            path_output_conc = './trim_frontend/static/.output/'
            just_name_conc = f'conc_new_{scn.name}_{scn.creator_id}_{ts}.xlsx'
            fname_conc = os.path.join(path_output_conc, just_name_conc)

            split_write_files(df_nt, sim_chems, fname_nt)
            split_write_files(df_conc, sim_chems, fname_conc)
    except Exception as e:
        print(f'{20 * ">"} Output write exception writing {filetype} file:\n{e}')
        fname_nt = "No File. There was an error while writing output..."
        fname_conc = "No File. There was an error while writing output..."
    return fname_nt, fname_conc


def split_write_files(df, sim_chems, of_pn):
    # Helper function to split and write time series files into excel workbook with multiple worksheets
    writer = pd.ExcelWriter(of_pn, engine='xlsxwriter')
    for chem in sim_chems:  # loop over sim chemicals
        # prefix = 'chem_'+chem.replace(' ', '_') + '_'  # construct prefix
        prefix = chem + '_'  # construct prefix
        dft = df[[df.columns[0]]+[x for x in list(df.columns) if prefix in x]]  # keep time/year and cols with prefix
        dft.columns = [x.replace(prefix, '') for x in list(dft.columns)]  # strip prefix
        # Write each dataframe to a different worksheet.
        dft.to_excel(writer, sheet_name=chem, index=False)
    writer.close()
    return()



def print_args(equation, evaluator, new_names={}, depth=0):
    print_vals = []
    print_vals.append('')
    print_vals.append('--' * 15)
    print_vals.append(equation)
    print_vals.append('--' * 15)
    old_names = dict(evaluator.names)
    evaluator.names.update(new_names)
    try:
        eval_args = evaluated_args(equation, evaluator)
        for k in sorted(eval_args.keys()):
            if k in evaluator.names:
                continue
            v = eval_args[k]
            if str(v).startswith('<function '):
                continue
            if str(v).startswith('<bound method '):
                continue

            print_vals.append(f'{k} = {v}')
            continue
            if not isinstance(v, NoEval):
                print_vals.append(f'{k} = {v}')
            else:
                param = k.rsplit('.', 1)
                if len(param) != 2:
                    print_vals.append(f'{k} = {v} (<None>)')
                    continue
                obj = param[0]
                obj = obj.split('.', 1)
                obj[0] = f'evaluator.names.get("{obj[0]}")'
                # print_vals.append('.'.join(obj))
                try:
                    obj = eval('.'.join(obj))
                except Exception as e:
                    print_vals.append(f'{k} = {v} ({e})')
                    continue
                if obj is None:
                    print_vals.append(f'{k} = {v} (<None>)')
                    continue
                param = param[1]
                if '(' in param:
                    param = param.split('(')
                    args = param[1]
                    param = param[0]
                    args = [
                        x.strip()
                        for x in args.replace(')', '').split(',')
                    ]
                else:
                    args = []
                param = obj.parameters.get(param)
                if param is None:
                    print_vals.append(f'{k} = {v} (<None>)')
                    continue
                # print_vals.append(f'{k} = {param}({", ".join(args)})')
                try:
                    param.quantity
                except AttributeError:
                    print_vals.append(
                        f'\t-> {k} = {param} has no quantity'
                    )
                try:
                    print_vals.append(
                        f'\t-> Evaluating {k} = {param}'
                    )
                    print_vals.extend(print_args(
                        param.quantity.equation, evaluator,
                        new_names={
                            'self': obj,
                            **{
                                x: eval(x) for x in args
                            }
                        },
                        depth=(depth + 1)
                    ))
                except AttributeError:
                    print_vals.append(
                        f'\t-> {k} = {param.quantity} is not an equation'
                    )
    finally:
        evaluator.names = old_names
    print_vals.append('--' * 15)
    # print(print_vals)
    print_vals = [('\t' * depth) + s for s in print_vals]
    return print_vals
