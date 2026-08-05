from wtforms import FormField, FieldList
from trim_db.services import MircProductService
from ..forms import MircScenarioForm
from .reports import *

__all__ = ['disable_form_fields', 'get_fragment_args']


# ===========================================
# Form helpers
# ===========================================


def disable_form_fields(form):
    for field in form:
        if isinstance(field, FormField):
            disable_form_fields(field)
        elif isinstance(field, FieldList):
            for subfield in field.entries:
                disable_form_fields(subfield)
        else:
            field.render_kw = field.render_kw or {}
            field.render_kw['readonly'] = True
            field.render_kw['disabled'] = True
            try:
                field.widget.params = field.widget.params or {}
                field.widget.params['readonly'] = True
                field.widget.params['disabled'] = True
            except Exception:
                pass


def get_fragment_args(fragment_name, scenario, opts):
    if not scenario:
        return None

    form = MircScenarioForm(data={
        'scenario_id': scenario.id,
        'name': scenario.name,
        'parent': scenario.parent.id if scenario.parent else None
    })

    if fragment_name == 'human_ingestion':
        params = human_ingestion_fragment_args(form, scenario, opts)

    elif fragment_name == 'body_weight':
        params = body_weight_fragment_args(form, scenario, opts)

    elif fragment_name == 'product_parameter':
        params = product_parameter_fragment_args(form, scenario, opts)

    elif fragment_name == 'breast_milk_parameter':
        params = breast_milk_parameter_fragment_args(form, scenario, opts)

    elif fragment_name == 'plant_parameter':
        params = plant_parameter_fragment_args(form, scenario, opts)

    elif fragment_name == 'animal_ingestion':
        params = animal_ingestion_fragment_args(form, scenario, opts)

    elif fragment_name == 'loss_factor':
        params = loss_factor_fragment_args(form, scenario, opts)

    elif fragment_name == 'chemical_parameter':
        params = chemical_parameter_fragment_args(form, scenario, opts)

    elif fragment_name == 'mutagenic_parameter':
        params = mutagenic_parameter_fragment_args(form, scenario, opts)

    elif fragment_name == 'baf_parameter':
        params = baf_parameter_fragment_args(form, scenario, opts)

    elif fragment_name == 'plant_chemical_parameter':
        params = plant_chemical_parameter_fragment_args(form, scenario, opts)

    elif fragment_name == 'animal_chemical_parameter':
        params = animal_chemical_parameter_fragment_args(form, scenario, opts)

    elif fragment_name == 'breast_milk_chemical_parameter':
        params = breast_milk_chemical_parameter_fragment_args(
            form, scenario, opts
        )
    else:
        raise NotImplementedError

    if scenario.is_builtin:
        # Need to do this AFTER so all the fields are added in correctly.
        disable_form_fields(form)

    return params


# ===========================================
# Form-fragment data loaders
# ===========================================


def human_ingestion_fragment_args(form, scenario, opts):
    try:
        a_id = int(opts['age'])
    except TypeError:
        return None
    try:
        p_id = int(opts['percentile'])
    except TypeError:
        return None

    params = form.human_ingestion_parameters

    i = opts.get('i')
    for _ in range(i):
        params.append_entry()

    entries = []
    for data in get_human_ingestion_rates(scenario, age_id=a_id, percentile_id=p_id):
        params.append_entry(data)
        entries.append(params.entries[-1])

    return {'irs': entries}


def body_weight_fragment_args(form, scenario, opts):
    try:
        a_id = int(opts['age'])
    except TypeError:
        return None

    params = form.body_weight_parameters

    i = opts.get('i')
    for _ in range(i):
        params.append_entry()

    entries = []
    for data in get_human_body_weights(scenario, age_id=a_id, include_no_percentile=False):
        params.append_entry(data)
        entries.append(params.entries[-1])

    return {'bws': entries}


def product_parameter_fragment_args(form, scenario, opts):
    try:
        p_id = int(opts['product'])
    except TypeError:
        return None

    params = form.product_parameters

    i = opts.get('i')
    for _ in range(i):
        params.append_entry()

    data = get_human_food_parameters(scenario, product_id=p_id)

    if not data:
        return None

    params.append_entry(data[0])
    entry = params.entries[-1]

    return {'pp': entry}


def plant_parameter_fragment_args(form, scenario, opts):
    try:
        p_id = int(opts['product'])
    except TypeError:
        return None

    data = get_plant_parameters(scenario, product_id=p_id)

    if not data:
        return None

    params = form.plant_parameters

    i = opts.get('i')
    for _ in range(i):
        params.append_entry()

    params.append_entry(data[0])
    entry = params.entries[-1]

    return {'pp': entry}


