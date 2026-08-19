import argparse
import os
import pandas as pd
from datetime import datetime
try:
    from trim_frontend.utils.logging import make_logger
except ModuleNotFoundError:
    from ..trim_frontend.utils.logging import make_logger


IDX_COLS = []


def compare(data1, data2, logger, splitter=', '):
    diffs = {}

    tabs1 = data1['data']
    tabs2 = data2['data']

    diffs = {}

    for tab, d1 in tabs1.items():
        if tab not in tabs2:
            logger.warning(f"\"{tab}\" not in {data2['filename']}")
            continue
        d2 = tabs2[tab]

        if d1.empty or d2.empty:
            continue

        logger.debug(f'Comparing "{tab}"')

        comp = d1.compare(d2)

        tab_diff = pd.DataFrame()
        if not len(comp.index):
            logger.debug(f'\tNo differences between scenarios for "{tab}"')
            # print(tab_diff)
            continue

        print(comp)

        checked = {}
        for (h1, h2) in comp.columns.values:
            if h1 in checked:
                continue
            checked[h1] = True

            if not h2:
                tab_diff[h1] = comp[(h1, h2)]
                continue

            c1 = comp[(h1, 'self')]
            c2 = comp[(h1, 'other')]

            if c1.equals(c2):
                tab_diff[h1] = c1
            else:
                tab_diff[f'{h1} (1)'] = c1
                tab_diff[f'{h1} (2)'] = c2

        # Clean up empty rows
        # tab_diff = tab_diff.set_index([
        #     x for x in IDX_COLS if x in tab_diff.columns.values
        # ]).applymap(
        #     lambda x: x or pd.NA
        # ).dropna(how='all').reset_index()

        print(tab_diff)

        other_cols = d1[[c for c in d1.columns.values if f'{c} (1)' not in tab_diff.columns.values]]

        tab_diff = tab_diff.join(other_cols)

        print(tab_diff)

        ordered_cols = []
        for c in d1.columns.values:
            if c not in tab_diff.columns.values:
                if f'{c} (1)' in tab_diff.columns.values:
                    ordered_cols.append(f'{c} (1)')
                if f'{c} (2)' in tab_diff.columns.values:
                    ordered_cols.append(f'{c} (2)')
            else:
                ordered_cols.append(c)

        tab_diff = tab_diff[ordered_cols]

        print(tab_diff)

        diffs[tab] = tab_diff

    timestamp = datetime.now().strftime('%Y-%m-%d')
    outdir = f'trim_scripts/output/Scenario-Comparison-{timestamp}'
    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    def get_scenario_from_fname(fname):
        return fname.split('_parameters_')[0]

    s1 = get_scenario_from_fname(data1['filename'])
    s2 = get_scenario_from_fname(data2['filename'])
    outname = f'{outdir}/{s1}_vs_{s2}.xlsx'
    with pd.ExcelWriter(outname, engine='xlsxwriter') as writer:
        for tab, df in diffs.items():
            logger.info(f'Writing "{tab}" diffs tab ...')
            df.to_excel(writer, sheet_name=tab, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p1', '--scenario-parameters-1', default=None
    )
    parser.add_argument(
        '-p2', '--scenario-parameters-2', default=None
    )
    parser.add_argument(
        '-v', '--verbose',
        action="store_true", default=False,
    )
    args = parser.parse_args()

    logger = make_logger(
        'scenario_comparer',
        level=('debug' if args.verbose else 'info')
    )

    rf1_name = os.path.basename(args.scenario_parameters_1)
    logger.info(f'Reading "{rf1_name}" ...')
    data1 = {
        'filename': rf1_name,
        'data': pd.read_excel(args.scenario_parameters_1, sheet_name=None)
    }

    rf2_name = os.path.basename(args.scenario_parameters_2)
    logger.info(f'Reading "{rf2_name}" ...')
    data2 = {
        'filename': rf2_name,
        'data': pd.read_excel(args.scenario_parameters_2, sheet_name=None)
    }

    compare(data1, data2, logger)
