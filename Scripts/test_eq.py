from trim_db.schema.parameters.equations import *
from trim_db.schema.parameters.equations import evaluated_args

if __name__ == '__main__':
    eq = (
        '((self.HowMuchFasterHgEliminationIsThanForMHg(compartment) * math.exp(0.066 * (compartment.linked_compartments(media="Surface_Water")[0].WaterTemperature_C) - 0.20 * math.log(compartment.BW.to("g")) - 5.83)) if compartment.media.id in {26 , 29 , 30} else ((self.HowMuchFasterHgEliminationIsThanForMHg(compartment) * math.exp(0.066 * (compartment.linked_compartments(media="Surface_Water")[0].WaterTemperature_C) - 0.20 * math.log(compartment.BW.to("g")) / math.log(math.exp(1.0)) - 5.83)) if compartment.media.id in {24 , 25 , 22} else 0))'
    )

    print(eq)
    print('')
    print(deconstruct_equation(eq))
    print('')
    print(find_arguments(eq))
    print('')
    print(find_arguments(eq, combine_partial_args=False))
    print('')
    print(find_arguments(eq, drop_functions=False))
    print('')
    print(find_arguments(eq, combine_partial_args=False, drop_functions=False))
    print('')
    print(evaluated_args(eq))
