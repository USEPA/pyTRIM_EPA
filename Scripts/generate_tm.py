import argparse
import os
import time
from trim_core.algorithms.transition_matrix import make_transition_matrix
from trim_db.services import ScenarioService


def generate_tm(scenario_name):
    scenario = ScenarioService.get(name=scenario_name)

    print('\n==========================\n')

    print('creating tm ...')
    start = time.time()
    df_tm, df_sm = make_transition_matrix(scenario)
    end = time.time()
    print('time to create tm = ', round((end - start), 2), ' seconds')

    safe_save_output(df_tm, df_sm)

    print('\n==========================\n')


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
    parser.add_argument('--scenario', default=None)
    args = parser.parse_args()

    from trim_db.local import *  # Loads user/role tables

    generate_tm(args.scenario)
