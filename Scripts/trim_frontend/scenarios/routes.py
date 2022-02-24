from flask import Blueprint, request, render_template, redirect, url_for
from flask_security import login_required, current_user
from custom.flask_api import ApiResult,  ApiException
from trim_db import ScenarioService, ParcelService
from trim_frontend import api
from .forms import *
from trim_db import Scenario, Parcel
from ..utils.logging import make_logger

import traceback
import re
import json

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
    s = ScenarioService.create(no_commit=True)
    form.populate_obj(s)
    if not s.name:
        raise AssertionError("Scenario name cannot be blank.")

    # Set the current_user as the form creator
    s.creator = current_user

    # Save the scenario
    ScenarioService.commit()

    return redirect(url_for('scenario.edit_scenario', id=s.id))


@scenario.route('/scenario/<int:id>/edit')
@login_required
def edit_scenario(id):
    s = ScenarioService.get(id)

    return render_template('scenarios/editor.html', scenario=s)


scenario_api = Blueprint('scenario_api', __name__)
api.use_api_errors(scenario_api)


@scenario_api.route('/api/scenario/<int:id>')
@login_required
def get_scenario(id):
    s = ScenarioService.get(id)

    if s is not None:
        s = s.as_serializable()
        s['emissions_sources'] = [
            {'name': 'alpha', 'chemicals': [{'rate': 100}]},
            {'name': 'beta', 'chemicals': [{'chemical': 'Chromium'}]}
        ]

    return ApiResult({'scenario': s})


parcels_api = Blueprint('parcels_api', __name__)
api.use_api_errors(parcels_api)


@parcels_api.route('/api/parcels', methods=['POST'])
@login_required
def create_parcels():
    logger = make_logger('parcels_api_create')
    # form = ScenarioParcelsForm()
    # if not form.validate_on_submit():
    #    redirect(url_for('parcel.view_parcels'))
    try:
        parcels_data = request.form.to_dict()
        from_url = request.referrer
        this_scenario_id = int(re.findall('/scenario/(\d+)/', from_url)[0])
        if not this_scenario_id:
            raise ApiException("No Scenario defined")
        # if not parcels_data:
        #    raise ApiException("No parcels defined")

        # Create a new parcel with the form data
        p = ParcelService.create(no_commit=True)
        # form.populate_obj(p)

        if not parcels_data['name']:
            raise AssertionError("Parcel name cannot be blank.")

        p.name = parcels_data['name']
        p.description = parcels_data['desc']
        p.scenario_id = this_scenario_id
        p.vertices = json.loads(parcels_data['geom'])

        # Save the scenario
        ParcelService.commit()
    except Exception as e:
        logger.error(traceback.format_exc())

    return "success"


@parcels_api.route('/api/parcels/', methods=['GET'])
@login_required
def get_parcels():
    logger = make_logger('parcels_api_get')
    try:
        from_url = request.referrer
        this_scenario_id = int(re.findall('/scenario/(\d+)/', from_url)[0])
        if not this_scenario_id:
            raise ApiException("No Scenario defined")
        p = ParcelService.get_all(scenario_id=this_scenario_id)
        parcels = []
        if p is not None:
            for i, this_p in enumerate(p):
                parcels.append(this_p.as_serializable())
    except Exception as e:
        logger.error(traceback.format_exc())

    return ApiResult({'scenario': parcels})