def animal_ingestion_fragment_args(form, scenario, opts):
    try:
        c_id = int(opts['consumer'])
    except TypeError:
        return None

    irs = get_animal_ingestion_rates(scenario, consumer_id=c_id)

    if not irs:
        return None

    params = form.animal_ingestion_parameters

    i = opts.get('i')
    for _ in range(i):
        params.append_entry()

    entries = []
    for data in irs:
        params.append_entry(data)
        entries.append(params.entries[-1])

    return {'irs': entries}


def breast_milk_parameter_fragment_args(form, scenario, opts):
    params = form.breast_milk_parameters

    data = get_breast_milk_parameters(scenario)

    if not data:
        return None

    params.form.process(data=data)

    return {'bmp': params}


def loss_factor_fragment_args(form, scenario, opts):
    try:
        p_id = int(opts['product'])
    except TypeError:
        return None

    params = form.product_loss_parameters

    i = opts.get('i')
    for _ in range(i):
        params.append_entry()

    entries = []
    for data in get_loss_factors(scenario, product_id=p_id):
        params.append_entry(data)
        entries.append(params.entries[-1])

    p = MircProductService.get(p_id)
    params.append_entry({
        'product_id': p.id,
        'product': p.name.title(),
        'fraction_lost': 0
    })
    dummy = params.entries[-1]

    return {'lfs': entries, 'p': p, 'dummy': dummy}


def chemical_parameter_fragment_args(form, scenario, opts):
    try:
        c_id = int(opts['chemical'])
    except TypeError:
        return None

    params = form.chemical_parameters

    i = opts.get('i')
    for _ in range(i):
        params.append_entry()

    data = get_chemical_parameters(scenario, chemical_id=c_id)

    params.append_entry(data[0])
    entry = params.entries[-1]

    return {'cp': entry}


def mutagenic_parameter_fragment_args(form, scenario, opts):
    try:
        c_id = int(opts['chemical'])
    except TypeError:
        return None

    params = form.mutagenic_parameters

    i = opts.get('i')
    for _ in range(i):
        params.append_entry()

    entries = []
    for data in get_mutagenic_parameters(scenario, chemical_id=c_id):
        params.append_entry(data)
        entries.append(params.entries[-1])

    return {'adafs': entries}


def baf_parameter_fragment_args(form, scenario, opts):
    try:
        c_id = int(opts['chemical'])
    except TypeError:
        return None

    params = form.baf_parameters

    i = opts.get('i')
    for _ in range(i):
        params.append_entry()

    entries = []
    for data in get_baf_parameters(scenario, chemical_id=c_id):
        params.append_entry(data)
        entries.append(params.entries[-1])

    return {'bafs': entries}


def plant_chemical_parameter_fragment_args(form, scenario, opts):
    try:
        c_id = int(opts['chemical'])
    except TypeError:
        return None
    try:
        p_id = int(opts['product'])
    except TypeError:
        return None

    params = form.plant_chemical_parameters

    i = opts.get('i')
    for _ in range(i):
        params.append_entry()

    data = get_plant_chemical_parameters(scenario, chemical_id=c_id, product_id=p_id)
    if not data:
        return None

    params.append_entry(data[0])
    entry = params.entries[-1]

    return {'pcp': entry}


def animal_chemical_parameter_fragment_args(form, scenario, opts):
    try:
        c_id = int(opts['chemical'])
    except TypeError:
        return None
    try:
        p_id = int(opts['product'])
    except TypeError:
        return None

    params = form.animal_chemical_parameters

    i = opts.get('i')
    for _ in range(i):
        params.append_entry()

    data = get_animal_chemical_parameters(scenario, chemical_id=c_id, product_id=p_id)
    if not data:
        return None

    params.append_entry(data[0])
    entry = params.entries[-1]

    return {'acp': entry}


def breast_milk_chemical_parameter_fragment_args(form, scenario, opts):
    try:
        c_id = int(opts['chemical'])
    except TypeError:
        return None

    params = form.breast_milk_chemical_parameters

    i = opts.get('i')
    for _ in range(i):
        params.append_entry()

    data = get_breast_milk_chemical_parameters(scenario, chemical_id=c_id)
    if not data:
        return None

    params.append_entry(data[0])
    entry = params.entries[-1]

    return {'bmcp': entry}
