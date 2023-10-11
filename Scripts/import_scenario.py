import argparse
import json
import os
from trim_core.porting import import_scenario

DEFAULT_IMPORT_RULES = './Scripts/import_config/default_rules.json'


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
        config.setdefault('scenario_name', args.scenario)
        config.setdefault('directory', args.directory)
        config.setdefault('import_rules', args.import_rules)
    else:
        config = {
            "scenario_name": args.scenario,
            "directory": args.directory,
            "import_rules": args.import_rules
        }

    import_scenario(config)
