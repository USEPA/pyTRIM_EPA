import os
from flask_wtf import FlaskForm
from ..utils.forms import json_form


__all__ = [
    'ScenarioParcelsForm'
]


root = os.path.dirname(os.path.abspath(__file__))
forms = os.path.abspath(os.path.join(root, '../static/forms'))


@json_form(os.path.abspath(
    f'{forms}/scenario_parcels_form.json'
))
class ScenarioParcelsForm(FlaskForm):
    pass

