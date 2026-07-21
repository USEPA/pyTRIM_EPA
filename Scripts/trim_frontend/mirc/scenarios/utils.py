from wtforms import FormField, FieldList
from trim_db.services import ChemicalService, \
    MircProductService, MircLifeStageService, MircPercentileService
from .forms import MircScenarioForm


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


def human_ingestion_fragment_args(form, scenario, opts):
    prods = MircProductService.get_all()
    try:
        a_id = int(opts['age'])
    except TypeError:
        return None
    age = MircLifeStageService.get(a_id)
    try:
        p_id = int(opts['percentile'])
    except TypeError:
        return None
    pct = MircPercentileService.get(p_id)

    params = form.human_ingestion_parameters

    i = opts.get('i')
    for _ in range(i):
        params.append_entry()

    entries = []
    for p in prods:
        if not p.is_food:
            continue
        data = {
            'life_stage_id': age.id,
            'life_stage': age.name.title(),
            'percentile_id': pct.id,
            'percentile': pct.name.title(),
            'product_id': p.id,
            'product': p.name.title()
        }
        ir = scenario.parameters.for_food(
            p
        ).at_life_stage(age).at_percentile(pct).IR
        if ir:
            data.update({
                'rate': ir.value,
                'unit': ir.unit,
                'notes': ir.notes
            })
        fc = scenario.parameters.for_media(p).FC
        if fc:
            data.update({
                'fraction_contaminated': fc.value
            })

        params.append_entry(data)
        entries.append(params.entries[-1])

    return {'irs': entries}


def body_weight_fragment_args(form, scenario, opts):
    pcts = MircPercentileService.get_all()
    try:
        a_id = int(opts['age'])
    except TypeError:
        return None
    age = MircLifeStageService.get(a_id)

    params = form.body_weight_parameters

    i = opts.get('i')
    for _ in range(i):
        params.append_entry()

    entries = []
    for pct in pcts:
        if pct.name == 'None':
            continue
        data = {
            'life_stage_id': age.id,
            'life_stage': age.name.title(),
            'percentile_id': pct.id,
            'percentile': pct.name.title()
        }
        bw = scenario.parameters.at_life_stage(age).at_percentile(pct).BW
        if bw:
            data.update({
                'value': bw.value,
                'unit': bw.unit,
                'notes': bw.notes
            })
        params.append_entry(data)
        entries.append(params.entries[-1])

    return {'bws': entries}


def product_parameter_fragment_args(form, scenario, opts):
    try:
        p_id = int(opts['product'])
    except TypeError:
        return None
    p = MircProductService.get(p_id)

    params = form.product_parameters

    i = opts.get('i')
    for _ in range(i):
        params.append_entry()

    p_props = scenario.parameters.for_media(p)
    if not p_props:
        return None

    data = {
        'product_id': p.id,
        'product': p.name.title(),
        'EF': p_props.EF.value
    }
    params.append_entry(data)
    entry = params.entries[-1]

    return {'pp': entry}


def plant_parameter_fragment_args(form, scenario, opts):
    try:
        p_id = int(opts['product'])
    except TypeError:
        return None
    p = MircProductService.get(p_id)

    if not p.is_a('plant'):
        return None

    params = form.plant_parameters

    i = opts.get('i')
    for _ in range(i):
        params.append_entry()

    plant_props = scenario.parameters.for_media(p)

    data = {
        'product_id': p.id,
        'product': p.name.title(),
        'MAF': plant_props.MAF.value,
        'Rp': plant_props.Rp.value,
        'kp': plant_props.kp.value,
        'kp_unit': plant_props.kp.unit,
        'Tp': plant_props.Tp.value,
        'Tp_unit': plant_props.Tp.unit,
        'Yp': plant_props.Yp.value,
        'Yp_unit': plant_props.Yp.unit
    }
    params.append_entry(data)
    entry = params.entries[-1]

    return {'pp': entry}


