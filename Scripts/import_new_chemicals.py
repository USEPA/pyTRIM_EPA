import json
import os
import time
from trim_db.porting import *
from trim_db.schema import *
from trim_db.services import *

DEFAULT_IMPORT_RULES = \
    {
    "chemicals": [
        "Benzo(A)Pyrene"
    ],
    "media": {
        "restrict_emissions": [],
        "restrict_absorption": []
    },
    "default_entries": {
        "external_data_files": {}
    },
    "transport_processes": [],
    "_notes": {}
}

CHEMICAL_PROPS_DONT_TRANSFER = [
    'CAS', 'enabled'
]


def parse_chemicals(chemical_parameters):

    for name, params in chemical_parameters.items():
        cas = params['CAS']['value']

        chem = ChemicalService.get_or_create(
            cas_number=cas, no_commit=True
        )
        chem.name = name
        ChemicalService.commit()

        prop_entity = chem  # Attach properties to this chemical

        for prop, prop_data in params.items():
            if prop in CHEMICAL_PROPS_DONT_TRANSFER:
                continue

            if prop == 'category':
                chem.category = prop_data['value']
                continue

            val = prop_data.get('value')
            if isinstance(val, str):
                formula = val
                val = None
            else:
                formula = prop_data.get('formula')
            if formula:
                formula = formula.replace('chemical.', 'self.')
            prop_data.update({
                'value': val,
                'formula': formula
            })
            prop_entity.parameters.add(prop, **prop_data)

    ChemicalService.commit()


def add_chem_params(parlib):
    chems = [ChemicalService.get(name=ch) for ch, pars in parlib['Chemical'].items() if ch in DEFAULT_IMPORT_RULES['chemicals']]
    default_scenario = ScenarioService.get(name='Default')
    for ch in chems:
        missing_pars = {}
        for p, v in parlib['Chemical'][ch.name].items():
            if p in CHEMICAL_PROPS_DONT_TRANSFER:
                continue
            if p == 'category':
                ch.category = parlib['Chemical'][ch.name][p]['value']
                continue
            existing_par = ch.parameters.get(p)
            if not existing_par:
                missing_pars.setdefault(p, v)
                # Create new parameter
                # if new parameter value is a formula set it as default formula
                # if new parameter value is numeric create custom parameter with (self.id == chemical.id) requirement.
                # BUT WAIT!! If it is a new parameter that means it is not in the form fields in the UI.
                # However, since it is a chemical property it does not depend on scenario or other environmental
                # entities. Therefore, it will not need to be changed for different cases. SO even though it is
                # technically a constant or a default value at this point, we may be changing it later, so it is better
                # to keep it as custom parameter. Note that nearly all chemical parameters (parameters within chemical
                # domain) are set up this way and all have custom parameters instead of default values.


                # npd = ParameterDefinition(variable_name=p, full_name=p, domain_id=2,
                #                                   default_unit=parlib['Chemical'][ch.name][p]['unit'])
                # new_par_def = ParameterService.create(npd)
                # ParameterService.commit()
                # print(f"{'!' * 100}\n NEW PARAMETER CREATED FOR {p} {'!' * 100}\n")
                #
                # if isinstance(parlib['Chemical'][ch.name][p]['value'], str):  # it is a formula
                #     new_formula = parlib['Chemical'][ch.name][p]['value'].replace("chemical.", "self.")
                #     # TODO Crate new formula and create custom parameter with that formula
                #     # obj_formula = FormulaService.create(equation=new_formula)
                #     # Create new formula arguments.
                #     # Create custom parameter
                #     # ParameterService.create()
                # else:
                #     # Create custom param using default formula
                #     if isinstance(parlib['Chemical'][ch.name][p]['value'], bool):
                #         value = 1 if parlib['Chemical'][ch.name][p]['value'] else 0
                #     else:
                #         value = parlib['Chemical'][ch.name][p]['value']
                #     ParameterService.create(definition=new_par_def, scenario=default_scenario,
                #                             requirements=f"(self.id == {ch.id})", value=value,
                #                             unit=new_par_def.default_unit)


            elif isinstance(existing_par, ParameterDefinition):
                # if parameter already exist create custom parameter with (self.id == chemical.id) requirement and for DEFAULT Scenario with id = 1.
                if isinstance(parlib['Chemical'][ch.name][p]['value'], str):  # it is a formula
                    print(f'{p} is custom and has formula {v}')
                    if existing_par.default_formula.equation == parlib['Chemical'][ch.name][p]['value'].replace("chemical.", "self."):
                        print(f"Formulas are the same, NO need to create new... Using the existing formula {existing_par.default_formula.equation}\n")
                        # Create custom param using default formula
                        ParameterService.create(definition=existing_par, scenario=default_scenario,
                                                requirements=f"(self.id == {ch.id})",
                                                unit=existing_par.default_unit, formula=existing_par.default_formula)
                    else:
                        print(f"These are not the same; lib-> {parlib['Chemical'][ch.name][p]['value'].replace('chemical.', 'self.')}, existing {existing_par.default_formula.equation}\n")
                        # Create new formula, then add custom parameter with that formula id
                        new_formula = parlib['Chemical'][ch.name][p]['value'].replace("chemical.", "self.")
                        # obj_formula = FormulaService.create(equation=new_formula)
                        # Create new formula arguments.
                else:  # it is a number
                    print(f'{p} is custom and has numeric value {v}\n')
                    # Create new custom parameter with numeric value
                    if isinstance(parlib['Chemical'][ch.name][p]['value'], bool):
                        value = 1 if parlib['Chemical'][ch.name][p]['value'] else 0
                    else:
                        value = parlib['Chemical'][ch.name][p]['value']
                    ParameterService.create(definition=existing_par, scenario=default_scenario,
                                            requirements=f"(self.id == {ch.id})", value=value,
                                            unit=existing_par.default_unit)
        print(missing_pars)
    ParameterService.commit()

def load_data(trim_file_root, import_rules):

    if not isinstance(import_rules, dict):
        import_rules = {}

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

    # parse_chemicals(parameter_library['Chemical'])
    return parameter_library


if __name__ == '__main__':
    from trim_db.utils.users_roles import implement_users_roles
    try:
        import time
        implement_users_roles()
        time.sleep(5)
    except Exception as e:
        print(f'-- Unable to create Users/Roles.\n{e}')

    try:
        ScenarioService.get(id=2)
    except Exception as e:
        print(e)
        raise

    directory = "./trim_core/backend/Legacy_Input_Files"
    trim_files = directory
    if not trim_files:
        raise AssertionError('Must specify a directory!')

    import_rules = DEFAULT_IMPORT_RULES

    print('\n==========================\n')

    print(f'Loading ...')
    print('')
    start = time.time()
    param_lib = load_data(trim_files, import_rules)
    add_chem_params(param_lib)
    end = time.time()
    print('Time to load data = ', round((end - start), 2), ' seconds')
    print('\n==========================\n')
