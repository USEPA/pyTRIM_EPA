import argparse
from trim_db.schema import *
from trim_db.services import *


def inspect_scenario(scenario_name):
    scenario = ScenarioService.get(name=scenario_name)
    if not scenario:
        print(f'Scenario "{scenario_name}" does not exist!')
        return

    print('\n==========================\n')

    print_scenario_info(scenario)

    print_chemical_class_info()

    print_scenario_chemical_info(scenario)

    print_scenario_volume_element_info(scenario)

    print_scenario_compartment_info(scenario)

    print('\n==========================\n')


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
            '\nc1.interface_with(c2) =',
            c1.interface_with(c2)
        )
        print('c1.connects_to(c2) =', c1.connects_to(c2))

        print('\n==========================\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', default=None)
    args = parser.parse_args()

    from trim_db.local import *  # Loads user/role tables

    inspect_scenario(args.name)
