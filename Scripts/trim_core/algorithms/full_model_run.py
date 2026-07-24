import os
import pandas as pd
import numpy as np
import json
import time
from pandas.api.types import is_numeric_dtype
from scipy.integrate import odeint
from trim_db.schema import *
from trim_db.schema.parameters.equations import evaluated_args, \
    evaluator, NoEval
from trim_db.services import *
from datetime import datetime

__all__ = ['run_full_model']

DEBUG = os.getenv('DEBUG_TRANSITION_MATRIX')
RESTRICT_COMPARTMENTS = [
    x.strip()
    for x in str(os.getenv('TRANSITION_MATRIX_COMPARTMENTS', '')).split(',')
    if x.strip()
]


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

    matrix_dimensions = n_chem * n_comp

    transition_matrix = np.zeros(
        (matrix_dimensions, matrix_dimensions), dtype=float
    )

    index_names = ['' for _ in transition_matrix]

    source_matrix = []
    ic_matrix = []
    vmu = []

    chem_indices = {
        c: i for i, c in enumerate(chem_list)
    }

    i_perc = int(100 / n_chem)

    def update_source_matrix(chem, comp):
        try:
            dr = comp.surfaceDepositionRate(chem)
            if not pd.isna(dr):
                chem_comp_name = chem.name + '_' + comp.standard_name
                source_matrix.append((chem_comp_name, dr.magnitude))
        except Exception:
            print(
                f'{"*" * 20}'
                f' Problem with getting Surface Deposition Rate'
                f' for compartment={comp.name}, chemical={chem}'
                f' {"*" * 20}'
                f'\nException is {full_stack()}'
            )

    def update_ic_matrix(chem, comp):
        chem_comp_name = chem.name + '_' + comp.standard_name

        try:
            ic = comp.initialConcentration(chem)
            ic_units = 'g/kg'
            if not pd.isna(ic):
                if hasattr(ic, 'dimensionality'):
                    ic_units = str(ic.units).replace(" ", "").replace("**", "^")
                    ic = ic.magnitude
                ic_matrix.append((chem_comp_name, ic, ic_units))
            else:
                ic_matrix.append((chem_comp_name, 0, ic_units))
        except Exception:
            print(
                f'{"*" * 20}'
                f' Problem with getting Initial Concentration'
                f' for compartment={comp.name}, chemical={chem}'
                f' {"*" * 20}'
                f'\nException is {full_stack()}'
            )

    def update_vmu(chem, comp):
        if comp.media.isa('Sink') or comp.media.isa('Air'):
            # Ignore sinks and air entirely (concentration is meaningless)
            return

        chem_comp_name = chem.name + '_' + comp.standard_name

        try:
            # if sending compartment has volume (m3)
            vol = comp.Volume
            if not pd.isna(vol) and vol:
                vol = vol.magnitude
            else:
                vol = np.nan

            # if sending compartment has mass (kg)
            mass = comp.TotalMass
            if not pd.isna(mass) and mass:
                mass = mass.magnitude
            else:
                mass = np.nan

            # if sending compartment has concentration output factor
            is_soil = comp.media.isa('Soil')
            cof = comp.concentrationOutputFactor
            cou = ''
            if pd.isna(cof) or (not cof):
                if is_soil:
                    cof = chem.concentrationOutputFactor(comp)
                    if hasattr(cof, 'dimensionality'):
                        cou = str(cof.units)
                        cof = cof.magnitude
                else:
                    cof = np.nan
                    cou = ''
            else:
                if hasattr(cof, 'dimensionality'):
                    cou = str(cof.units)
                    cof = cof.magnitude

            # denominator in concentration calculation
            if comp.media.isa("Surface_Water") or comp.media.isa("Groundwater"):
                # note that denom must be in L
                denom = "volume_L"
            elif (
                comp.media.isa("Abiotic")
                or comp.media.isa("$Leaf")
                or comp.media.isa("$Leaf_Particle")
            ):
                denom = "volume"
            else:
                denom = "mass"  # default denom is mass

            # tuples of volume, mass, units, output factor, and denominator quantity
            vmu_tup = (chem_comp_name, comp.name, vol, mass, cou, cof, denom)
        except Exception:
            print(
                f'{"*" * 20}'
                f' Problem with getting Surface Concentration Output factor'
                f' for compartment={comp.name}, chemical={chem}'
                f' {"*" * 20}'
                f'\nException is {full_stack()}'
            )
            vmu_tup = (chem_comp_name, comp.name, np.nan, np.nan, '', np.nan, 'mass')

        vmu.append(vmu_tup)

    def update_other_matrices(chem, comp):
        update_source_matrix(chem, comp)
        update_ic_matrix(chem, comp)
        update_vmu(chem, comp)

    try:
        ureg.default_format = '~'
        for chem_idx, chem in enumerate(chem_list):
            this_perc = i_perc * chem_idx
            scenario.latest_proc_status.run_status = f'run tm {this_perc}'
            ScenarioService.commit(preserve_cache=True)
            # if chem.name != 'Elemental Mercury':
            #     continue
            print('\n' + '==' * 28)
            print(f'Chemical = {chem.name}')
            print('==' * 28)

            for x, sender in enumerate(comp_list):
                if (x % 100) == 0:
                    comp_perc = int(this_perc + ((i_perc * x) / n_comp))
                    scenario.latest_proc_status.run_status = f'run tm {comp_perc}'
                    ScenarioService.commit(preserve_cache=True)
                tm_x = int(chem_idx * n_comp + x)

                index_names[tm_x] = chem.name + '_' + sender.standard_name

                update_other_matrices(chem, sender)

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
                            if hasattr(transfer_factor, 'dimensionality'):
                                transfer_factor = transfer_factor.magnitude
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

    try:
        df_sm = pd.DataFrame(
            source_matrix, columns=['chem_sender_name', 'deposition_rate_g_day-1']
        ).set_index('chem_sender_name')
        df_sm.index.name = None

        df_vmu = pd.DataFrame(
            vmu, columns=[
                'chem_sender_name',
                'comp_name',
                'volume_m3',
                'mass_kg',
                'concentrationOutputUnits',
                'concentrationOutputFactor',
                'denominator'
            ]
        ).set_index('chem_sender_name')
        df_vmu.index.name = None

        df_c0 = pd.DataFrame(
            ic_matrix, columns=[
                'chem_sender_name',
                'initial_concentration',
                'initial_concentration_units'
            ]
        ).set_index('chem_sender_name')
        df_c0.index.name = None

    except Exception as a:
        print(full_stack())

    return df_tm, df_sm, df_vmu, df_c0


