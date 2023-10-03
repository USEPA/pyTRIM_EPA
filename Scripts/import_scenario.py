import argparse
import json
import os
import time
from trim_db.porting import *
from trim_db.services import *

DEFAULT_IMPORT_RULES = './Scripts/import_config/default_rules.json'


def import_scenario(config):
    scenario_name = config.get('scenario_name')
    if not scenario_name:
        raise AssertionError('Must specify a scenario name!')

    scenario = ScenarioService.get(name=scenario_name)
    if scenario:
        print(f'Scenario "{scenario_name}" already exists!')
        return

    trim_files = config.get('directory')
    if not trim_files:
        raise AssertionError('Must specify a directory!')

    import_rules = config.get('import_rules') or DEFAULT_IMPORT_RULES

    print('\n==========================\n')

    print(f'Loading "{scenario_name}" ...')
    print('')
    start = time.time()
    load_data(trim_files, scenario_name, import_rules)
    end = time.time()
    print('Time to load data = ', round((end - start), 2), ' seconds')

    scenario = ScenarioService.get(name=scenario_name)
    print(scenario)

    print('\n==========================\n')


def load_data(trim_file_root, scenario_name, import_rules):
    if os.path.isfile(import_rules):
        with open(import_rules, mode='r', encoding='utf-8') as f:
            import_rules = json.load(f)

    master_library = [
        os.path.join(trim_file_root, f) for f in os.listdir(trim_file_root)
        if 'Master_Library' in f and f.endswith('_PropertyExporter.txt')
    ]
    if not master_library:
        return

    parameter_library = {}
    for f in master_library:
        parameter_library.update(read_master_library(f, import_rules=import_rules))
        break  # Should only be one??

    for_chemicals = import_rules.get('chemicals', [])

    def chemical_of_interest(chem):
        for c in for_chemicals:
            if chem.isa(c):
                return True
        return False

    parse_chemicals(parameter_library['Chemical'])

    chems = [
        c for c in ChemicalService.get_all()
        if chemical_of_interest(c)
    ]
    parse_scenario(
        trim_file_root, scenario_name,
        parameter_library=parameter_library, chemicals=chems
    )

    parse_transport_processes(
        parameter_library['Algorithm'],
        restrict_to=import_rules.get('transport_processes')
    )

    default_entries = import_rules.get('default_entries', {})

    if default_entries:
        print('Loading additional default parameters ...')

        from trim_db.schema import Compartment

    for param in default_entries.get('compartment_default_params', []):
        if param[3] is None:
            Compartment.parameters.add(param[0], value=param[1], unit=param[2])
        else:
            par_domain = ParameterService.domains.get(name=param[3])
            Compartment.parameters.add(param[0], value=param[1], unit=param[2], domain=par_domain)

    non_emitting_media = import_rules.get('media', {}).get(
        'restrict_emissions', []
    )
    non_absorbing_media = import_rules.get('media', {}).get(
        'restrict_absorption', []
    )

    for m in CompartmentService.media.get_all():
        for x in non_absorbing_media:
            if m.isa(x):
                m.can_absorb = False
        for x in non_emitting_media:
            if m.isa(x):
                m.can_emit = False
    CompartmentService.commit()

    # Load met, litter fall and allow exchange files and update params
    for file in default_entries.get('external_data_files', {}):
        default_entries["external_data_files"][file] = os.path.join(
            trim_file_root, default_entries["external_data_files"][file]
        )
    ext_dict = read_external_data(
        default_entries.get('external_data_files', {}), scenario_name
    )

    # print(ext_dict)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config')
    parser.add_argument('--scenario', default=None)
    parser.add_argument('--directory', default=None)
    parser.add_argument('--import-rules', default=DEFAULT_IMPORT_RULES)
    args = parser.parse_args()

    from trim_db.local import *  # Loads user/role tables

    config = {}
    if args.config:
        if os.path.isfile(args.config):
            with open(args.config, mode='r', encoding='utf-8') as f:
                config = json.load(f)
    else:
        config = {
            "scenario_name": args.scenario,
            "directory": args.directory,
            "import_rules": args.import_rules
        }

    import_scenario(config)
