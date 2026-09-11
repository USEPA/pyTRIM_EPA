BEGIN TRANSACTION;
-- Extracting RTR Screening

-- Inherits from RTR Site-Specific
INSERT INTO mirc_scenario (name, is_builtin, notes, parent_id)
VALUES ('RTR Screening', true, NULL, 1);

-- Parameters
-- TODO update scenario_id based on mirc_scenario insert
INSERT INTO mirc_parameter(scenario_id,name,variable,value,unit,source,notes,chemical_id,media_id,food_id,life_stage_id,percentile_id,id) VALUES (8,'cancer slope factor','CSF',150.0,'(mg/kg/day)^-1',NULL,NULL,1,NULL,NULL,NULL,NULL,2692);
INSERT INTO mirc_parameter(scenario_id,name,variable,value,unit,source,notes,chemical_id,media_id,food_id,life_stage_id,percentile_id,id) VALUES (8,'reference dose','RfD',7e-07,'mg/kg/day',NULL,NULL,1,NULL,NULL,NULL,NULL,2702);
INSERT INTO mirc_parameter(scenario_id,name,variable,value,unit,source,notes,chemical_id,media_id,food_id,life_stage_id,percentile_id,id) VALUES (8,'cancer slope factor','CSF',300.0,'(mg/kg/day)^-1',NULL,NULL,2,NULL,NULL,NULL,NULL,2693);
INSERT INTO mirc_parameter(scenario_id,name,variable,value,unit,source,notes,chemical_id,media_id,food_id,life_stage_id,percentile_id,id) VALUES (8,'reference dose','RfD',3.5e-07,'mg/kg/day',NULL,NULL,2,NULL,NULL,NULL,NULL,2703);
INSERT INTO mirc_parameter(scenario_id,name,variable,value,unit,source,notes,chemical_id,media_id,food_id,life_stage_id,percentile_id,id) VALUES (8,'cancer slope factor','CSF',7500.0,'(mg/kg/day)^-1',NULL,NULL,3,NULL,NULL,NULL,NULL,2679);
INSERT INTO mirc_parameter(scenario_id,name,variable,value,unit,source,notes,chemical_id,media_id,food_id,life_stage_id,percentile_id,id) VALUES (8,'reference dose','RfD',1.4e-08,'mg/kg/day',NULL,NULL,3,NULL,NULL,NULL,NULL,2680);
INSERT INTO mirc_parameter(scenario_id,name,variable,value,unit,source,notes,chemical_id,media_id,food_id,life_stage_id,percentile_id,id) VALUES (8,'cancer slope factor','CSF',3000.0,'(mg/kg/day)^-1',NULL,NULL,4,NULL,NULL,NULL,NULL,2681);
INSERT INTO mirc_parameter(scenario_id,name,variable,value,unit,source,notes,chemical_id,media_id,food_id,life_stage_id,percentile_id,id) VALUES (8,'reference dose','RfD',3.5e-08,'mg/kg/day',NULL,NULL,4,NULL,NULL,NULL,NULL,2682);
INSERT INTO mirc_parameter(scenario_id,name,variable,value,unit,source,notes,chemical_id,media_id,food_id,life_stage_id,percentile_id,id) VALUES (8,'cancer slope factor','CSF',15000.0,'(mg/kg/day)^-1',NULL,NULL,5,NULL,NULL,NULL,NULL,2683);
INSERT INTO mirc_parameter(scenario_id,name,variable,value,unit,source,notes,chemical_id,media_id,food_id,life_stage_id,percentile_id,id) VALUES (8,'reference dose','RfD',7e-09,'mg/kg/day',NULL,NULL,5,NULL,NULL,NULL,NULL,2704);
INSERT INTO mirc_parameter(scenario_id,name,variable,value,unit,source,notes,chemical_id,media_id,food_id,life_stage_id,percentile_id,id) VALUES (8,'cancer slope factor','CSF',14000.0,'(mg/kg/day)^-1',NULL,NULL,6,NULL,NULL,NULL,NULL,2684);
INSERT INTO mirc_parameter(scenario_id,name,variable,value,unit,source,notes,chemical_id,media_id,food_id,life_stage_id,percentile_id,id) VALUES (8,'reference dose','RfD',7.8e-09,'mg/kg/day',NULL,NULL,6,NULL,NULL,NULL,NULL,2685);
INSERT INTO mirc_parameter(scenario_id,name,variable,value,unit,source,notes,chemical_id,media_id,food_id,life_stage_id,percentile_id,id) VALUES (8,'cancer slope factor','CSF',45000.0,'(mg/kg/day)^-1',NULL,NULL,7,NULL,NULL,NULL,NULL,2686);
INSERT INTO mirc_parameter(scenario_id,name,variable,value,unit,source,notes,chemical_id,media_id,food_id,life_stage_id,percentile_id,id) VALUES (8,'reference dose','RfD',2.3e-09,'mg/kg/day',NULL,NULL,7,NULL,NULL,NULL,NULL,2687);
INSERT INTO mirc_parameter(scenario_id,name,variable,value,unit,source,notes,chemical_id,media_id,food_id,life_stage_id,percentile_id,id) VALUES (8,'cancer slope factor','CSF',14000.0,'(mg/kg/day)^-1',NULL,NULL,9,NULL,NULL,NULL,NULL,2688);
INSERT INTO mirc_parameter(scenario_id,name,variable,value,unit,source,notes,chemical_id,media_id,food_id,life_stage_id,percentile_id,id) VALUES (8,'reference dose','RfD',7.8e-09,'mg/kg/day',NULL,NULL,9,NULL,NULL,NULL,NULL,2689);
INSERT INTO mirc_parameter(scenario_id,name,variable,value,unit,source,notes,chemical_id,media_id,food_id,life_stage_id,percentile_id,id) VALUES (8,'cancer slope factor','CSF',30000.0,'(mg/kg/day)^-1',NULL,NULL,11,NULL,NULL,NULL,NULL,2690);
INSERT INTO mirc_parameter(scenario_id,name,variable,value,unit,source,notes,chemical_id,media_id,food_id,life_stage_id,percentile_id,id) VALUES (8,'reference dose','RfD',3.5e-09,'mg/kg/day',NULL,NULL,11,NULL,NULL,NULL,NULL,2691);
INSERT INTO mirc_parameter(scenario_id,name,variable,value,unit,source,notes,chemical_id,media_id,food_id,life_stage_id,percentile_id,id) VALUES (8,'cancer slope factor','CSF',60000.0,'(mg/kg/day)^-1',NULL,NULL,12,NULL,NULL,NULL,NULL,2694);
INSERT INTO mirc_parameter(scenario_id,name,variable,value,unit,source,notes,chemical_id,media_id,food_id,life_stage_id,percentile_id,id) VALUES (8,'reference dose','RfD',1.8e-09,'mg/kg/day',NULL,NULL,12,NULL,NULL,NULL,NULL,2695);
INSERT INTO mirc_parameter(scenario_id,name,variable,value,unit,source,notes,chemical_id,media_id,food_id,life_stage_id,percentile_id,id) VALUES (8,'cancer slope factor','CSF',1500.0,'(mg/kg/day)^-1',NULL,NULL,13,NULL,NULL,NULL,NULL,2696);
INSERT INTO mirc_parameter(scenario_id,name,variable,value,unit,source,notes,chemical_id,media_id,food_id,life_stage_id,percentile_id,id) VALUES (8,'reference dose','RfD',7e-08,'mg/kg/day',NULL,NULL,13,NULL,NULL,NULL,NULL,2697);
INSERT INTO mirc_parameter(scenario_id,name,variable,value,unit,source,notes,chemical_id,media_id,food_id,life_stage_id,percentile_id,id) VALUES (8,'cancer slope factor','CSF',15000.0,'(mg/kg/day)^-1',NULL,NULL,15,NULL,NULL,NULL,NULL,2698);
INSERT INTO mirc_parameter(scenario_id,name,variable,value,unit,source,notes,chemical_id,media_id,food_id,life_stage_id,percentile_id,id) VALUES (8,'reference dose','RfD',7e-09,'mg/kg/day',NULL,NULL,15,NULL,NULL,NULL,NULL,2699);
INSERT INTO mirc_parameter(scenario_id,name,variable,value,unit,source,notes,chemical_id,media_id,food_id,life_stage_id,percentile_id,id) VALUES (8,'cancer slope factor','CSF',11000.0,'(mg/kg/day)^-1',NULL,NULL,17,NULL,NULL,NULL,NULL,2700);
INSERT INTO mirc_parameter(scenario_id,name,variable,value,unit,source,notes,chemical_id,media_id,food_id,life_stage_id,percentile_id,id) VALUES (8,'reference dose','RfD',1e-08,'mg/kg/day',NULL,NULL,17,NULL,NULL,NULL,NULL,2701);

COMMIT;