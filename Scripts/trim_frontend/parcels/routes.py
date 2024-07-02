from flask import Blueprint, request, render_template
from flask_security import login_required
from flask_api import ApiResult,  ApiException
from trim_db.services import *
from trim_db.schema import *
from trim_frontend import api
from .defaults import *
from .forms import *
from .utils import delete_parcel_contents, handle_parcel_update, initialize_parcel_contents
from ..scenarios.forms import *
from ..utils.logging import make_logger

import traceback
import re
import json
import time

parcels_api = Blueprint('parcels_api', __name__)
api.use_api_errors(parcels_api)


@parcels_api.route(
    '/api/scenario/<int:scenario_id>/parcel', methods=['POST']
)
@login_required
def create_parcel(scenario_id):
    s = ScenarioService.get(scenario_id)
    if not s:
        raise ApiException("Unknown Scenario")

    logger = make_logger('parcels_api_create')
    # form = ScenarioParcelsForm()
    try:
        parcels_data = request.form.to_dict()
        # if not parcels_data:
        #    raise ApiException("No parcels defined")

        # Create a new parcel with the form data
        p = ParcelService.create(no_commit=True)
        # form.populate_obj(p)

        if not parcels_data['name']:
            raise AssertionError("Parcel name cannot be blank.")

        p.name = parcels_data['name']
        p.description = parcels_data['desc']
        p.scenario_id = scenario_id
        p.vertices = json.loads(parcels_data['geom'])

        # Save the scenario
        ParcelService.commit()
        # Add default compartments, media and parameters
        initialize_parcel_contents(p)
        media = LAND_USE_TYPES
    except Exception as e:
        logger.error(traceback.format_exc())

    return ApiResult({'scenario': p.as_serializable(), 'media': media})


@parcels_api.route(
    '/api/scenario/<int:scenario_id>/parcel', methods=['GET']
)
@login_required
def get_parcels(scenario_id):
    logger = make_logger('parcels_api_get')
    try:
        s = ScenarioService.get(scenario_id)
        if not s:
            raise ApiException("Unknown Scenario")
        p = ParcelService.get_all(scenario_id=scenario_id)
        m = LAND_USE_TYPES
        parcels = []
        media = m

        if p is not None:
            start_time_s = time.time()
            sh = s.as_serializable()
            logger.info(f"Acquired scenario {s.name} in {time.time() - start_time_s} seconds")
            total_start = time.time()
            for this_p in p:
                start_time = time.time()
                parcels.append(this_p.as_serializable())
                logger.info(f"Acquired parcel {this_p.name} in {time.time() - start_time} seconds")
            logger.info(f"Acquired all parcels in {time.time() - total_start} seconds")
    except Exception as e:
        logger.error(traceback.format_exc())

    return ApiResult({
        'parcels': parcels,
        'media': media
    })


@parcels_api.route(
    '/api/scenario/<int:scenario_id>/parcel/<int:id>/update', methods=['POST']
)
@login_required
def update_parcel(id, scenario_id):
    logger = make_logger('parcels_api_update')

    try:
        # Get the specified parcel
        p = ParcelService.get(id)
        parcels_data = request.form.to_dict()
        print(f"updating with {parcels_data}")
        rv = None
        try:
            rv = handle_parcel_update(p, parcels_data)
        except Exception as e:
            print(f"exception while updating parcel {p} with {parcels_data}: {e}")

        if rv is not None:
            return rv
    except Exception as e:
        logger.error(traceback.format_exc())
    return ApiResult({'message': 'success'})


@parcels_api.route('/api/scenario/<int:scenario_id>/parcel/<int:id>/delete', methods=['POST'])
@login_required
def delete_parcel(id, scenario_id):
    logger = make_logger('parcels_api_delete')
    try:
        p = ParcelService.get(id)
        # Delete Contents
        delete_parcel_contents(p)

        # Delete the specified parcel
        p = ParcelService.delete(id, no_commit=True)

        # Save the scenario
        ParcelService.commit()
    except Exception as e:
        logger.error(traceback.format_exc())

    return "success"




