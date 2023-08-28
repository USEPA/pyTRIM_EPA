import os
import pandas as pd
from ..services import *
from ..utils import iter_by_longest_key
from .environment import *
from .utils import *


__all__ = ['parse_scenario', 'parse_prop_types']


def parse_scenario(
    root_folder, name, parameter_library={}, chemicals=[], creator_id=2
):
    print(f'Parsing scenario "{name}" at "{root_folder}" ...')
    name = name.rstrip()
    files = [
        os.path.join(root_folder, f) for f in os.listdir(root_folder)
        if f.startswith(name)
    ]

    s = ScenarioService.get_or_create(
        name=name,
        creator_id=creator_id,
        no_commit=True
    )
    for chem in chemicals:
        s.chemicals.append(chem)
    ScenarioService.commit()

    vol_file = [f for f in files if f.endswith('Volume Elements.txt')]
    ps_vol_file = [
        f for f in files if f.endswith('pseudo_volume_elements.txt')
    ]
    for vf in [vol_file, ps_vol_file]:
        if not vf:
            continue
        parse_volume_elements(s, vf[0])

    comp_file = [f for f in files if f.endswith('Compartments.txt')]
    if comp_file:
        parse_compartments(s, comp_file[0])

    def merge_props_with_master(master, props):
        props = {
            k: {
                nm: {
                    x['name']: {
                        'value': (
                            x['equation'] if x['value'] is None
                            else x['value']
                        ),
                        'unit': x['unit']
                    }
                    for x in params
                }
                for nm, params in v.items()
            }
            for k, v in props.items()
        }
        for k, v in master.items():
            props.setdefault(k, {}).update(v)
        return props

    lib = parameter_library
    for f in files:
        if f.lower().endswith('pseudo_library_objects.txt'):
            props = parse_props(f)
            lib = merge_props_with_master(
                lib, props
            )
        elif f.lower().endswith('pseudo_link_properties.txt'):
            props = parse_props(f, oneline_keyvals=True, rules={
                'NewLink': {
                    'name': 'Link',
                    'ignore': [
                        'Algorithm'
                    ]
                }
            })
            lib = merge_props_with_master(
                lib, props
            )
    parameter_library.update(lib)
    # with open('temp.json', 'w') as f:
    #     import json
    #     json.dump(parameter_library, f)

    if parameter_library:
        parse_compartment_props(s, parameter_library.get('Compartment', {}))

    prop_file = [f for f in files if f.endswith('Properties.txt')]
    if prop_file:
        parsed = parse_props(prop_file[0])

        add_scenario_properties(
            s, parsed, parameter_library.get('Link', {})
        )

    fr_prop_file = [f for f in files if f.endswith('FlushRate.txt')]
    if fr_prop_file:
        fr_parsed = parse_props(fr_prop_file[0])

        add_scenario_properties(
            s, fr_parsed, parameter_library.get('Link', {})
        )

    prop_types = [f for f in files if f.endswith('PropertyType_Exporter.txt')]
    if prop_types:
        parse_prop_types(prop_types[0])


TRANSFER_RULES = {
    'Scenario': {
        'ignore': [
            'outputDir',
            'evaluateHTMLPropertiesAtTime',
            'simulationBeginDateTime',
            'simulationEndDateTime',
            'simulationTimeStep',
            'simulationStepsPerOutputStep',
            # 'simulateSteadyState',
            'averageResultsFiles',
            'averagingInterval',
            'enableBoundaryContributions',
            'exportAllResultsToDB',
            'exportAvgResultsToDB',
            'exportIngestionInputs',
            'exportDeposition',
            'exportBiotaIntakeRates',
            'exportOutdoorEnvironmentBeforeRun',
            'exportPropertiesBeforeRun',
            'exportRiskECOInputs',
            'FractionInitialConcentrations',
            'exportMass',
            'exportConcentration',
            'exportHTML',
            'exportTimeStepsDown',
            'significantDigits',
            'image',
            # 'isDay_SteadyState_forAir',
            # 'isDay_SteadyState_forOther',
            # 'isDay_Dynamic'
        ]
    },
    'VolumeElement': {
        'ignore': [
            'top',
            'bottom',
            'image'
        ]
    },
    'Compartment': {
        'ignore': [
            'Enabled',
            'acceptableAbiotic',
            'Area',
            'category',
            'concentrationOutputUnits',
            'Volume',
            'image'
        ],
        'unit_map': {
            'SuspendedSedimentConcentration': 'kg/m^3'
        }
    },
    'Link': {
        'ignore': [
            'Enabled'
        ]
    },
    'Algorithm': {
    },
    'PointSource': {
        'name': 'Source',
        'ignore': [
            'Enabled'
        ]
    }
}