def compute_initial_mass(df_c0, df_vmu):
    # arguments are the chemical mass array (nt), mass dataframe
    df = df_c0.merge(df_vmu, how='left', left_index=True, right_index=True)

    def compute_mass(row):
        try:
            ic_units = row.initial_concentration_units
            ic_val = row.initial_concentration
            if ic_units == 'g/m^3':
                return ic_val * row.volume_m3
            elif ic_units == 'g/L':
                return ic_val * row.volume_m3 * 1000
            elif ic_units == 'g/kg':
                return ic_val * row.mass_kg
        except Exception:
            pass
        return 0

    df['n0_g'] = df.apply(compute_mass, axis=1)

    df_n0 = df[['initial_concentration_units', 'n0_g']]

    return df_n0


def ode_sim(df_tm, df_sm, df_n0, simulation_start_date, simulation_end_date):
    sm = df_sm['deposition_rate_g_day-1']
    tm = np.nan_to_num(
        df_tm.to_records(index=False).tolist(),
        copy=True,
        nan=0.0,  # replace nans with zero
        posinf=None,
        neginf=None
    )
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

    time_range_d = pd.date_range(  # date times series in days over the simulation period
        simulation_start_date, simulation_end_date, freq='D'
    )
    ndays = len(time_range_d)
    ts = np.linspace(0, ndays, ndays * 24)  # array of hours to be modelled (in units of days because TFs are in /d)

    n0 = np.array(df_n0['n0_g'], dtype='float64')  # get initial masses
    n0 = pd.Series(n0).fillna(0).to_numpy()

    df_nt = pd.DataFrame(odeint(dn_dt, n0, ts, hmax=24))  # mass at time t
    # print(df_nt)
    cols = list(df_sm.index)
    df_nt.columns = cols
    df_nt['time'] = ts
    cols_ordered = ['time'] + [c for c in cols if not ('Air in ' in c)]

    df_nt = df_nt[cols_ordered]

    return df_nt