def animal_ingestion_fragment_args(form, scenario, opts):
    prods = MircProductService.get_all()
    try:
        c_id = int(opts['consumer'])
    except TypeError:
        return None
    c = MircProductService.get(c_id)

    if not c.is_a('animal'):
        return None

    params = form.animal_ingestion_parameters

    i = opts.get('i')
    for _ in range(i):
        params.append_entry()

    p_props = scenario.parameters.for_media(c)

    entries = []
    for p in prods:
        if not p.is_feed:
            continue
        data = {
            'consumer_id': c.id,
            'consumer': c.name.title(),
            'product_id': p.id,
            'product': p.name.title()
        }

        ir = p_props.for_food(p).IR
        if ir:
            data.update({
                'rate': ir.value,
                'unit': ir.unit,
                'notes': ir.notes
            })
        fc = scenario.parameters.for_media(p).FC
        if fc:
            data.update({
                'fraction_contaminated': fc.value
            })

        params.append_entry(data)
        entries.append(params.entries[-1])

    return {'irs': entries}


def breast_milk_parameter_fragment_args(form, scenario, opts):
    p = MircProductService.get(name='breast milk')

    params = form.breast_milk_parameters

    bm_props = scenario.parameters.for_media(p)
    if not bm_props:
        return None

    data = {
        'f_mbm': bm_props.f_mbm.value,
        'f_fm': bm_props.f_fm.value,
        'f_pm': bm_props.f_pm.value,
        't_pn': bm_props.t_pn.value,
        't_pn_unit': bm_props.t_pn.unit
    }
    params.form.process(data=data)

    return {'bmp': params}


def loss_factor_fragment_args(form, scenario, opts):
    try:
        p_id = int(opts['product'])
    except TypeError:
        return None
    p = MircProductService.get(p_id)

    params = form.product_loss_parameters

    i = opts.get('i')
    for _ in range(i):
        params.append_entry()

    p_props = scenario.parameters.for_media(p)

    entries = []
    lfs = p_props.LF
    if not isinstance(lfs, list):
        lfs = [lfs]
    for lf in lfs:
        if lf.value == 0:
            continue
        data = {
            'product_id': p.id,
            'product': p.name.title(),
            'fraction_lost': lf.value,
            'loss_description': lf.name,
            'source': lf.source
        }
        params.append_entry(data)
        entries.append(params.entries[-1])
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
    c = ChemicalService.get(c_id)

    params = form.chemical_parameters

    i = opts.get('i')
    for _ in range(i):
        params.append_entry()

    chem_props = scenario.parameters.for_chemical(c)

    data = {
        'chemical_id': c.id,
        'chemical': (c.hap_name or c.name).title(),
        'Fw': chem_props.Fw.value,
        'soil_adjustment': chem_props.SoilAdjFactor.value,
        'CSF': chem_props.CSF.value,
        'CSF_unit': chem_props.CSF.unit,
        'RfD': chem_props.RfD.value,
        'RfD_unit': chem_props.RfD.unit
    }
    params.append_entry(data)
    entry = params.entries[-1]

    return {'cp': entry}


def mutagenic_parameter_fragment_args(form, scenario, opts):
    try:
        c_id = int(opts['chemical'])
    except TypeError:
        return None
    c = ChemicalService.get(c_id)
    ages = MircLifeStageService.get_all()

    params = form.mutagenic_parameters

    i = opts.get('i')
    for _ in range(i):
        params.append_entry()

    chem_props = scenario.parameters.for_chemical(c)

    entries = []
    for age in ages:
        if age.name == 'Pregnant Mother':
            continue
        data = {
            'chemical_id': c.id,
            'chemical': (c.hap_name or c.name).title(),
            'life_stage_id': age.id,
            'life_stage': age.name
        }
        adaf = chem_props.at_life_stage(age).ADAF
        if adaf:
            data.update({
                'value': adaf.value,
                'notes': adaf.notes
            })
        params.append_entry(data)
        entries.append(params.entries[-1])

    return {'adafs': entries}


def baf_parameter_fragment_args(form, scenario, opts):
    try:
        c_id = int(opts['chemical'])
    except TypeError:
        return None
    c = ChemicalService.get(c_id)
    ats = MircProductService.get_all()

    params = form.baf_parameters

    i = opts.get('i')
    for _ in range(i):
        params.append_entry()

    chem_props = scenario.parameters.for_chemical(c)

    entries = []
    for at in ats:
        if not at.is_a('fish') or at.name == 'fish':
            continue
        nm = at.name.lower()
        ft = 'BSAF' if 'benthic' in nm else 'BAF'
        data = {
            'chemical_id': c.id,
            'chemical': (c.hap_name or c.name).title(),
            'aquatic_type_id': at.id,
            'aquatic_type': f'{nm.title()} ({ft})',
        }
        baf = chem_props.for_media(at).get_by_variable(ft)
        if baf:
            data.update({
                'value': baf.value,
                'unit': baf.unit,
                'notes': baf.notes
            })
        params.append_entry(data)
        entries.append(params.entries[-1])

    return {'bafs': entries}


