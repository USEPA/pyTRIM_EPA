BEGIN TRANSACTION;

DELETE FROM mirc_parameter_toxicity;
DELETE FROM mirc_parameter;
DELETE FROM mirc_simulation_consumption_breakdown;
DELETE FROM mirc_simulation_parameter;
DELETE FROM mirc_simulation_percentile;
DELETE FROM mirc_simulation;
DELETE FROM mirc_scenario WHERE NOT(is_builtin);

COMMIT;