def compute_concentration(df_nt, df_vmu):  # arguments are the chemical mass array (nt), mass dataframe
    conc_data = {
        'time': df_nt['time']
    }

    for row in df_vmu.itertuples():  # loop over the rows of the compartment volume mass units dataframe
        conc_out_factor = row.concentrationOutputFactor
        mass_conc_conv_factor = np.nan
        if conc_out_factor != np.nan:
            if 'mass' in row.denominator:
                mass_conc_conv_factor = conc_out_factor / row.mass_kg
            if 'volume' in row.denominator:
                mass_conc_conv_factor = conc_out_factor / row.volume_m3
            # need to convert volume from m3 to L for these compartments (surface water and groundwater)
            if 'volume_L' in row.denominator:
                mass_conc_conv_factor = conc_out_factor / (row.volume_m3 * 1000)

        full_name = row.Index
        conc_data[full_name] = df_nt[full_name] * mass_conc_conv_factor
        conc_data[f'{full_name}_units'] = pd.Series(
            [row.concentrationOutputUnits] * len(conc_data[full_name])
        )

    df_conc = pd.concat(conc_data.values(), axis=1, ignore_index=True)
    df_conc.columns = conc_data.keys()

    df_conc = df_conc.replace(np.nan, 0)

    # safe_save_output([
    #     {'abbr': 'debug_nt', 'df': df_nt},
    #     {'abbr': 'debug_vmu', 'df': df_vmu},
    #     {'abbr': 'debug_conc', 'df': df_conc}
    # ])

    return df_conc


def gen_avg(df_nt, df_conc, simulation_start_date):
    # get simulation start date and convert to datetime object
    start_date = pd.to_datetime(simulation_start_date, format='%Y-%m-%d')

    # convert the first col (time in d) to datetime objects
    df_nt['time'] = pd.to_datetime(df_nt['time'], origin=start_date, unit='d')
    df_nt['year'] = df_nt['time'].dt.year   # create year column
    # group the data by year and calculate the annual averages
    dfn_avg = df_nt.groupby('year').mean().reset_index()

    # convert the first col (time in d) to datetime objects
    df_conc['time'] = pd.to_datetime(df_conc['time'], origin=start_date, unit='d')
    df_conc['year'] = df_conc['time'].dt.year  # create year column
    # group the data by year and calculate the annual averages
    conc_agg = {
        c: (
            'mean' if (c == 'time') or is_numeric_dtype(df_conc[c])
            else lambda col: (col.mode() if col.nunique() == 1 else np.nan)
        )
        for c in df_conc.columns.values if c != 'year'
    }
    dfc_avg = df_conc.groupby('year').agg(conc_agg).reset_index()
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
    st = time.time()
    try:
        # get transition matrix and source matrix
        # if none exist create new one
        run_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if scn.has_process_hist:
            scn.latest_proc_status.run_status = 'run tm 0'
            scn.latest_proc_status.run_datetime = run_time
        else:
            try:
                new_proc = ScenarioLoadRunProc(
                    scenario=scn,
                    load_status='load 100', run_status='run null null',
                    run_datetime=run_time
                )
                scn.proc_status.add(new_proc)
            except Exception as e:
                print(e)
        ScenarioService.commit()
        scn = ScenarioService.get(scn.id)
        try:
            (df_tm, df_sm, df_vmu, df_c0) = make_transition_matrix(scn)
        except Exception as e:
            print(full_stack())
            return model_err(scn, f"ERRORED WHILE MAKING TRANSITION MATRIX: {e}", 'err tm 0')

        try:
            df_n0 = compute_initial_mass(df_c0, df_vmu)  # dataframe of initial masses computed
        except Exception as e:
            print(full_stack())
            return model_err(scn, f"ERRORED WHILE COMPUTING INITIAL MASS: {e}", 'err tm 0')

        # get result
        scn.latest_proc_status.run_status = 'run ode 0'
        ScenarioService.commit()
        scn = ScenarioService.get(scn.id)
        try:
            df_nt = ode_sim(df_tm, df_sm, df_n0, scn.start_date, scn.end_date)
            scn.latest_proc_status.run_status = 'run ode 50'
            ScenarioService.commit()
            # make concentration output
            df_conc = compute_concentration(df_nt, df_vmu)
        except Exception as e:
            print(full_stack())
            return model_err(scn, f"ERRORED WHILE MAKING CONCENTRATION OUTPUT: {e}", 'err ode 0')

        # compute annual average mass and conc time series
        try:
            dfn_avg, dfc_avg = gen_avg(df_nt, df_conc, scn.start_date)
            json_n_avg = dfn_avg.to_json(orient='columns')[1:-1].replace('},{', '} {')
            json_c_avg = dfc_avg.to_json(orient='columns')[1:-1].replace('},{', '} {')
        except Exception as e:
            return model_err(scn, f"ERRORED WHILE COMPUTING AVERAGES: {e}", 'err ode 0')

        scn.latest_proc_status.run_status = 'run csv 0'
        ScenarioService.commit()
        scn = ScenarioService.get(scn.id)

        try:
            outfiles = safe_save_output([
                {'abbr': 'nt', 'df': dfn_avg, 'split_chems': True},
                {'abbr': 'conc', 'df': dfc_avg, 'split_chems': True},
                {'abbr': 'tm', 'df': df_tm, 'testing_only': True}
            ], scn, filetype='excel')

            file_error_txt = 'No File. There was an error while writing output...'
            outfile_nt = outfiles.get('nt', file_error_txt)
            outfile_conc = outfiles.get('conc', file_error_txt)
            outfile_tm = outfiles.get('tm', file_error_txt)
        except Exception as e:
            return model_err(scn, f"ERRORED WHILE MAKING CSV: {e}", 'err csv 0')

        try:
            scn.latest_proc_status.run_status = 'run fin 0'

            scn.latest_proc_status.result_file_nt = outfile_nt
            scn.latest_proc_status.result_file_conc = outfile_conc
            scn.latest_proc_status.result_file_tm = outfile_tm

            scn.latest_proc_status.result_nt = json.dumps(json_n_avg, default=str)
            scn.latest_proc_status.result_conc = json.dumps(json_c_avg, default=str)

            scn.latest_proc_status.run_status = 'run fin 100'

            ScenarioService.commit()
        except Exception as e:
            return model_err(scn, f"ERRORED WHILE UPDATING DB: {e}", 'err fin 0')

        return json_n_avg, json_c_avg, outfile_nt, outfile_conc, outfile_tm
    finally:
        et = time.time()
        print(f'Ran model in {(et - st) / 60:.4f} min')