def plant_chemical_parameter_fragment_args(form, scenario, opts):
    try:
        c_id = int(opts['chemical'])
    except TypeError:
        return None
    c = ChemicalService.get(c_id)
    try:
        p_id = int(opts['product'])
    except TypeError:
        return None
    p = MircProductService.get(p_id)

    params = form.plant_chemical_parameters

    i = opts.get('i')
    for _ in range(i):
        params.append_entry()

    chem_props = scenario.parameters.for_chemical(c)
    if not chem_props:
        return None

    data = {
        'chemical_id': c.id,
        'chemical': (c.hap_name or c.name).title(),
        'product_id': p.id,
        'product': p.name
    }
    cp_props = chem_props.for_media(p)
    data.update({
        'Br': cp_props.Br.value,
        'VG': cp_props.VG.value,
        'Bv_ag': cp_props.Bv_ag.value,
        'RCF': cp_props.RCF.value,
        'RCF_unit': cp_props.RCF.unit,
        'notes': cp_props.notes
    })
    params.append_entry(data)
    entry = params.entries[-1]

    return {'pcp': entry}


def animal_chemical_parameter_fragment_args(form, scenario, opts):
    try:
        c_id = int(opts['chemical'])
    except TypeError:
        return None
    c = ChemicalService.get(c_id)
    try:
        p_id = int(opts['product'])
    except TypeError:
        return None
    p = MircProductService.get(p_id)

    params = form.animal_chemical_parameters

    i = opts.get('i')
    for _ in range(i):
        params.append_entry()

    chem_props = scenario.parameters.for_chemical(c)
    if not chem_props:
        return None

    data = {
        'chemical_id': c.id,
        'chemical': (c.hap_name or c.name).title(),
        'product_id': p.id,
        'product': p.name
    }
    ca_props = chem_props.for_media(p)
    data.update({
        'Bs': ca_props.Bs.value,
        'MF': ca_props.MF.value,
        'cooking_adjustment': ca_props.FishAdjFactor.value,
        'Ba': ca_props.Ba.value,
        'Ba_unit': ca_props.Ba.unit,
        'notes': ca_props.notes
    })
    params.append_entry(data)
    entry = params.entries[-1]

    return {'acp': entry}


def breast_milk_chemical_parameter_fragment_args(form, scenario, opts):
    try:
        c_id = int(opts['chemical'])
    except TypeError:
        return None
    c = ChemicalService.get(c_id)
    p = MircProductService.get(name='breast milk')

    params = form.breast_milk_chemical_parameters

    i = opts.get('i')
    for _ in range(i):
        params.append_entry()

    chem_props = scenario.parameters.for_chemical(c)
    if not chem_props:
        return None

    data = {
        'chemical_id': c.id,
        'chemical': (c.hap_name or c.name).title(),
        'product_id': p.id,
        'product': p.name
    }
    bm_props = chem_props.for_media(p)
    data.update({
        'AE_inf': bm_props.AE_inf.value,
        'AE_mat': bm_props.AE_mat.value,
        'f_bl': bm_props.f_bl.value,
        'f_f': bm_props.f_f.value,
        'f_pl': bm_props.f_pl.value,
        'h_bm': bm_props.h_bm.value,
        'h_bm_unit': bm_props.h_bm.unit,
        'k_elim': bm_props.k_elim.value,
        'k_elim_unit': bm_props.k_elim.unit,
        'k_aq_elac': bm_props.k_aq_elac.value,
        'k_aq_elac_unit': bm_props.k_aq_elac.unit,
        'PC_pl_aq': bm_props.PC_pl_aq.value,
        'PC_pl_aq_unit': bm_props.PC_pl_aq.unit,
        'PC_rbc_pl': bm_props.PC_rbc_pl.value,
        'PC_rbc_pl_unit': bm_props.PC_rbc_pl.unit,
        'notes': bm_props.notes
    })
    params.append_entry(data)
    entry = params.entries[-1]

    return {'bmcp': entry}
