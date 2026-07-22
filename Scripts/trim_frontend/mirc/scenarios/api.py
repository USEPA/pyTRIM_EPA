from flask import request
from flask_security import login_required, current_user
from werkzeug.datastructures import MultiDict
from trim_db.services import MircScenarioService
from trim_frontend import api, db
from ...users.models import User
from .forms import MircScenarioForm as ScenarioForm

mirc_scenario_api = api.Blueprint('mirc_scenario_api', __name__)


@mirc_scenario_api.route('/api/mirc/exposure_profile/', methods=['POST'])
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

    try:
        s = MircScenarioService.from_form(form, owner=current_user)
        db.session.commit()
    except Exception:
        import traceback
        traceback.print_exc()
        raise

    if s.id is None:
        raise api.Exception({
            'form_errors': {
                'name': ['Invalid name (possibly a duplicate?)']
            }
        })

    return api.Result({'scenario': s.as_serializable()})


@mirc_scenario_api.route('/api/mirc/exposure_profile/<int:id>/', methods=['POST'])
@login_required
@api.csrf_exempt
def update_risk_scenario(id):
    scenario = MircScenarioService.get(id)

    if scenario is None:
        raise api.Exception('Exposure Profile not found', 404)

    if scenario.is_builtin:
        raise api.Exception(
            "Built-in Exposure Profiles Cannot Be Modified", 403
        )

    if not current_user.can('edit', scenario):
        raise api.Exception(
            "You don't have permission to edit this exposure profile", 403
        )

    try:
        if request.json is not None:
            form = ScenarioForm(
                formdata=MultiDict(dict(request.json))
            )
        else:
            form = ScenarioForm()
    except Exception:
        form = ScenarioForm()

    if not form.validate_on_submit():
        raise api.Exception({
            'form_errors': form.errors
        }, 400)

    try:
        MircScenarioService(scenario).update_from_form(form)
        db.session.commit()
    except Exception:
        import traceback
        traceback.print_exc()
        raise

    return api.Result({})


@mirc_scenario_api.route('/api/mirc/exposure_profile/')
@login_required
def get_risk_scenarios():
    s = MircScenarioService.get_all()

    if s:
        s = [
            x.as_serializable() for x in s
            if current_user.can('view', x)
        ]

    return api.Result({'scenarios': s})


@mirc_scenario_api.route('/api/mirc/exposure_profile/<int:id>/')
@login_required
def get_risk_scenario(id):
    s = MircScenarioService.get(id).first()

    if s is None:
        raise api.Exception('Exposure Profile not found', 404)

    if not current_user.can('view', s):
        raise api.Exception(
            "You don't have permission to view this exposure profile", 403
        )

    return api.Result({'scenario': s.as_serializable()})


@mirc_scenario_api.route('/api/mirc/exposure_profile/<int:id>/parameters/')
@login_required
def get_risk_scenario_parameters(id):
    s = MircScenarioService.get(id)

    if s is None:
        raise api.Exception('Exposure Profile not found', 404)

    if not current_user.can('view', s):
        raise api.Exception(
            "You don't have permission to view this exposure profile", 403
        )

    params = []
    for param in s.parameters:
        param = param.as_serializable()
        param.pop('scenario')
        params.append(param)

    return api.Result(params)


@mirc_scenario_api.route('/api/mirc/exposure_profile/<int:id>/permissions', methods=['POST'])
@login_required
@api.csrf_exempt
def update_risk_scenario_permissions(id):
    scenario = MircScenarioService.get(id)
    if not scenario:
        raise api.Exception('Exposure Profile not found', 404)

    if scenario.is_builtin:
        raise api.Exception(
            "Built-in Exposure Profiles Cannot Be Modified", 403
        )

    if not current_user.can('manage', scenario):
        raise api.Exception(
            "You don't have permission to manage this exposure profile", 403
        )

    if scenario.is_builtin:
        raise api.Exception((
            "Permissions for built-in exposure profiles"
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


@mirc_scenario_api.route('/api/mirc/exposure_profile/<int:id>/', methods=['DELETE'])
@login_required
@api.csrf_exempt
def delete_risk_scenario(id):
    scenario = MircScenarioService.get(id)
    if not scenario:
        raise api.Exception('Exposure Profile not found', 404)

    if scenario.is_builtin:
        raise api.Exception(
            "Built-in Exposure Profiles Cannot Be Modified", 403
        )

    if not current_user.can('manage', scenario):
        raise api.Exception(
            "You don't have permission to delete this exposure profile", 403
        )

    MircScenarioService.delete(scenario)

    return api.Result({})
