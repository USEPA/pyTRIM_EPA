from flask import Blueprint, redirect, url_for, render_template
from flask_security import current_user


base = Blueprint('base', __name__)


@base.route('/', methods=['GET'])
def index():
    import os, json, boto3
    def get_client_secret(secret_id):
        # TESTING ACCESS DMAP SECRETS MANAGER
        if not secret_id:
            return None
        secrets_client = boto3.client('secretsmanager')
        response = secrets_client.get_secret_value(
            SecretId=secret_id
        )
        try:
            secret_data = json.loads(response['SecretString'])
        except:
            secret_data = response['SecretString']
        return secret_data['client_secret']

    try:
        return get_client_secret(os.getenv('LOGIN_GOV_SECRET_ARN')) or "None!"
    except Exception as e:
        return e

    scenarios = []
    if current_user.is_authenticated:
        return redirect(url_for('scenario.view_scenarios'))
    return render_template('base/index.html', scenarios=scenarios)
