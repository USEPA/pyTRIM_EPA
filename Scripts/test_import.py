import time
from trim_db.porting import *
from trim_db.schema import *
from trim_db.services import *

TRIM_FILES = (
    '/Users/55284/Library/CloudStorage/OneDrive-ICF/Desktop/RTR_TRIM-FaTE/TRIM_builder_new_mac/Scripts/'
    'trim_core/backend/Legacy_Input_Files'
)

SCENARIO_NAME = 'Foundries_SS'
CHEMICAL_CATEGORY = 'Mercury'


def load_data():
    parameter_library = read_master_library(
        f'{TRIM_FILES}/ICF_Master_Library_03212016_PropertyExporter.txt'
    )

    parse_chemicals(parameter_library['Chemical'])

    chems = [
        c for c in ChemicalService.get_all()
        if CHEMICAL_CATEGORY in (c.category or '')
    ]

    parse_scenario(
        TRIM_FILES, SCENARIO_NAME,
        parameter_library=parameter_library, chemicals=chems
    )

    parse_transport_processes(parameter_library['Algorithm'])

    for m in CompartmentService.media.get_all():
        if m.isa('Abiotic|Air') or m.isa('Sink'):
            m.can_emit = False
        elif m.isa('Source'):
            m.can_absorb = False
    CompartmentService.commit()


def print_scenario_info(scenario):
    print('Scenario.domains =', Scenario.domains)
    print('Scenario.parameters =', Scenario.parameters)

    print('\nscenario = ', scenario)

    print('\nscenario.domains =', scenario.domains)
    print('scenario.parameters =', scenario.parameters)

    print('\nscenario.chemicals =', scenario.chemicals)
    print('len(scenario.volume_elements) =', len(scenario.volume_elements))

    print(
        '\nscenario.parameters["IdealGasConstant"] =',
        scenario.parameters['IdealGasConstant']
    )
    print('\nscenario.IdealGasConstant =', scenario.IdealGasConstant)
    print('scenario.AirTemperature =', scenario.AirTemperature)

    # print(f'\ntransport_processes = {TransportProcessService.get_all()}')

    print('\n==========================\n')


def print_chemical_class_info():
    print('Chemical.domains =', Chemical.domains)
    print('Chemical.parameters =', Chemical.parameters)

    print(
        '\nChemical.parameters["D_pureair"] =',
        Chemical.parameters['D_pureair']
    )

    print('\n==========================\n')


def print_scenario_chemical_info(scenario):
    for chem in scenario.chemicals:
        print('chem =', chem)
        print('chem.current_scenario() =', chem.current_scenario())
        print('\nchem.domains =', chem.domains)
        print('chem.parameters =', chem.parameters)

        print('\nchem.parameters["D_pureair"] =', chem.parameters['D_pureair'])
        print('\nchem.D_pureair =', chem.D_pureair)
        print('chem.MeltingPoint =', chem.MeltingPoint)

        print(
            '\nchem.parameters["H_over_R_T"] =',
            chem.parameters['H_over_R_T']
        )
        print('chem.H_over_R_T =', chem.H_over_R_T)
        print('chem.K_oc =', chem.K_oc)

        print('\n==========================\n')


def print_scenario_volume_element_info(scenario):
    for ve in scenario.volume_elements:
        if 'SW_' not in ve.standard_name:
            continue

        print('\nve =', ve)
        print('ve.current_scenario() =', ve.current_scenario())
        print('ve.parameters =', ve.parameters)

        print('\n==========================\n')


def print_scenario_compartment_info(scenario):
    from itertools import combinations

    for (c1, c2) in combinations(scenario.compartments, 2):
        if not ('_E1' in c1.standard_name and '_E1' in c2.standard_name):
            continue

        print('\nc1 =', c1)
        print('c1.current_scenario() =', c1.current_scenario())
        print('c1.parameters =', c1.parameters)

        print('\nc2 =', c2)
        print('c2.current_scenario() =', c2.current_scenario())
        print('c2.parameters =', c2.parameters)

        print(
            '\nc1.volume_element.overlap_with(c2.volume_element) =',
            c1.volume_element.overlap_with(c2.volume_element)
        )
        print('c1.connects_to(c2) =', c1.connects_to(c2))

        print('\n==========================\n')