def parse_props(props_file, oneline_keyvals=False, rules=TRANSFER_RULES):
    print(f'Parsing properties from "{os.path.basename(props_file)}" ...')

    prop_types = list(rules)

    with open(props_file, 'r') as f:
        lines = f.readlines()

    # Parse the lines in the properties file
    # into an easier format to manipulate
    copying = {}
    parsed_lines = {x: {} for x in prop_types}
    current_els = []
    prop_name = None
    got_prop = False
    multi_line = ""
    for i, line in enumerate(lines):
        line = line.split('//')[0].strip()  # remove comment
        if not line:
            continue  # Nothing to see here

        if line.count("(") > line.count(")") or line.count("[") > line.count("]") or (not multi_line == ""):
            multi_line += line.replace("\n", "")
            if multi_line.count("(") > multi_line.count(")") or multi_line.count("[") > multi_line.count("]"):
                continue
            else:
                line = multi_line
        multi_line = ""

        line = line.split(':', 1)
        if not len(line) > 1:
            if oneline_keyvals:
                line.append('')
            else:
                continue

        key = line[0].strip()
        val = line[1].strip()

        for prop_type in prop_types:
            if prop_type == key:
                if got_prop or not copying.get(prop_type):
                    current_els = []
                    got_prop = False
                copying = {prop_type: True}
                new_name = val
                if not new_name and oneline_keyvals:
                    new_name = str(i)
                current_els.append(
                    parsed_lines[prop_type].setdefault(new_name, {})
                )
            elif copying.get(prop_type):
                if key == 'Property':
                    prop_name = val
                elif key == 'Value' and prop_name:
                    for el in current_els:
                        el[safe_name(prop_name)] = clean_prop(val)
                    prop_name = None
                    got_prop = True
                elif oneline_keyvals:
                    for el in current_els:
                        el[safe_name(key)] = clean_prop(val)
                    prop_name = None
                    got_prop = True

    # Parse the properties into a dict format,
    # collating values from other prop files
    props_root = os.path.dirname(props_file)
    prop_files = {}
    parsed = {}
    for prop_type in prop_types:
        disallowed = rules.get(prop_type, {}).get('ignore', {})
        for name, props in parsed_lines[prop_type].items():
            for prop, val in props.items():
                if prop in disallowed:
                    continue

                if isinstance(val, str) and 'C:\\' in val:
                    val = val.split('\\')[-1].split(',')
                    if len(val) > 1:
                        fname = val[0].strip()
                        colname = val[1].strip()
                        if fname not in prop_files:
                            prop_files[fname] = pd.read_csv(
                                os.path.join(props_root, fname),
                                low_memory=False
                            )
                        df = prop_files[fname]
                        try:
                            val = pd.to_numeric(
                                df[colname], errors='coerce'
                            ).mean()
                        except Exception:
                            val = 0
                    else:
                        continue

                eq = None
                try:
                    val = pd.to_numeric(val)
                except Exception:
                    eq = val
                    val = None

                if eq is not None:
                    eq = clean_equation(eq, prop_type.lower())

                unit = None
                for k, v in iter_by_longest_key(UNIT_SUFFIXES):
                    if prop.endswith(k):
                        prop = prop.rstrip(k)
                        unit = v
                        break

                prop_type_name = rules.get(prop_type, {}).get(
                    'name', prop_type
                )

                parsed.setdefault(prop_type_name, {}).setdefault(
                    name, []
                ).append({
                    'name': prop,
                    'value': val,
                    'equation': eq,
                    'unit': unit
                })

    return parsed