def model_err(scn, err_msg, status):
    print(err_msg)
    # import traceback; traceback.print_exc()
    if ' fin ' in status:
        new_status = status  # force the provided status
    else:
        try:
            # Try to see if we can replace the old status with an err status
            # while keeping progress indicators
            old_status = scn.latest_proc_status.run_status
            new_status = 'err ' + old_status.split(' ', 1)[1]
        except Exception:
            # Just use the provided status
            new_status = status
    try:
        scn.latest_proc_status.run_status = new_status
        ScenarioService.commit()
    except Exception:
        pass
    return {}, {}, "", "", ""


def safe_save_output(output_data, scn=None, filetype='csv'):
    outfiles = {}
    try:
        ts = datetime.now().strftime('%Y-%m-%d--%H_%M_%S')

        out_dir = './trim_frontend/static/.output'
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)

        sim_chems = []
        if filetype != 'csv':
            if scn is not None:
                sim_chems = [c.name for c in scn.chemicals]

        user_has_tester_role = False
        if scn is not None:
            user_has_tester_role = (
                len([r.name for r in scn.creator.roles if r.name == 'tester']) > 0
                or scn.creator.email.endswith("@icf.com")
            )

        if scn is not None:
            fname_suff = f'new_{scn.name}_{scn.creator_id}_{ts}'
        else:
            fname_suff = f'temp_{ts}'

        for data in output_data:
            abbr = data['abbr']
            if data.get('testing_only') and not user_has_tester_role:
                outfiles[abbr] = ''
                continue

            df = data['df']
            fname = os.path.join(out_dir, f'{abbr}_{fname_suff}')
            print(f'\t> Saving "{fname}" ...')
            try:
                if filetype == 'csv':
                    fname += '.csv'
                    df.to_csv(fname)
                else:
                    fname += '.xlsx'
                    if data.get('split_chems'):
                        split_write_files(df, sim_chems, fname)
                    else:
                        writer = pd.ExcelWriter(fname, engine='xlsxwriter')
                        df.to_excel(writer)
                        writer.close()
                outfiles[abbr] = fname
            except Exception:
                print(f'{20 * ">"} Output write exception writing {filetype} file for {abbr} data:\n{e}')
    except Exception as e:
        print(f'{20 * ">"} Output write exception writing {filetype} file:\n{e}')
    return outfiles


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