def make_transition_matrix(scenario):
    import pandas as pd
    import numpy as np

    chem_list = list(sorted(
        scenario.chemicals, key=lambda x: x.name
    ))
    comp_list = list(sorted(
        scenario.compartments, key=lambda x: x.standard_name
    ))

    if True:  # DEBUGGING
        comp_list = [
            x for x in comp_list if (
                'Lake' in x.standard_name
            )
        ]

    n_chem = len(chem_list)
    n_comp = len(comp_list)

    matrix_dimensions = n_chem * n_comp

    source_matrix = np.zeros(matrix_dimensions, dtype=float)
    transition_matrix = np.zeros(
        (matrix_dimensions, matrix_dimensions), dtype=float
    )

    index_names = ['' for _ in source_matrix]

    chem_indices = {
        c: i for i, c in enumerate(chem_list)
    }

    try:
        for chem_idx, chem in enumerate(chem_list):
            # try:
            #     kd = chem.Kd(scenario.get_compartment(
            #         'Surface_water in SW_LakeCadillac'
            #     ))
            # except Exception:
            #     kd = None

            print('\n' + '==' * 28)
            print(f'Chemical = {chem.name}')
            # print(f'Chemical = {chem.name}, Kd = {kd}')
            print('==' * 28)

            # check_alg_values(
            #     scenario, chem,
            #     (
            #         'Direct Transfer from PseudoSource to Surface water'
            #     ),
            #     'WetParticleSource in WetParticleSource_LakeCadillac',
            #     'Surface_water in SW_LakeCadillac'
            # )
            # continue

            for x, sender in enumerate(comp_list):
                tm_x = int(chem_idx * n_comp + x)

                index_names[tm_x] = chem.name + '_' + sender.standard_name

                try:
                    dr = sender.deposition_rate(chemical=chem)
                    source_matrix[tm_x] += dr
                except Exception:
                    pass

                # Some media just don't send anything
                if not sender.media.can_emit:
                    continue

                for y, receiver in enumerate(comp_list):
                    # Some media just don't receive anything
                    if not receiver.media.can_absorb:
                        continue

                    links = sender.get_links(receiver)
                    if not links:
                        continue

                    tm_y = int(chem_idx * n_comp + y)

                    print_vals = []
                    print_vals.append(
                        f'\n\t{sender.standard_name} >'
                        f' {receiver.standard_name}'
                        f' ({chem_idx + 1}/{n_chem},'
                        f' {x + 1}/{n_comp}, {y + 1}/{n_comp})'
                    )
                    # print_vals.append(links)

                    for link in links:
                        for transport_proc in link.transport_processes(chem):
                            transfer_factor = transport_proc.eval(
                                sender=sender, receiver=receiver,
                                chemical=chem,
                                environment=scenario
                            )
                            try:
                                transfer_factor = transfer_factor.magnitude
                            except Exception:
                                pass
                            print_vals.append(
                                f'\t\t- "{transport_proc.name}"'
                                f' = {transfer_factor}'
                            )

                            try:
                                if (
                                    not transfer_factor
                                    or pd.isna(transfer_factor)
                                ):
                                    continue
                            except ValueError:
                                pass

                            if transport_proc.is_transform:
                                try:
                                    real_chem_idx = chem_indices[
                                        transport_proc.output_chemical
                                    ]
                                except KeyError:
                                    real_chem_idx = -1
                                if real_chem_idx < 0:
                                    tm_y = -1
                                else:
                                    tm_y = int(real_chem_idx * n_comp + x)

                            transition_matrix[tm_x][tm_x] -= transfer_factor
                            if tm_y > -1:
                                transition_matrix[tm_y][tm_x] += (
                                    transfer_factor
                                )

                    if len(print_vals) > 1:
                        for ln in print_vals:
                            print(ln)

    except KeyboardInterrupt:
        pass

    df_tm = pd.DataFrame(
        transition_matrix, index=index_names,
        columns=index_names
    )
    df_sm = pd.DataFrame(
        source_matrix, index=index_names,
        columns=['deposition_rate_g_day-1']
    )

    return df_tm, df_sm


