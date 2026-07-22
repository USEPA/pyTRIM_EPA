from ...schema.mirc.parameters.models import MircParameter


def update_parameter(
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

    if (
        val == parameter.value
        and unit == parameter.unit
        and (not with_notes or notes == parameter.notes)
    ):
        return
    elif (val is None and parameter.value is None):
        return

    print(f'Changed {parameter}')

    if val is None:
        val = 0  # Blanks need to be saved as 0

    if (
        not hasattr(parameter, 'scenario')
        or parameter.scenario == None
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
