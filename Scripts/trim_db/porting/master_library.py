import os
import pandas as pd
import re
from ..schema.chemicals.models import *


def parse_master_library(file_root, scenario, master_filepath, props_filepath):
    add_constants(scenario)

    params = parse_properties(file_root, props_filepath)

    for s_name, s_params in params.get('Scenario', {}).items():
        for opts in s_params:
            scenario.parameters.add(**opts)

    df_lib = pd.read_csv(
        master_filepath, sep=';', encoding='windows-1252', nrows=0,
        low_memory=False
    )
    df_lib = pd.read_csv(
        master_filepath, sep=';', encoding='windows-1252', skiprows=[0],
        names=df_lib.columns.values,
        low_memory=False
    )

    parse_chemicals(
        scenario, df_lib[df_lib.ObjectType == 'Chemical']
    )

    vol_params = params.get('VolumeElement', {})
    comp_params = params.get('Compartment', {})
    for vol in scenario.volume_elements:

        for comp in vol.compartments:
            if comp.full_name not in comp_params:
                continue
            for opts in comp_params[comp.full_name]:
                comp.parameters(scenario).add(**opts)

        if vol.name not in vol_params:
            continue
        for opts in vol_params[vol.name]:
            vol.parameters(scenario).add(**opts)


def add_constants(scenario):
    constants = [
        ('g_per_kg', 1000),
        ('IdealGasConstant', 8.314),  # (Pa-m3/mol-K)
        ('kg_per_g', 1e-3),
        ('kg_per_m3_Water', 1000),
        ('kg_per_ug', 1e6),
        ('L_per_m3', 1000),
        ('m3_per_kg_Water', 1e-3),
        ('m3_per_L', 1e-3),
        ('m3_per_um3', 1e-18),
        ('pi', 3.14159265358979323846),
        ('ug_per_kg', 1e6),
        ('um3_per_m3', 1e18),
        ('vonKarmensConstant', 0.74),
        ('waterMeltingPoint', 273.15)
    ]
    for (name, val) in constants:
        scenario.parameters.add(name=name, value=val)


def safe_name(name):
    if not isinstance(name, str):
        return name
    try:
        name = float(name)
        return name
    except Exception:
        pass

    name = re.sub('[^0-9a-zA-Z]+', '_', name)
    # name = re.sub('_+', '_', name)
    name = name.replace('Halflife', 'HalfLife')
    return name


def clean_prop(prop):
    if prop is None:
        return prop

    val = str(prop).strip()
    try:
        val = float(val)
        return val
    except ValueError:
        val = str(prop).strip()  # Reset

    if val.lower() == 'true':
        return True
    if val.lower() == 'false':
        return False

    val = val.replace('Chemical.', 'self.')
    val = val.replace('containingScenario.', 'environment.')
    val = val.replace('Constants.', 'environment.')

    replacements = {
        'Constants': 'environment',
        'containingScenario': 'environment',

        'chemical.': 'self.',
        'Chemical.': 'self.',
        'compartment.': 'self.',
        'Compartment.': 'self.',

        'ln': 'log',
        '<Unset>': '"<Unset>"',
        'Halflife': 'HalfLife',
        'D_Purewater': 'D_purewater',
        'FractionMass_Vapor': 'FractionMass_vapor',
        'VolumeFraction_algae': 'VolumeFraction_Algae',
        'Chemical_Z_algae': 'Chemical_Z_Algae',
        'self.Volume *': 'self.volume_element.volume *',
        'self.Volume*': 'self.volume_element.volume*',
        'self.Height': 'self.volume_element.height'
    }
    # Replace longest keys first to avoid substring issues
    keys = sorted(list(replacements), key=lambda x: len(x))
    for k in reversed(keys):
        v = replacements[k]
        val = val.replace(str(k), str(v))

    return val


def parse_properties(
    file_root, props_filepath,
    prop_types=['Scenario', 'VolumeElement', 'Compartment']
):
    if not isinstance(prop_types, list):
        prop_types = [prop_types]

    with open(props_filepath, 'r') as f:
        lines = f.readlines()

    copying = {}
    parsed_lines = {x: {} for x in prop_types}
    current_els = []
    prop_name = None
    got_prop = False
    for line in lines:
        line = line.split('//')[0].strip()  # remove comment
        if not line:
            continue  # Nothing to see here

        line = line.split(':', 1)
        key = line[0].strip()
        val = line[1].strip()

        for prop_type in prop_types:
            if prop_type == key:
                if got_prop or not copying.get(prop_type):
                    current_els = []
                    got_prop = False
                copying = {prop_type: True}
                current_els.append(parsed_lines[prop_type].setdefault(val, {}))
            elif copying.get(prop_type):
                if key == 'Property':
                    prop_name = val
                elif key == 'Value' and prop_name:
                    for el in current_els:
                        el[safe_name(prop_name)] = clean_prop(val)
                    prop_name = None
                    got_prop = True

    allow_props = {
        'Scenario': [
            'AirTemperature_K'
        ]
    }

    prop_files = {}

    parsed = {}

    for prop_type in prop_types:
        allowed = allow_props.get(prop_type, [])
        for name, props in parsed_lines[prop_type].items():
            for prop, val in props.items():
                if allowed and prop not in allowed:
                    continue

                if isinstance(val, str) and 'C:\\' in val:
                    val = val.split('\\')[-1].split(',')
                    fname = val[0].strip()
                    colname = val[1].strip()
                    if fname not in prop_files:
                        prop_files[fname] = pd.read_csv(
                            os.path.join(file_root, fname),
                            low_memory=False
                        )
                    df = prop_files[fname]
                    try:
                        val = pd.to_numeric(
                            df[colname], errors='coerce'
                        ).mean()
                    except Exception:
                        val = 0

                eq = None
                try:
                    val = pd.to_numeric(val)
                except Exception:
                    eq = val
                    val = None

                parsed.setdefault(prop_type, {}).setdefault(name, []).append({
                    'name': prop,
                    'value': val,
                    'equation': eq
                })
    return parsed


def parse_chemicals(scenario, chem_df):
    chems = []

    for name, data in chem_df.groupby("ObjectName"):
        name = 'Chem_' + safe_name(name)
        chem = Chemical(name=name)

        scenario_params = chem.parameters(scenario)

        for param_data in data.itertuples():
            param = param_data.PropertyName
            val = clean_prop(param_data.PropertyValue)

            if param == 'CAS':
                chem.cas_number = val
            elif param == 'category':
                chem.category = val
            else:
                try:
                    float(val)
                    scenario_params.add(name=param, value=val)
                except ValueError:
                    scenario_params.add(name=param, equation=val)

        scenario.chemicals.append(chem)
        chems.append(chem)

    return chems
