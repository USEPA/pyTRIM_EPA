import json
import os
import time
from trim_db.porting import *
from trim_db.schema import *
from trim_db.services import *
from trim_db.schema.parameters.equations import find_arguments

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

FORMULA_ARG_DOMAINS = {
    'environment': 1,
    'self': 2,
    'compartment': 3
}

replacements = {
    'Advection_Sink': 'Soil_Advection_Sink',
    'Sediment_Burial_Sink': 'Burial_Sink'
}

chem_specific_fix_replacements = {
    "self.": "compartment.",
    "chemical.": "self.",
    "self.self.": "self.",
    " self.VolumeFraction_Solid ": " self.VolumeFraction_Solid(compartment) ",
    " self.VolumeFraction_Solid)": " self.VolumeFraction_Solid(compartment))",
    "compartment.self.VolumeFraction_Solid": "self.VolumeFraction_Solid(compartment)",
    "self.UseInputCharacteristicDepth_0_MeansNo_ElseYes": "self.UseInputCharacteristicDepth_0_MeansNo_ElseYes(compartment)"
}

AUX_MEDIA_INTRA_MAP = {
 'Abiotic|Soil|Surface_Soil': ['Abiotic|Soil|Surface_Soil|Tilled_Soil', 'Abiotic|Soil|Surface_Soil|Untilled_Soil']
}

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


def add_comp_chem_params(parlib):
    chems = [ChemicalService.get(name=ch) for ch, pars in parlib['Chemical'].items() if
             ch in DEFAULT_IMPORT_RULES['chemicals']]
    # Default scenario (scenario_id = 1) is where default chemical params need to be stored when they also depend on
    # compartment media type
    default_scenario = ScenarioService.get(name='Default')
    for ch in chems:
        comp_media_map = {do_replacements(clean_compartment_name(c), replacements): MEDIA_MAP.get(
            do_replacements(clean_compartment_name(c), replacements), "") for c, _ in param_lib['Compartment'].items()}

        # Get the input into a format that we can operate per prop and aggregate the compartments
        props = {}
        for cmp in comp_media_map:
            if comp_media_map[cmp] == '':
                continue
            for ic in parlib["Compartment"]:
                if do_replacements(clean_compartment_name(ic), replacements) != cmp:
                    continue
                for p in parlib["Compartment"][ic]:
                    if isinstance(parlib["Compartment"][ic][p].get('for_chemicals'), list):
                        for cc in parlib["Compartment"][ic][p]['for_chemicals']:
                            if cc['target'] != ch.name:
                                continue
                            if not props.get(p):
                                props.setdefault(p, [])
                            pv = {'compartment': do_replacements(clean_compartment_name(ic), replacements),
                                  'value': cc['value'], 'unit': cc['unit']}
                            props[p].append(pv)

        # Create a formula dict for each prop.
        frm = {}
        for prp in props:
            frmla = ""
            parts = {}
            for part in props[prp]:
                this_media = comp_media_map.get(part['compartment'])
                this_media_id = str(CompartmentService.media.get(category=this_media).id)
                if not parts.get(part["value"]):
                    parts[part["value"]] = [this_media_id]
                else:
                    parts[part["value"]].append(this_media_id)
                # we need to correctly mapped sub media types such as Tilled and Untille Soils.
                aux_meds = AUX_MEDIA_INTRA_MAP.get(this_media)
                if aux_meds:
                    if not isinstance(aux_meds, list):
                        aux_meds = [aux_meds]
                    for am in aux_meds:
                        aux_media_id = str(CompartmentService.media.get(category=am).id)
                        parts[part["value"]].append(aux_media_id)
            pc = 0
            for p, a in parts.items():
                pc += 1
                frmla += f'({p}) if compartment.media.id in {{{" , ".join(a)}}}'
                if pc == len(parts):
                    frmla += " else 0"
                else:
                    frmla += " else "
            for rk, rv in chem_specific_fix_replacements.items():
                frmla = frmla.replace(rk, rv)

            args = find_arguments(frmla)
            new_args = []
            for arg in args:
                if "." in arg:
                    base_arg = arg.split(".")[0]
                    if base_arg in new_args:
                        continue
                    else:
                        new_args.append(base_arg)
            frm.setdefault(prp, (frmla, new_args))

        # Push props to db (custom param, formula and formula_argument)s
        for pr in props:
            this_formula = frm[pr][0]
            this_arguments = frm[pr][1]
            this_unit = props[pr][0]['unit']
            this_req = f'(self.id == {ch.id})'
            this_scn_id = default_scenario.id
            this_definition = [d for d in ParameterService.definitions.get_all() if d.variable_name == pr][0]
            # Add new formula
            new_formula = FormulaService.create(equation=this_formula, no_commit=False)
            # Add new custom parameter on default scenario with new formula
            new_custom_par = ParameterService.create(definition=this_definition, scenario=default_scenario,
                                                     requirements=this_req, unit=this_unit, formula_id=new_formula.id,
                                                     no_commit=False)
            # Fix self as chemical for the new formula Arguments where applies
            self_arr = [fa for fa in new_formula._arguments.all() if fa.name == "self"]
            if len(self_arr) > 0:
                self_arr[0].domain_id = FORMULA_ARG_DOMAINS.get("self")
            print(f'completed created new custom param {pr} with formula {frm[pr][0]} and arguments {frm[pr][1]}')
        FormulaService.commit()
        ParameterService.commit()


def check_chem_params(parlib):
    chems = [ChemicalService.get(name=ch) for ch, pars in parlib['Chemical'].items() if ch in DEFAULT_IMPORT_RULES['chemicals']]
    default_scenario = ScenarioService.get(name='Default')
    for ch in chems:
        missing_pars = {}
        different_pars = {}

        for p, v in parlib['Chemical'][ch.name].items():
            if p in CHEMICAL_PROPS_DONT_TRANSFER:
                continue
            if p == 'category':
                ch.category = parlib['Chemical'][ch.name][p]['value']
                continue
            existing_par = ch.parameters.get(p)
            if not existing_par:
                missing_pars.setdefault(p, v)
            elif isinstance(existing_par, ParameterDefinition):
                # if parameter already exist create custom parameter with (self.id == chemical.id) requirement and for DEFAULT Scenario with id = 1.
                if isinstance(parlib['Chemical'][ch.name][p]['value'], str):  # it is a formula
                    print(f'{p} is custom and has formula {v}')
                    if existing_par.default_formula.equation == parlib['Chemical'][ch.name][p]['value'].replace("chemical.", "self."):
                        print(f"Formulas are the same, NO need to create new... Use the existing formula {existing_par.default_formula.equation}\n")
                    else:
                        print(f"These are NOT the same; lib-> {parlib['Chemical'][ch.name][p]['value'].replace('chemical.', 'self.')}, existing {existing_par.default_formula.equation}\n")
                        different_pars.setdefault(p, v)
                else:  # it is a number
                    print(f'{p} is custom and has numeric value {v}\n')
                    # Create new custom parameter with numeric value
                    if isinstance(parlib['Chemical'][ch.name][p]['value'], bool):
                        value = 1 if parlib['Chemical'][ch.name][p]['value'] else 0
                    else:
                        value = parlib['Chemical'][ch.name][p]['value']
        print(missing_pars)
        print(f'{200*"V"}\n')
        print(different_pars)


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
    # add_chem_params(param_lib)
    # check_chem_params(param_lib)
    add_comp_chem_params(param_lib)
    end = time.time()
    print('Time to load data = ', round((end - start), 2), ' seconds')
    print('\n==========================\n')
