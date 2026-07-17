from flask import request
from flask_security import login_required, current_user
from werkzeug.datastructures import MultiDict
from trim_db.services import MircScenarioService
from trim_frontend import api, db
from ...users.models import User
from .forms import MircScenarioForm as ScenarioForm

mirc_scenario_api = api.Blueprint('mirc_scenario_api', __name__)


@mirc_scenario_api.route('/api/mirc/risk_scenario/', methods=['POST'])
@login_required
@api.csrf_exempt
def create_risk_scenario():
    if request.json is not None:
        form = ScenarioForm(
            formdata=MultiDict(dict(request.json))
        )
    else:
        form = ScenarioForm()

    del form.breast_milk_parameters

    if not form.validate_on_submit():
        raise api.Exception({
            'form_errors': form.errors
        }, 400)

    s = MircScenarioService.from_form(form, owner=current_user)
    db.session.commit()

    if s.id is None:
        raise api.Exception({
            'form_errors': {
                'name': ['Invalid name (possibly a duplicate?)']
            }
        })

    return api.Result({'scenario': s.as_serializable()})


@mirc_scenario_api.route('/api/mirc/risk_scenario/<int:id>/', methods=['POST'])
@login_required
@api.csrf_exempt
def update_risk_scenario(id):
    scenario = MircScenarioService.get(id)

    if scenario is None:
        raise api.Exception('Scenario not found', 404)

    if scenario.is_builtin:
        raise api.Exception(
            "Built-in Risk Scenarios Cannot Be Modified", 403
        )

    if not current_user.can('edit', scenario):
        raise api.Exception(
            "You don't have permission to edit this scenario", 403
        )

    if request.json is not None:
        form = ScenarioForm(
            formdata=MultiDict(dict(request.json))
        )
    else:
        form = ScenarioForm()

    if not form.validate_on_submit():
        raise api.Exception({
            'form_errors': form.errors
        }, 400)

    MircScenarioService(scenario).update_from_form(form)
    db.session.commit()

    return api.Result({})


@mirc_scenario_api.route('/api/mirc/risk_scenario/')
@login_required
def get_risk_scenarios():
    s = MircScenarioService.get_all()

    if s:
        s = [
            x.as_serializable() for x in s
            if current_user.can('view', s)
        ]

    return api.Result({'scenarios': s})


@mirc_scenario_api.route('/api/mirc/risk_scenario/<int:id>/')
@login_required
def get_risk_scenario(id):
    s = MircScenarioService.get(id).first()

    if s is None:
        raise api.Exception('Scenario not found', 404)

    if not current_user.can('view', s):
        raise api.Exception(
            "You don't have permission to view this scenario", 403
        )

    return api.Result({'scenario': s.as_serializable()})


@mirc_scenario_api.route('/api/mirc/risk_scenario/<int:id>/parameters/')
@login_required
def get_risk_scenario_parameters(id):
    s = MircScenarioService.get(id)

    if s is None:
        raise api.Exception('Scenario not found', 404)

    if not current_user.can('view', s):
        raise api.Exception(
            "You don't have permission to view this scenario", 403
        )

    params = []
    for param in s.parameters:
        param = param.as_serializable()
        param.pop('scenario')
        params.append(param)

    return api.Result(params)


@mirc_scenario_api.route('/api/mirc/risk_scenario/<int:id>/permissions', methods=['POST'])
@login_required
@api.csrf_exempt
def update_risk_scenario_permissions(id):
    scenario = MircScenarioService.get(id)
    if not scenario:
        raise api.Exception('Scenario not found', 404)

    if scenario.is_builtin:
        raise api.Exception(
            "Built-in Risk Scenarios Cannot Be Modified", 403
        )

    if not current_user.can('manage', scenario):
        raise api.Exception(
            "You don't have permission to manage this scenario", 403
        )

    if scenario.is_builtin:
        raise api.Exception((
            "Permissions for built-in scenarios"
            " cannot be updated through the API"
        ), 403)

    if request.json is not None:
        for email, permission in request.json['permissions'].items():
            u = User.query.filter_by(email=email).first()
            if u:
                MircScenarioService.revoke(scenario, u)
                if permission != 'none':
                    MircScenarioService.grant(scenario, u, permission)
        db.session.commit()

    return api.Result({})


@mirc_scenario_api.route('/api/mirc/risk_scenario/<int:id>/', methods=['DELETE'])
@login_required
@api.csrf_exempt
def delete_risk_scenario(id):
    scenario = MircScenarioService.get(id)
    if not scenario:
        raise api.Exception('Scenario not found', 404)

    if scenario.is_builtin:
        raise api.Exception(
            "Built-in Risk Scenarios Cannot Be Modified", 403
        )

    if not current_user.can('manage', scenario):
        raise api.Exception(
            "You don't have permission to delete this scenario", 403
        )

    MircScenarioService.delete(scenario)

    return api.Result({})
