from flask import Blueprint
from flask_security import login_required
from flask_api import ApiResult,  ApiException
from trim_db.services import ChemicalService
from trim_frontend import api

chemicals_api = Blueprint('chemicals_api', __name__)
api.use_api_errors(chemicals_api)


@chemicals_api.route(
    '/api/chemicals/', methods=['GET']
)
@login_required
def get_chemicals():
    chems = [c.as_serializable() for c in ChemicalService.get_all()]
    return ApiResult({
        'chemicals': chems
    })
