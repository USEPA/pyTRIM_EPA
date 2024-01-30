import warnings
# warnings.warn(
#     (
#         '\n'
#         '\n============================================================='
#         '\nDEPRECATED'
#         '\n-------------------------------------------------------------'
#         '\nThis version of the code for generating a transfer matrix'
#         ' has been deprecated; check out Scripts/generate_tm.py instead!'
#         '\n============================================================='
#         '\n'
#     ),
#     DeprecationWarning
# )
# if input('Continue? [Y/N] ').upper() != 'Y':
#     import sys
#     sys.exit()

# import termios
import time
import types
import numpy as np
from scipy.integrate import odeint
import pandas as pd

from trim_db.porting import *
from trim_db.schema import *
from trim_db.services import *


SCENARIO_NAME = 'Foundries_SS'
CHEMICAL_CATEGORY = 'Mercury'


def make_transfer_matrix(scenario):
    # import pandas as pd
    # import numpy as np

    chem_list = list(sorted(
        scenario.chemicals, key=lambda xcl: xcl.name
    ))

    # -- TEMPORARILY SHORTEN CHEMICAL LIST (COMMENT OUT FOR TM COMPARISON)
    # chem_list = [chem_list[0]]
    # -- --

    comp_list = list(sorted(
        scenario.compartments, key=lambda xl: xl.standard_name
    ))

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

    problem_tfm_file = open("Problem_TFM_components.txt", "a")
    for chem_idx, chem in enumerate(chem_list):
        problem_tfm_file.write(f"{20*'-'} Chemical: {chem} {20*'-'} Scenario: {chem.current_scenario()} {20*'-'} \n")
        print('\n' + '==' * 28)
        print(f'Chemical = {chem.name} **** Scenario: {chem.current_scenario()}')
        print('==' * 28)
        for x, sender in enumerate(comp_list):
            tm_x = int(chem_idx * n_comp + x)
            index_names[tm_x] = chem.name + '_' + sender.standard_name
            dr = sender.surfaceDepositionRate(chem)

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

            if not (str(dr) == 'nan'):
                source_matrix[tm_x] += dr.magnitude
            if not sender.media.can_emit:
                continue
            for y, receiver in enumerate(comp_list):
                if not receiver.media.can_absorb:
                    continue
                links = sender.get_links(receiver)
                if not links:
                    continue
                tm_y = int(chem_idx * n_comp + y)
                for link in links:
                    for transport_proc in link.transport_processes(chem):
                        try:
                            transfer_factor = transport_proc.eval(sender=sender, receiver=receiver,
                                                                  chemical=chem, environment=scenario)
                            print(f"{sender.name} -> {receiver.name}: ")
                        except Exception as err:
                            print(f"{20*'*'} EVAL PROBLEM {20*'*'} {sender.name} -> {receiver.name}: {transport_proc.name}\n{str(err)}")
                            problem_tfm_file.write(f"EVAL PROBLEM: {sender.name} -> {receiver.name}: {transport_proc.name}: {str(err)}\n")
                            pass
                        try:
                            if not isinstance(transfer_factor, float) and not isinstance(transfer_factor, int):
                                if isinstance(transfer_factor, types.FunctionType):
                                    transfer_factor = eval(f'transfer_factor()')
                                else:
                                    transfer_factor = transfer_factor.magnitude
                            elif pd.isna(transfer_factor):
                                print(f"{20 * '*'} NAN PROBLEM {20 * '*'}")
                                problem_tfm_file.write(
                                    f"NAN PROBLEM: {sender.name} -> {receiver.name}: {transport_proc.name}, id: "
                                    f"{transport_proc.algorithm_id}\n")
                            print(f"{transport_proc.name}: {transfer_factor} ({transport_proc.algorithm_id})\n")
                        except Exception as err:
                            print(
                                f"{20 * '*'} MAG PROBLEM {20 * '*'} {sender.name} -> {receiver.name}: {transport_proc.name}")
                            problem_tfm_file.write(
                                f"MAG PROBLEM: {sender.name} -> {receiver.name}: {transport_proc.name}: {str(err)}\n")
                            pass
                        try:
                            if (not transfer_factor or pd.isna(transfer_factor)):
                                continue
                        except ValueError as err:
                            print(
                                f"{20 * '*'} VALUE PROBLEM {20 * '*'} {sender.name} -> {receiver.name}: {transport_proc.name}")
                            problem_tfm_file.write(
                                f"VALUE PROBLEM: {sender.name} -> {receiver.name}: {transport_proc.name}: {str(err)}\n")
                            pass
                        if transport_proc.is_transform:
                            try:
                                real_chem_idx = chem_indices[transport_proc.output_chemical]
                            except KeyError:
                                real_chem_idx = -1
                            if real_chem_idx < 0:
                                tm_y = -1
                            else:
                                tm_y = int(real_chem_idx * n_comp + x)
                        try:
                            transition_matrix[tm_x][tm_x] -= transfer_factor
                            if tm_y > -1:
                                transition_matrix[tm_y][tm_x] += (transfer_factor)
                        except Exception as err:
                            print(
                                f"{20 * '*'} TM PROBLEM {20 * '*'} {sender.name} -> {receiver.name}: {transport_proc.name}")
                            problem_tfm_file.write(
                                f"TM PROBLEM: {sender.name} -> {receiver.name}: {transport_proc.name}: {str(err)}\n")
                            pass

    problem_tfm_file.close()

    df_tm = pd.DataFrame(
        transition_matrix, index=index_names,
        columns=index_names)
    df_sm = pd.DataFrame(
        source_matrix, index=index_names,
        columns=['deposition_rate_g_day-1'])
    df_vmu = pd.DataFrame(vmu, index=index_names,
                          columns=['comp_name', 'volume_m3', 'mass_kg', 'concentrationOutputUnits',
                                   'concentrationOutputFactor', 'denominator'])
    df_vmu.to_csv('VMU_DATA.csv')

    return transition_matrix, df_tm, source_matrix, df_sm, df_vmu


