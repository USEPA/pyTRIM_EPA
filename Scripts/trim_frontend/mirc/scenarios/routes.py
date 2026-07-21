from flask import Blueprint, render_template, abort, request, \
    redirect, url_for
from flask_security import login_required, current_user
from trim_db.services import MircScenarioService, ChemicalService, \
    MircProductService, MircLifeStageService, MircPercentileService, \
    UserService
from trim_frontend import api
from .forms import MircScenarioForm
from .utils import disable_form_fields, get_fragment_args


mirc_scenario = Blueprint('mirc_scenario', __name__)


@mirc_scenario.route('/mirc/risk_scenario', methods=['GET'])
@login_required
def view_risk_scenarios():
    scenarios = [
        ms for ms in MircScenarioService.get_all()
        if current_user.can('view', ms)
    ]

    return render_template(
        'mirc/risk_scenarios/dashboard.html', title='Risk Scenarios',
        mirc_scenarios=scenarios,
        scenario_form=MircScenarioForm()
    )


@mirc_scenario.route('/mirc/risk_scenario/<int:id>/')
@login_required
def view_risk_scenario(id):
    ms = MircScenarioService.get(id)
    if ms is None:
        return abort(404)

    if not current_user.can('edit', ms):
        return abort(403)

    p = sorted(MircProductService.get_all(), key=lambda x: x.name)
    c = ChemicalService.get_all()
    ages = sorted(MircLifeStageService.get_all(), key=lambda x: x.name)
    pcts = MircPercentileService.get_all()

    form = MircScenarioForm(data={
        'scenario_id': ms.id,
        'name': ms.name,
        'parent': ms.parent.id if ms.parent else None
    })
    if ms.is_builtin:
        disable_form_fields(form)

    mirc_scenarios = [
        x for x in MircScenarioService.get_all()
        if current_user.can('view', x)
    ]

    return render_template(
        'mirc/risk_scenarios/editor.html', mirc_scenario=ms, title=ms.name,
        form=form, mirc_scenarios=mirc_scenarios,
        products=p, ages=ages, percentiles=pcts,
        chemicals=c
    )


@mirc_scenario.route('/mirc/risk_scenario/form_fragment/', methods=['POST'])
@login_required
@api.csrf_exempt
def get_form_fragment():
    data = request.json

    name = data['name']
    scenario_id = data.get('scenario_id') or 0

    ms = MircScenarioService.get(int(scenario_id))
    if ms is None:
        # Check if there is a parent id, if this is a new scenario
        parent_id = data.get('parent_id') or 0
        ms = MircScenarioService.get(int(parent_id))

    params = get_fragment_args(name, ms, data)

    return render_template(
        f'components/scenarios/mirc/risk_scenarios/editor/{name}_fragment.html',
        scenario=ms, **(params or {})
    )


@mirc_scenario.route('/mirc/risk_scenario/<int:id>/permissions/')
@login_required
def risk_scenario_permissions(id):
    ms = MircScenarioService.get(id)
    if not ms:
        return abort(404)

    if ms.is_builtin:
        return abort(403)  # Don't allow editing builtins this way

    if not current_user.can('manage', ms):
        return abort(403)

    users = UserService.get_all()

    return render_template(
        'mirc/risk_scenarios/permissions.html', mirc_scenario=ms, users=users
    )
