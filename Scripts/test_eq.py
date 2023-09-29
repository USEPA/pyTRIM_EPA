import argparse
from trim_db.schema.parameters.equations import *
from trim_db.schema.parameters.equations import evaluated_args

def parse_equation(eq):
    print('')
    print(eq)
    print('')
    print('deconstruct_equation ->')
    print(deconstruct_equation(eq))
    print('')
    print('find_arguments ->')
    print(find_arguments(eq))
    print('')
    print('find_arguments(!combine_partial_args) ->')
    print(find_arguments(eq, combine_partial_args=False))
    print('')
    print('find_arguments(!drop_functions) ->')
    print(find_arguments(eq, drop_functions=False))
    print('')
    print('find_arguments(!combine_partial_args, !drop_functions) ->')
    print(find_arguments(eq, combine_partial_args=False, drop_functions=False))
    print('')
    print('evaluated_args ->')
    print(evaluated_args(eq))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--equation')
    args = parser.parse_args()
    # eq = (
    #     '(- math.exp(1 - chemical.SedimentPartitioning_AlphaofEquilibrium(sender)) / chemical.SedimentPartitioning_TimeToReachAlphaofEquilibrium(sender))'
    # )
    # eq = (
    #     '(chemical.EffectiveAdvectionVelocity(sender) * chemical.GradientofSoilConcentrationChange(sender)) / (math.exp(chemical.GradientofSoilConcentrationChange(sender) * sender) - 1)'
    # )

    parse_equation(args.equation)
