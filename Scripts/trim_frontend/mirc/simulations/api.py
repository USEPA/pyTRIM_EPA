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

    simulations = MircSimulationService.from_form(trim_scenario, form)
    db.session.commit()

    MircSimulationService.update_simulation_names(trim_scenario)  # make sure numbering is correct

    if len(simulations) == 1:
        return {'simulation_id': simulations[0].id}
    else:
        return {'simulation_ids': [s.id for s in simulations]}


@mirc_simulation_api.route(
    '/api/scenario/<int:trim_scenario_id>/mirc/simulation'
)
@login_required
def get_simulations(trim_scenario_id):
    trim_scenario = ScenarioService.get(trim_scenario_id)
    if not current_user.can('view', trim_scenario):
        abort(403)

    return api.Result({
        'simulations': [s.as_serializable() for s in trim_scenario.mirc_simulations]
    })


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

    try:
        results = MircSimulationService(simulation).run_pathways()
    except Exception:
        import traceback
        traceback.print_exc()
        raise

    f = request.args.get('format', 'json')
    if f == 'xlsx':
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                report = make_report(results)
            except Exception:
                import traceback
                traceback.print_exc()
                raise

            if not isinstance(report, list):
                report = [report]

            n = f'{trim_scenario.name}_{simulation.name}.xlsx'.replace(' ', '_')
            filepath = os.path.join(tmpdir, n)
            with pd.ExcelWriter(filepath) as writer:
                for i, df in enumerate(report, start=1):
                    df.to_excel(writer, sheet_name=f'Sheet{i}', index=False)

            return api.FileResult(filepath)
    else:
        from trim_db.schema.utils.serialize import serialize
        return serialize(results)


@mirc_simulation_api.route(
    '/api/scenario/<int:trim_scenario_id>/mirc/simulation/<int:id>', methods=['DELETE']
)
@login_required
def delete_simulation(trim_scenario_id, id):
    trim_scenario = ScenarioService.get(trim_scenario_id)
    if not current_user.can('view', trim_scenario):
        abort(403)

    simulation = MircSimulationService.get(id)
    if not simulation:
        return api.Result({
            'success': True
        })

    MircSimulationService.delete(simulation)
    MircSimulationService.update_simulation_names(trim_scenario)  # make sure numbering is correct

    return api.Result({
        'success': True
    })