def add_scenario_properties(scenario, parsed_props, library_link_properties):
    # Add non-Link properties to DB
    for prop_type, prop_data in parsed_props.items():
        if prop_type == 'Link':
            continue

        for entity_name, entity_params in prop_data.items():
            obj = None

            if prop_type == 'Scenario':
                obj = scenario

            elif prop_type == 'VolumeElement':
                obj = scenario.get_volume_element(entity_name)

            elif prop_type == 'Compartment':
                obj = find_compartment(scenario, entity_name)

            if obj is None:
                print(scenario)
                print(prop_type)
                print(entity_name)

            for opts in entity_params:
                obj.parameters.add(
                    opts['name'], value=opts['value'],
                    formula=opts['equation'],
                    unit=opts['unit']
                )

    # Add Link properties to DB
    link_props = {}
    for link_name, link_params in parsed_props['Link'].items():
        compartments = link_name.split(' to ', 1)
        if len(compartments) != 2:
            continue
        sender = find_compartment(scenario, clean_prop(compartments[0]))
        receiver = find_compartment(scenario, clean_prop(compartments[1]))

        if not sender or not receiver:
            print(f'{compartments}\nsender = {sender}\nreceiver = {receiver}')
            raise AssertionError

        if not sender.connects_to(receiver):
            CompartmentService.links.create(sender=sender, receiver=receiver)

        link_prop_data = link_props.setdefault(
            sender, {}
        ).setdefault(sender.media.name, {})
        for param_data in link_params:
            param = param_data.pop('name')
            val = param_data.get('value')
            if val is None:
                val = param_data.get('equation')
            unit = param_data.get('unit')
            link_prop_data.setdefault(
                param, param_data
            ).setdefault('for_compartments', []).append({
                'target': receiver.standard_name,
                'value': val,
                'unit': unit
            })

    for sender, link_prop_data in link_props.items():
        parse_compartment_props(
            scenario, link_prop_data, compartment=sender,
            silent=True
        )

    for name, props in library_link_properties.items():
        try:
            sender = find_compartment(
                scenario, props['SendingCompartment']['value']
            )
            receiver = find_compartment(
                scenario, props['ReceivingCompartment']['value']
            )
        except Exception:
            print(props)
            raise

        if not sender or not receiver:
            print(f'{compartments}\nsender = {sender}\nreceiver = {receiver}')
            raise AssertionError

        if not sender.connects_to(receiver):
            CompartmentService.links.create(sender=sender, receiver=receiver)
        else:
            print(
                f'"{sender.standard_name}" already connects'
                f' to "{receiver.standard_name}"'
            )


def find_compartment(scenario, name):
    if ' in ' in name:
        name = name.split(' in ')
        name = ' in '.join([
            clean_compartment_name(name[0]),
            *name[1:]
        ])
    obj = scenario.get_compartment(name)
    if obj is None:
        if ' in ' in name:
            v_name = name.split(' in ')[-1]
            v = scenario.get_volume_element(v_name)
            if v is not None:
                obj = create_compartment(name.split(' in ')[0], v)
    return obj


