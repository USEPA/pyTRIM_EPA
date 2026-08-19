
SELECT setval('mirc_scenario_id_seq', (SELECT MAX(id) FROM "mirc_scenario"));
SELECT setval('mirc_product_id_seq', (SELECT MAX(id) FROM "mirc_product"));
SELECT setval('mirc_percentile_id_seq', (SELECT MAX(id) FROM "mirc_percentile"));
SELECT setval('mirc_life_stage_id_seq', (SELECT MAX(id) FROM "mirc_life_stage"));
SELECT setval('mirc_parameter_id_seq', (SELECT MAX(id) FROM "mirc_parameter"));
SELECT setval('mirc_simulation_id_seq', (SELECT MAX(id) FROM "mirc_simulation"));
