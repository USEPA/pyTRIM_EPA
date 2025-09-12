import argparse
import os
import time
from datetime import datetime
from trim_core.algorithms.full_model_run import make_transition_matrix
from trim_db.schema.scenarios.models import ScenarioLoadRunProc
from trim_db.services import ScenarioService


def generate_tm(scenario_name):
    scenario = ScenarioService.get(name=scenario_name)
    if scenario is None:
        print(f'No Scenario found with name "{scenario_name}"!')
        return

    try:
        new_proc = ScenarioLoadRunProc(
            scenario=scenario,
            load_status='load 100',
            run_status='run null null',
            run_datetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        scenario.proc_status.add(new_proc)
    except Exception as e:
        print(e)
    ScenarioService.commit()

    print('\n==========================\n')

    print('creating tm ...')
    start = time.time()
    try:
        (df_tm, df_sm, df_vmu, df_c0) = make_transition_matrix(scenario)
    except Exception as e:
        print('!>>', e)
    end = time.time()
    print('time to create tm = ', round((end - start), 2), ' seconds')

    # safe_save_output(df_tm, df_sm)

    print('\n==========================\n')

    try:
        try:
            ScenarioService.db.session.rollback()
        except Exception:
            pass
        scenario.proc_status.remove(new_proc)
        ScenarioService.commit()
    except Exception as e:
        print(e)


def safe_save_output(df_tm, df_sm):
    try:
        if not os.path.isdir('./.output'):
            os.makedirs('./.output')
        df_sm.to_csv('./.output/sm_new.csv')
        df_tm.to_csv('./.output/tm_new.csv')
    except Exception:
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--scenario')
    args = parser.parse_args()

    from trim_db.local import *  # Loads user/role tables

    generate_tm(args.scenario)
