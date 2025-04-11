from .config import *
from ..schema import Chemical
from ..services import ChemicalService

__all__ = ['parse_chemicals']


def parse_chemicals(
    chemical_parameters, scenario=None,
    message='Loading chemicals from library data ...'
):
    if message:
        print(message)

    for name, params in chemical_parameters.items():
        cas = params['CAS']['value']

        chem = ChemicalService.get_or_create(
            cas_number=cas, no_commit=True
        )
        chem.name = name
        ChemicalService.commit()

        prop_entity = chem  # Attach properties to this chemical
        if scenario is not None:
            if scenario.chemicals and chem not in scenario.chemicals:
                continue
            # Make sure this is set so we don't add global parameters
            chem.current_scenario(scenario)

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
