import os
import pandas as pd
import traceback
from flask import Blueprint, request
from flask_security import login_required
from werkzeug.utils import secure_filename
from custom.flask_api import ApiException, ApiResult
from trim_frontend import api
from ..utils.file_io import csv_to_df
from ..utils.forms import assemble_json_form
from ..utils.logging import make_logger


file_api = Blueprint('file_api', __name__)
api.use_api_errors(file_api)


@file_api.route('/api/file', methods=['POST'])
@login_required
def parse():
    logger = make_logger('file_uploader')

    files = request.files
    if not files:
        raise ApiException("No files were uploaded")

    data = {}
    for n, f in files.items():
        err = None
        fields = []
        entries = 0
        preview = None
        try:
            fname = secure_filename(f.filename)

            if fname.endswith('.csv'):
                df = csv_to_df(f, dtype=str)
                # Get rid of carriage returns b/c they mess up output
                df = df.replace('\r', '', regex=True)

                fields = list(df.columns.values)
                entries = len(df.index)
                preview = df.head().where(
                    pd.notnull(df), None
                ).to_dict('records')

        except Exception as e:
            logger.error(traceback.format_exc())
            err = e

        if err:
            raise ApiException(
                f"Unable to upload file: {err}", 500
            ) from err

        data[n] = {
            'filename': fname,
            'fields': fields,
            'entry_count': entries,
            'preview': preview
        }

    return ApiResult({'files': data})


root = os.path.dirname(os.path.abspath(__file__))
static = os.path.abspath(os.path.join(root, '../static'))


@file_api.route('/api/form', methods=['GET'])
@login_required
def load_json_form():
    forms = request.args.getlist('form')

    json_forms = {}

    for form in forms:
        json_forms[form] = None
        name = form
        if not name.endswith('.json'):
            name += '.json'
        json_forms[form] = assemble_json_form(name)

    return ApiResult(json_forms)
