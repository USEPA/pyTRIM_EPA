BEGIN TRANSACTION;

-- Remove HHRAP parameters that conflict with RTR
DELETE FROM mirc_parameter
WHERE scenario_id = 1
AND CONCAT(
	variable, '-', chemical_id, '-', media_id, '-', food_id, '-', life_stage_id, '-', percentile_id
) IN (
	SELECT CONCAT(
		variable, '-', chemical_id, '-', media_id, '-', food_id, '-', life_stage_id, '-', percentile_id
	)
	FROM mirc_parameter
	WHERE scenario_id = 2
);

-- Rename HHRAP to RTR
UPDATE mirc_scenario SET name = 'RTR Site-Specific' WHERE id = 1;

-- Swap scenarios/simulations/parameters that pointed at old RTR to point to new RTR (= old HHRAP)
UPDATE mirc_scenario SET parent_id = 1 WHERE parent_id = 2;
UPDATE mirc_simulation SET mirc_scenario_id = 1 WHERE mirc_scenario_id = 2;
UPDATE mirc_parameter SET scenario_id = 1 WHERE scenario_id = 2;

-- Remove any permissions that pointed to old RTR
DELETE FROM mirc_scenario_permissions WHERE mirc_scenario_id = 2;

-- Remove old RTR
DELETE FROM mirc_scenario WHERE id = 2;

COMMIT;
