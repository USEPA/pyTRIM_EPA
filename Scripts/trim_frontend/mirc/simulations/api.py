import os
import pandas as pd
import tempfile
from flask import request, abort
from flask_security import login_required, current_user
from werkzeug.datastructures import MultiDict
from trim_db.services import ScenarioService, MircSimulationService
from trim_frontend import api, db
from .forms import MircSimulationForm as SimulationForm
from .utils import make_report


mirc_simulation_api = api.Blueprint('mirc_simulation_api', __name__)


@mirc_simulation_api.route(
    '/api/scenario/<int:trim_scenario_id>/mirc/simulation/', methods=['POST']
)
@login_required
@api.csrf_exempt
def create_simulation(trim_scenario_id):
    trim_scenario = ScenarioService.get(trim_scenario_id)
    if not current_user.can('view', trim_scenario):
        abort(403)

    try:
        form = SimulationForm(
            formdata=MultiDict(dict(request.json))
        )
    except Exception:
        form = SimulationForm()

    sim = MircSimulationService.from_form(trim_scenario, form)
    db.session.commit()

    return {
        "simulation_id": sim.id
    }


@mirc_simulation_api.route(
    '/api/scenario/<int:trim_scenario_id>/mirc/simulation/<int:simulation_id>'
)
@login_required
def get_results(trim_scenario_id, simulation_id):
    trim_scenario = ScenarioService.get(trim_scenario_id)
    if not current_user.can('view', trim_scenario):
        abort(403)

    simulation = [
        s for s in trim_scenario.mirc_simulations if s.id == simulation_id
    ]

    if not simulation:
        raise Exception('The requested simulation does not exist')

    simulation = simulation[0]

    results = MircSimulationService(simulation).run_pathways()

    f = request.args.get('format', 'json')
    if f == 'xlsx':
        with tempfile.TemporaryDirectory() as tmpdir:
            report = make_report(results)

            if not isinstance(report, list):
                report = [report]

            n = f'{trim_scenario.name}_{simulation.name}.xlsx'.replace(' ', '_')
            filepath = os.path.join(tmpdir, n)
            with pd.ExcelWriter(filepath) as writer:
                for i, df in enumerate(report, start=1):
                    df.to_excel(writer, sheet_name=f'Sheet{i}', index=False)

            return filepath
    else:
        from trim_db.schema.utils.serialize import serialize
        return serialize(results)
