import os
import pandas as pd
import numpy as np
from scipy.integrate import odeint
from trim_db.schema import *
from trim_db.schema.parameters.equations import evaluated_args, \
    evaluator, NoEval
from trim_db.services import *

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

sim_begin_date = "01/01/1990"
sim_end_date = "01/01/2040"

def is_compartment_of_interest(comp):
    if not RESTRICT_COMPARTMENTS:
        return True
    for x in RESTRICT_COMPARTMENTS:
        if x in comp.standard_name:
            return True
    return False


def make_transition_matrix(scenario):
    # a=ScenarioService.get(scenario.id)
    # b=ParcelService.get(id=1)
    # c=ParameterService.get(id=1)
    # d=CompartmentService.get(id=1)
    # e=TransportProcessService.get(id=1)
    # f=ChemicalService.get(id=1)
    # gg=VolumeElementService.get(id=1)
    # hg=FormulaService.get(id=1)

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
    transition_matrix = np.zeros(
        (matrix_dimensions, matrix_dimensions), dtype=float
    )

    index_names = ['' for _ in source_matrix]

    chem_indices = {
        c: i for i, c in enumerate(chem_list)
    }

    try:
        for chem_idx, chem in enumerate(chem_list):
            # if chem.name != 'Elemental Mercury':
            #     continue
            print('\n' + '==' * 28)
            print(f'Chemical = {chem.name}')
            print('==' * 28)

            for x, sender in enumerate(comp_list):
                tm_x = int(chem_idx * n_comp + x)

                index_names[tm_x] = chem.name + '_' + sender.standard_name

                try:
                    dr = sender.surfaceDepositionRate(chem)
                    if not (str(dr) == 'nan'):
                        source_matrix[tm_x] += dr.magnitude
                except Exception:
                    print(f'{"*" * 20} Problem with getting Surface Deposition Rate for compartment={sender.name}, '
                          f'chemical={chem} {"*" * 20}')
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
                except Exception:
                    print(f'{"*" * 20} Problem with getting Surface Concentration Output factor for '
                          f'compartment={sender.name}, chemical={chem} {"*" * 20}')

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
    df_sm = pd.DataFrame(
        source_matrix, index=index_names,
        columns=['deposition_rate_g_day-1']
    )

    df_vmu = pd.DataFrame(vmu, index=index_names,
                          columns=['comp_name', 'volume_m3', 'mass_kg', 'concentrationOutputUnits',
                                   'concentrationOutputFactor', 'denominator'])

    return transition_matrix, df_tm, source_matrix, df_sm, df_vmu


def ode_sim(tm, sm, df_sm, scn):

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

    simulation_start_date = sim_begin_date  # scn.simulationBeginDateTime
    simulation_end_date = sim_end_date  # scn.simulationEndDateTime
    time_range_h = pd.date_range(simulation_start_date, simulation_end_date,
                                 freq='H')  # pandas date times series in hours over the simulation period
    time_range_d = pd.date_range(simulation_start_date, simulation_end_date,
                                 freq='D')  # pandas date times series in days over the simulation period
    ndays = len(time_range_d) - 1  # last day is not a full day
    # nhours = len(time_range_h) - 1  # last hour is not modelled
    ts = np.linspace(0, ndays, ndays * 24)  # array of hours to be modelled (in units of days because TFs are in /d)

    # ts = np.linspace(0, 365 * nyear,
    #               365 * nyear * steps_per_day)  # time line in hours for nyear years, tstart and tend should be inputs

    n0 = np.zeros(ndim)  # zero mass initial condition
    nt = odeint(dn_dt, n0, ts, hmax=24)  # mass at time t

    df_nt = pd.DataFrame(nt)
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
    start_date = pd.to_datetime(start_date, format='%d/%m/%Y')
    # convert the start_date and end_date to datetime objects
    end_date = pd.to_datetime(end_date, format='%d/%m/%Y')
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
    scn.description = 'tm'
    ScenarioService.commit()
    (tm, df_tm, sm, df_sm, df_vmu) = make_transition_matrix(scn)

    # get result
    scn.description = 'ode'
    ScenarioService.commit()
    (nt, df_nt) = ode_sim(tm, sm, df_sm, scn)

    # make concentration output
    df_conc = compute_concentration(df_nt, df_vmu)

    print(df_conc)

    # compute annual average mass and conc time series
    inputs = {
        'simulation_start_date': sim_begin_date,  # scn.simulationBeginDate,
        'simulation_end_date': sim_end_date  # scn.simulationEndDate
    }
    print(inputs)
    dfn_avg, dfc_avg = gen_avg(df_nt, df_conc, inputs)
    json_n_avg = dfn_avg.to_json(orient='columns')[1:-1].replace('},{', '} {')
    json_c_avg = dfc_avg.to_json(orient='columns')[1:-1].replace('},{', '} {')

    # Output components as csv
    # df_tm.to_csv("Transfer_Matrix_test.csv")
    # df_sm.to_csv("Source_Matrix_test.csv")
    # df_nt.to_csv("Result_Matrix_test.csv")
    # df_conc.to_csv("Concentration_Result_Matrix_test.csv")

    scn.description = 'csv'
    ScenarioService.commit()
    safe_save_output(dfn_avg, dfc_avg, scn.name, scn.creator_id)
    # safe_save_output(df_nt, df_conc, scn.name, scn.creator_id)

    scn.description = 'fin'
    ScenarioService.commit()

    return json_n_avg, json_c_avg


def safe_save_output(df_nt, df_conc, scn_name, usr_id):
    try:
        if not os.path.isdir('./trim_frontend/static/.output'):
            os.makedirs('./trim_frontend/static/.output')
        df_nt.to_csv(f'./trim_frontend/static/.output/nt_new_{scn_name}_{usr_id}.csv')
        df_conc.to_csv(f'./trim_frontend/static/.output/conc_new_{scn_name}_{usr_id}.csv')
    except Exception:
        pass


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