def ode_sim(tm, df_tm, sm, df_sm, scn):

    tm = np.nan_to_num(tm, copy=True, nan=0.0, posinf=None, neginf=None)  # replace nans with zero
    steps_per_day = 24  # steps per day for integration and output -- will need to be input / argument eventually

    def m(t):  # transition matrix
        m = tm  #
        return (m)

    def s(t):  # source term
        s = sm
        #        s=sm/steps_per_day # adjusts emission rate to g/integration time step --not required odeint understands from the linspace statement that the
        return (s)

    def dn_dt(n, t):  # derivative function
        n_prime = np.matmul(m(t), n) + s(t)
        return (n_prime)

    ndim = sm.shape[0]  # number of compartments

    simulation_start_date = "01/01/2001" # scn.simulationBeginDateTime
    simulation_end_date = "01/01/2050" # scn.simulationEndDateTime
    # time_range_h = pd.date_range(simulation_start_date, simulation_end_date,
    #                              freq='H')  # pandas datetimes series in hours over the simulation period
    time_range_d = pd.date_range(simulation_start_date, simulation_end_date,
                                 freq='D')  # pandas datetimes series in days over the simulation period
    ndays = len(time_range_d) - 1  # last day is not a full day
    # nhours = len(time_range_h) - 1  # last hour is not modelled
    ts = np.linspace(0, ndays, ndays * 24)  # array of hours to be modelled (in units of days because TFs are in /d)

    # ts = np.linspace(0, 365 * nyear,
    #                  365 * nyear * steps_per_day)  # time line in hours for nyear years, tstart and tend should be inputs

    n0 = np.zeros(ndim)  # zero mass initial condition
    nt = odeint(dn_dt, n0, ts, hmax=24)  # mass at time t

    df_nt = pd.DataFrame(nt)
    cols = list(df_sm.index)
    df_nt.columns = cols
    df_nt['time_in_hours'] = ts
    cols_ordered = ['time_in_hours'] + cols
    #
    df_nt = df_nt[cols_ordered]

    return (nt, df_nt)


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

    df_conc = pd.DataFrame()

    for i in index_list:
        conv_fact = df_vmu.loc[i, 'Mass_to_Conc_Conv_Factor']
        units = df_vmu.loc[i, 'concentrationOutputUnits']
        # col_name=i+'_'+units
        col_name = i
        col_val = np.array(df_nt[i]) * conv_fact
        df_conc[col_name] = col_val
        df_conc[col_name + '_units'] = units

    return (df_conc)


if __name__ == '__main__':
    from trim_db.utils.users_roles import implement_users_roles
    try:
        implement_users_roles()
    except Exception as e:
        print(f'-- Unable to create Users/Roles.\n{e}')

    SCENARIO_NAME = 'Foundries_SS'
    scn = ScenarioService.get(name=SCENARIO_NAME)

    # get transition matrix and source matrix
    (tm, df_tm, sm, df_sm, df_vmu) = make_transfer_matrix(scn)

    # get result
    (nt, df_nt) = ode_sim(tm, df_tm, sm, df_sm, scn)

    # make concentration output
    df_conc = compute_concentration(df_nt, df_vmu)

    # Output components as csv
    df_tm.to_csv("Transfer_Matrix_test.csv")
    df_sm.to_csv("Source_Matrix_test.csv")
    df_nt.to_csv("Result_Matrix_test.csv")
    df_conc.to_csv("Concentration_Result_Matrix_test.csv")

    print(tm)
