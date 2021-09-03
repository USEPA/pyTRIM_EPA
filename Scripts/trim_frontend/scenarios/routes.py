from flask import Blueprint, render_template, redirect, url_for
from flask_security import login_required, current_user
from Scripts.custom.flask_api import ApiResult
from Scripts.trim_db import Scenario
from Scripts.trim_frontend import api
from .forms import *


scenario = Blueprint('scenario', __name__)


@scenario.route('/scenario')
@login_required
def view_scenarios():
    scenarios = current_user.active_scenarios
    scenario_form = ScenarioDefinitionForm()

    return render_template(
        'scenarios/view_all.html', scenarios=scenarios,
        scenario_form=scenario_form
    )


@scenario.route('/scenario/<int:id>')
@login_required
def view_scenario(id):
    s = Scenario.query.filter_by(id=id).first()
    return render_template('scenarios/view_single.html', scenario=s)


@scenario.route('/scenario', methods=['POST'])
@login_required
def create_scenario():
    form = ScenarioDefinitionForm()
    if not form.validate_on_submit():
        redirect(url_for('scenario.view_scenarios'))

    # Create a new scenario with the form data
    s = Scenario()
    form.populate_obj(s)
    if not s.name:
        raise AssertionError("Scenario name cannot be blank.")

    # Set the current_user as the form creator
    s.creator = current_user

    # Save the scenario
    from Scripts.trim_frontend import db
    db.session.add(s)
    db.session.commit()

    return redirect(url_for('scenario.edit_scenario', id=s.id))


@scenario.route('/scenario/<int:id>/edit')
@login_required
def edit_scenario(id):
    s = Scenario.query.filter_by(id=id).first()

    return render_template('scenarios/editor.html', scenario=s)


scenario_api = Blueprint('scenario_api', __name__)
api.use_api_errors(scenario_api)


@scenario_api.route('/api/scenario/<int:id>')
@login_required
def get_scenario(id):
    s = Scenario.query.filter_by(id=id).first()

    if s is not None:
        s = s.as_serializable()
        s['emissions_sources'] = [
            {'name': 'alpha', 'chemicals': [{'rate': 100}]},
            {'name': 'beta', 'chemicals': [{'chemical': 'Chromium'}]}
        ]

    return ApiResult({'scenario': s})