def parse_compartment_props(
    s, compartment_parameters, compartment=None, silent=False
):
    if not compartment_parameters:
        return

    if not silent:
        print('Loading compartment-media properties from library data ...')

    from .config import MEDIA_MAP
    from .environment import clean_compartment_name
    from ..schema import Compartment, Chemical
    from functools import partial

    ignore = TRANSFER_RULES['Compartment']['ignore']
    unit_map = TRANSFER_RULES['Compartment']['unit_map']

    relative_params = {
        'chemicals': {},
        'compartments': {}
    }

    for_specific_compartment = (compartment is not None)

    for name, params in compartment_parameters.items():
        clean_name = clean_compartment_name(name)
        full_name = MEDIA_MAP.get(clean_name, clean_name)

        media = CompartmentService.media.get(name=full_name.split('|')[-1])
        if not media:
            if clean_name in MEDIA_MAP:
                media = CompartmentService.media.get_or_create(
                    category=full_name
                )
            else:
                continue

        requirements = f'self.media_id == {media.id}'
        domain_name = f'Compartment [{media.name}]'

        base_id = (
            compartment.id if for_specific_compartment else media.id
        )

        for prop, prop_data in params.items():
            if prop in ignore or not prop_data:
                continue

            if prop == 'concentrationOutputFactor':
                prop_data['unit'] = params.get(
                    'concentrationOutputUnits', {}
                ).get('value')

            val = prop_data['value']
            if isinstance(val, str):
                formula = val.replace('compartment.', 'self.')
                val = None
            else:
                formula = None

            had_rel_defs = False
            for rel_type in relative_params:
                relative_defs = prop_data.pop(f'for_{rel_type}', None)
                if not relative_defs:
                    continue
                had_rel_defs = True

                if rel_type == 'chemicals':
                    service_getter = ChemicalService.get
                elif rel_type == 'compartments':
                    service_getter = partial(find_compartment, s)

                default = 0

                for rel_def in relative_defs:
                    target = service_getter(name=rel_def['target'])
                    if not target:
                        continue

                    target_params = relative_params[rel_type].setdefault(
                        (
                            target.name if isinstance(target, Chemical)
                            else compartment.standard_name
                        ), {}
                    )
                    if isinstance(target, Chemical):
                        target_params.setdefault('CAS', {
                            'value': target.cas_number
                        })
                    else:
                        base_id = target.id
                    target_prop_data = target_params.setdefault(prop, {
                        'default': default
                    })

                    unit = rel_def.get('unit')
                    if unit is None and prop in unit_map:
                        unit = unit_map[prop]

                    val = rel_def.get('value')
                    if isinstance(val, str):
                        formula = val
                        val = None
                    else:
                        formula = None

                    if val:
                        target_prop_data.setdefault(
                            'values', {}
                        ).setdefault(val, []).append(base_id)
                    if formula:
                        target_prop_data.setdefault(
                            'formulas', {}
                        ).setdefault(formula, []).append(base_id)
                    if unit:
                        target_prop_data.setdefault('unit', unit)

            if not had_rel_defs:
                new_data = {
                    'requirements': requirements,
                    'domain_name': domain_name,
                    'value': val,
                    'formula': formula
                }
                if prop in unit_map:
                    new_data['unit'] = unit_map[prop]
                prop_data.update(new_data)
                if for_specific_compartment:
                    compartment.parameters.add(prop, **prop_data)
                else:
                    Compartment.parameters.add(prop, **prop_data)

        CompartmentService.commit()

    target_id_path = (
        'compartment.id' if for_specific_compartment
        else 'compartment.media.id'
    )

    for rel_type, rel_params in relative_params.items():
        for comp_name, rel_props in rel_params.items():
            for prop_name, prop_data in rel_props.items():
                if 'value' in prop_data:
                    continue
                vals = prop_data.pop('values', {})
                formulas = prop_data.pop('formulas', {})
                default = prop_data.pop('default', None)

                total_opts = len(vals) + len(formulas)

                if total_opts > 0:
                    formulas = [
                        f'(({k}) if {target_id_path} in {set(v)}'
                        for k, v in formulas.items() if v and k
                    ]
                    if vals:
                        vals = [
                            f'(({k}) if {target_id_path} in {set(v)}'
                            for k, v in vals.items() if v and k
                        ]
                        formulas.extend(vals)
                    formula = (
                        ' else '.join(formulas)
                        + f' else {default}'
                        + (')' * len(formulas))
                    ).strip() or None
                    if rel_type == 'compartments':
                        formula = formula.replace('compartment.', 'receiver.')
                    formula = formula.replace('self.', 'compartment.')
                else:
                    formula = None

                if rel_type == 'compartments':
                    prop_data.update({
                        'value': formula if formula is not None else default
                    })
                elif rel_type == 'chemicals':
                    prop_data.update({
                        'value': None if formula is not None else default,
                        'formula': formula
                    })

            if rel_type == 'compartments':
                sender = find_compartment(s, comp_name)
                parse_compartment_props(
                    s, {sender.media.name: rel_props}, compartment=sender,
                    silent=True
                )

        if rel_type == 'chemicals':
            from .chemicals import parse_chemicals
            parse_chemicals(rel_params, scenario=s, message=(
                'Loading compartment-chemical properties from library data ...'
            ) if not silent else '')


def parse_prop_types(fpath):
    prop_types = pd.read_csv(fpath, sep='\t', index_col=False)

    prop_types.columns = [
        ' '.join(c.split()).strip().lower().replace(' ', '_')
        for c in prop_types.columns.values
    ]

    # pd.set_option('display.max_columns', None)
    # print(prop_types)

    for row in prop_types.itertuples():
        name, _ = split_unit_suffix(row.property_type)

        name = clean_prop(name)

        param = ParameterService.definitions.get(variable_name=name)
        if param is None:
            continue

        changed = False

        default = row.default
        if not pd.isna(default) and param.default_value is None:
            if isinstance(default, str):
                if default.lower() == 'false':
                    default = 0
                elif default.lower() == 'true':
                    default = 1
                else:
                    default = None
            elif default is False:
                default = 0
            elif default is True:
                default = 1

            if default is not None:
                changed = True
                # print(default)
                param.default_value = default

        units = clean_unit(row.units)
        if units and param.default_unit is None:
            changed = True
            # print(units)
            param.default_unit = units
            if param.default_value is None:
                param.default_value = 0

        desc = row.description
        if desc and param.description is None:
            changed = True
            # print(desc)
            param.description = desc

        # if changed:
        #     print(param)

    ParameterService.commit()