def safe_save_output(df_tm, df_sm):
    try:
        import os
        if not os.path.isdir('./.output'):
            os.makedirs('./.output')
        df_sm.to_csv('./.output/sm_new.csv')
        df_tm.to_csv('./.output/tm_new.csv')
    except Exception:
        pass


def check_alg_values(scenario, chemical, alg, sender, receiver):
    print('')
    print(alg)

    sender = scenario.get_compartment(sender)
    print(f'sender = {sender}')
    print(f'sender.media.id = {sender.media.id}')
    receiver = scenario.get_compartment(receiver)
    print(f'receiver = {receiver}')
    print(f'receiver.media.id = {receiver.media.id}')

    print('')
    print(f'sender.get_links(receiver) = {sender.get_links(receiver)}')

    process = TransportProcessService.get(name=alg)

    applies = process.applies_to(
        sender=sender, receiver=receiver,
        chemical=chemical
    )
    print(f'transport_process_applies = {applies}')

    from trim_db.schema.parameters.equations import evaluated_args, \
        evaluator, CANT_EVAL

    def print_args(equation, evaluator, new_names={}):
        print('')
        # print(equation)
        old_names = dict(evaluator.names)
        evaluator.names.update(new_names)
        try:
            eval_args = evaluated_args(equation, evaluator)
            for k in sorted(eval_args.keys()):
                if k in evaluator.names:
                    continue
                v = eval_args[k]
                if str(v).startswith('<function '):
                    continue

                print(f'{k} = {v}')
                if v == CANT_EVAL:
                    param = k.rsplit('.', 1)
                    obj = param[0]
                    obj = obj.split('.', 1)
                    obj[0] = f'evaluator.names.get("{obj[0]}")'
                    # print('.'.join(obj))
                    obj = eval('.'.join(obj))
                    param = param[1]
                    if '(' in param:
                        param = param.split('(')
                        args = param[1]
                        param = param[0]
                        args = [
                            x.strip()
                            for x in args.replace(')', '').split(',')
                        ]
                    else:
                        args = []
                    param = obj.parameters[param]
                    # print(f'{k} = {param}({", ".join(args)})')
                    print_args(
                        param.quantity.equation, evaluator,
                        new_names={
                            'self': obj
                        }
                    )
        finally:
            evaluator.names = old_names

    print_args(process.algorithm.equation, evaluator, new_names={
        'sender': sender,
        'receiver': receiver,
        'chemical': chemical,
        'environment': scenario
    })

    try:
        transfer_factor = process.eval(
            sender=sender, receiver=receiver,
            chemical=chemical,
            environment=scenario
        )
        print(
            f'transfer_factor = {transfer_factor}'
        )
    except TypeError as e:
        if 'Invalid arguments for "' not in str(e):
            raise
        print('Cannot evaluate transfer_factor')
    print('')


def run_tests():
    # parse_prop_types(
    #     f'{TRIM_FILES}/ICF_Master_Library_03212016_PropertyType_Exporter.txt'
    # )
    # return
    scenario = ScenarioService.get(name=SCENARIO_NAME)

    if not scenario:
        # return
        print('loading data ...')
        start = time.time()
        load_data()
        end = time.time()
        print('time to load data = ', round((end - start), 2), ' seconds')

        scenario = ScenarioService.get(name=SCENARIO_NAME)

    print('\n==========================\n')

    # print_scenario_info(scenario)

    # print_chemical_class_info()

    # print_scenario_chemical_info(scenario)

    # print_scenario_volume_element_info(scenario)

    # print_scenario_compartment_info(scenario)

    # print('creating tm ...')
    # start = time.time()
    # df_tm, df_sm = make_transition_matrix(scenario)
    # end = time.time()
    # print('time to create tm = ', round((end - start), 2), ' seconds')

    # safe_save_output(df_tm, df_sm)

    print('\n==========================\n')


if __name__ == '__main__':
    try:
        # import os
        # os.environ.setdefault('TEST_DB_SERVERLESS', 'True')
        from trim_db.utils.users_roles import implement_users_roles
        implement_users_roles()
        # time.sleep(10)
        # from trim_db.porting import *
        # from trim_db.schema import *
        # from trim_db.services import *
    except Exception as e:
        print(f'-- Unable to create Users/Roles.\n{e}')

    run_tests()
