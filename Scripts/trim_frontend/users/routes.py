from flask import Blueprint, redirect, url_for
from flask_security import current_user
from flask_wtf.csrf import generate_csrf
from trim_frontend import api


auth = Blueprint('auth', __name__)
api.use_api_errors(auth)


@auth.route('/auth/check_csrf', methods=['POST'])
def check_token():
    if not current_user.is_authenticated:
        raise api.Exception("Access denied", 404)

    return api.Result("Valid token")


@auth.route('/auth/get_csrf', methods=['GET'])
def get_token():
    if not current_user.is_authenticated:
        raise api.Exception("Access denied", 404)

    return api.Result({'token': generate_csrf()})
