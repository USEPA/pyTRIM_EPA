from ...schema.mirc import MircParameter, NullParameter
from ...schema import ureg


def get_updated_parameter(
    scenario, parameter_form,
    variable, parameter_name,
    chemical=None, media=None, food=None,
    life_stage=None, percentile=None,
    value_name='value', unit_name='unit',
    with_notes=True
):
    try:
        val = getattr(parameter_form, value_name).data
    except AttributeError:
        val = None
    try:
        if unit_name is not None:
            unit = getattr(parameter_form, unit_name).data
        else:
            unit = None
    except AttributeError:
        unit = None
    if unit == 'dimensionless':
        unit = ''
    notes = None
    if with_notes:
        try:
            notes = parameter_form.notes.data
        except AttributeError:
            notes = None
        notes = notes or None

    params = scenario.parameters
    if chemical is not None and chemical > -1:
        params = params.for_chemical(chemical)
    if media is not None and media > -1:
        params = params.for_media(media)
    if food is not None and food > -1:
        params = params.for_food(food)
    if life_stage is not None and life_stage > -1:
        params = params.at_life_stage(life_stage)
    if percentile is not None and percentile > -1:
        params = params.at_percentile(percentile)

    parameter = getattr(params, variable)

    if isinstance(parameter, list):
        if len(parameter) == 1:
            parameter = parameter[0]
        else:
            raise TypeError(f'Found too many parameters: {parameter}')

    def parameter_matches(param, v, u, n):
        if isinstance(param, NullParameter):
            if not (
                v is None or v == 0 or str(v).strip() == ''
                or v == param.value
            ):
                # New value wasn't null-ish
                return False
            if not (
                u is None or str(u).strip() == ''
                or ureg(u) == ureg(param.unit)
            ):
                # New unit wasn't null-ish
                return False
            if with_notes:
                # New notes weren't null-ish
                if param.notes != n:
                    return False
        else:
            if param.value != v:
                # New value didn't match
                return False
            if param.unit != u:
                # New unit didn't match
                return False
            if with_notes:
                if param.notes != n:
                    # New notes didn't match
                    return False
        return True

    if parameter_matches(parameter, val, unit, notes):
        return

    print(f'Changed {parameter} ({parameter_name}) -> {val} {unit}, "{notes}"')

    if val is None:
        val = 0  # Blanks need to be saved as 0

    if (
        not hasattr(parameter, 'scenario')
        or parameter.scenario is None
        or parameter.scenario.id != scenario.id
    ):
        parameter = MircParameter(
            scenario=scenario,
            chemical=params.chemical,
            media=params.media,
            food=params.food,
            percentile=params.percentile,
            life_stage=params.life_stage,
            name=parameter_name,
            variable=variable
        )
    parameter.value = val
    parameter.unit = unit
    if with_notes:
        parameter.notes = notes

    print(f'New value: {parameter}')

    return parameter
