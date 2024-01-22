import os
from flask_wtf import FlaskForm
from ..utils.forms import json_form


__all__ = [
    'ScenarioDefinitionForm', 'ScenarioInfoForm',
    'ScenarioMeteorologicalSettingsForm',
    'ScenarioSeasonalDynamicsForm', 'ScenarioAbioticPropertiesForm',
    'ScenarioEmissionsForm', 'ScenarioErosionForm',
    'ScenarioExportSettingsForm'
]


root = os.path.dirname(os.path.abspath(__file__))
forms = os.path.abspath(os.path.join(root, '../static/forms'))


@json_form(os.path.abspath(
    f'{forms}/scenario_definition_form.json'
))
class ScenarioDefinitionForm(FlaskForm):
    pass


@json_form(os.path.abspath(
    f'{forms}/scenario_info_form.json'
))
class ScenarioInfoForm(FlaskForm):
    pass


@json_form(os.path.abspath(
    f'{forms}/scenario_exports_form.json'
))
class ScenarioExportSettingsForm(FlaskForm):
    pass


@json_form(os.path.abspath(
    f'{forms}/scenario_meteorology_form.json'
))
class ScenarioMeteorologicalSettingsForm(FlaskForm):
    pass


@json_form(os.path.abspath(
    f'{forms}/scenario_abiotic_props_form.json'
))
class ScenarioAbioticPropertiesForm(FlaskForm):
    pass


@json_form(os.path.abspath(
    f'{forms}/scenario_seasonal_dynamics_form.json'
))
class ScenarioSeasonalDynamicsForm(FlaskForm):
    pass


@json_form(os.path.abspath(
    f'{forms}/scenario_erosion_form.json'
))
class ScenarioErosionForm(FlaskForm):
    pass


@json_form(os.path.abspath(
    f'{forms}/scenario_emissions_form.json'
))
class ScenarioEmissionsForm(FlaskForm):
    pass
