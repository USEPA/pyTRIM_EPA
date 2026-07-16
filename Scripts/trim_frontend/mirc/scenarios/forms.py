import os
from flask_wtf import FlaskForm
from ...utils.forms import json_form


__all__ = [
    'MircScenarioForm'
]


root = os.path.dirname(os.path.abspath(__file__))
forms = os.path.abspath(os.path.join(root, '../../static/forms/mirc'))


@json_form(os.path.abspath(f'{forms}/risk_scenario.json'))
class MircScenarioForm(FlaskForm):
    pass
