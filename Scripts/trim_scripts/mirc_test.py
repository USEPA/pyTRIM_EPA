from base import *

from trim_frontend.mirc.simulations.utils import make_report

trim_scenario_id = 15  # Foundries_SS_V#4
simulation_id = 46  # (2) Divalent Mercury Simulation (CAS 14302-87-5)

trim_scenario = ScenarioService.get(trim_scenario_id)
simulation = [s for s in trim_scenario.mirc_simulations if s.id == simulation_id]
simulation = simulation[0]

s = simulation.as_serializable()
other_parameters = [p.as_serializable() for p in (simulation.parameters + simulation.consumption_breakdowns)]

results = MircSimulationService(simulation).run_pathways()
report = make_report(results)

print("!")
