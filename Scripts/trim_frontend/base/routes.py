from flask import Blueprint, redirect, url_for, render_template
from flask_security import current_user


base = Blueprint('base', __name__)


@base.route('/', methods=['GET'])
def index():
    scenarios = []
    if current_user.is_authenticated:
        return redirect(url_for('scenario.view_scenarios'))
    return render_template('base/index.html', scenarios=scenarios)
