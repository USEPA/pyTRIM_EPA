# import termios
import time
import types

from trim_db.porting import *
from trim_db.schema import *
from trim_db.services import *


SCENARIO_NAME = 'Foundries_SS'
CHEMICAL_CATEGORY = 'Mercury'


def make_transfer_matrix(scenario):
    import pandas as pd
    import numpy as np

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
            dr = sender.deposition_rate(chemical=chem)
            source_matrix[tm_x] += dr
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
                            print(f"{20*'*'} EVAL PROBLEM {20*'*'} {sender.name} -> {receiver.name}: {transport_proc.name}")
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
                                if transport_proc.algorithm_id in [2501, 2576]:
                                    print("2507")
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
    return df_tm


if __name__ == '__main__':
    from trim_db.local import *  # Loads user/role tables

    SCENARIO_NAME = 'Foundries_SS'
    scn = ScenarioService.get(name=SCENARIO_NAME)

    tm = make_transfer_matrix(scn)
    tm.to_csv("Transfer_Matrix_test.csv")
    print(tm)

