import numpy as np
import pandas as pd


def make_report(data):
    df = pd.DataFrame.from_dict({k: data[k] for k in ['results', 'meta']})
    df = df.reset_index()

    # Create two datatables one for metadata and the other for results
    df_meta = df.dropna(subset=['meta']).drop('results', axis=1)
    df_meta = df_meta.reset_index()
    df_results = df.dropna(subset=['results']).drop('meta', axis=1)
    df_results = pd.concat([
        df_results.drop(['results'], axis=1),
        df_results['results'].apply(pd.Series)
    ], axis=1)

    # Melt columns into rows
    df_results = pd.concat([
        df_results.drop(['risk'], axis=1),
        df_results['risk'].apply(pd.Series)
    ], axis=1)
    df_results = pd.melt(
        df_results, id_vars=["index", "concentration"],
        var_name="Age Group", value_name="results"
    )

    # Break Concentration into Units and Magnitude
    def get_attr(attr, default='-', return_original_on_fail=False):
        def inner_get(obj):
            try:
                return getattr(obj, attr)
            except AttributeError:
                if return_original_on_fail:
                    return obj
                return default
        return inner_get

    df_results['Concentration Units'] = df_results.concentration.apply(
        get_attr('units')
    )
    df_results['concentration'] = df_results.concentration.apply(
        get_attr('magnitude', return_original_on_fail=True)
    )

    # Break Result Dictionaries into Pandas Columns
    df_results_series = df_results['results'].apply(pd.Series)
    df_results = pd.concat([
        df_results.drop(['results'], axis=1),
        df_results_series[
            ['adjusted_intake', 'hazard_quotient', 'intake', 'risk_factor']
        ]
    ], axis=1)
    df_results = df_results.fillna(value="-")
    df_results = df_results.rename(columns={"index": "Product"})

    # Divide Intake into Units and Magnitude
    df_results['Intake Units'] = df_results.intake.apply(
        get_attr('units')
    )
    df_results['intake'] = df_results.intake.apply(
        get_attr('magnitude', return_original_on_fail=True)
    )

    is_mutagenic = data['meta']['chemical']['mutagenic']
    if is_mutagenic:
        df_results['Adjusted Intake Units'] = df_results.adjusted_intake.apply(
            get_attr('units')
        )
        df_results['Adjusted Intake'] = df_results.adjusted_intake.apply(
            get_attr('magnitude')
        )

    # Remove Hazard Quotient Units (dimensionless)
    df_results['hazard_quotient'] = df_results.hazard_quotient.apply(
        get_attr('magnitude')
    )

    # Remove Risk Factor Units (dimensionless)
    df_results['risk_factor'] = df_results.risk_factor.apply(
        get_attr('magnitude')
    )

    # Add Chemical Name
    chemical = (df_meta.loc[df_meta['index'] == "chemical", "meta"]).values[0]
    df_results["Chemical"] = str(chemical['name'])

    # Add Scenario Name
    scenario = df_meta.loc[
        df_meta['index'] == "importSource", "meta"
    ].values[0].split("|")[0]
    df_results["scenario"] = scenario

    # Order Columns and Clean-up
    cols = [
        'Chemical', 'scenario', 'Age Group', 'Product',
        'concentration', 'Concentration Units',
        'intake', 'Intake Units'
    ]
    if is_mutagenic:
        cols.extend(['Adjusted Intake', 'Adjusted Intake Units'])
    cols.extend(['hazard_quotient', 'risk_factor'])
    df_results_ordered = df_results[cols]
    df_results_ordered = df_results_ordered.rename(columns={
        'scenario': 'TRIM Scenario',
        'concentration': "Concentration",
        'intake': "ADD/LADD",
        'Intake Units': "ADD/LADD Units",
        'Adjusted Intake': "Adjusted ADD/LADD",
        'Adjusted Intake Units': "Adjusted ADD/LADD Units",
        "hazard_quotient": "HQ",
        'risk_factor': "Risk"
    })
    df_results_ordered["Product"] = (
        df_results_ordered['Product'].str.replace("_", " ")
    )
    df_results_ordered["Product"] = df_results_ordered['Product'].str.title()
    df_results_ordered["Product"] = np.where(
        df_results_ordered['Product'] == 'Root',
        'Root Vegetable',
        df_results_ordered['Product']
    )

    def simplify_unit(unit, time_last=True):
        simple = str(unit)
        simple = simple.replace('gram', 'g')
        simple = simple.replace('milli', 'm')
        simple = simple.replace('kilo', 'k')
        simple = simple.replace('liter', 'L')
        simple = simple.replace(' ', '')
        if time_last:
            if '/day' in simple:
                simple = simple.replace('/day', '')
                simple += '/day'
        return simple

    df = df_results_ordered
    # Edit unit names
    for i, r in df.iterrows():
        for col in df.columns.values:
            if ('Unit' not in col):
                continue

            val = str(r[col] or '')
            if not val or val == '-':
                continue
            r[col] = simplify_unit(val)

            if 'Concentration' not in col:
                continue
            if r['Product'] == 'Soil':
                r[col] = r[col] + ' dry weight'
            elif r['Product'] not in ['Water']:
                r[col] = r[col] + ' wet weight'

    df = df.drop(columns=['TRIM Scenario'])  # No need to include this

    metadata = {
        'Exposure Profile': data['meta']['exposureProfile']['name'],
        'Timestamp': data['meta']['timestamp'],
        'Fish Calculation': data['meta']['fishPathway'],
        'Includes AERMOD Data?': data['meta']['usesAermod']
    }

    df_meta = pd.DataFrame({
        '': list(metadata.keys()),
        'Value': list(metadata.values())
    })
    print(df_meta)

    return [df, df_meta]
