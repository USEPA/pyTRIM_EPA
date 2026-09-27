BEGIN TRANSACTION;

-- Adding an 'active' column to Chemical
ALTER TABLE chemical
ADD COLUMN active BOOLEAN NOT NULL DEFAULT true;

UPDATE chemical SET active=false WHERE name='Lead';

-- Updating the human-readable variable name
UPDATE mirc_simulation_parameter
SET name='Average Concentration where Produce Root Uptake Occurs (mg/kg)'
WHERE variable='C_root_veg';

UPDATE mirc_simulation_parameter
SET name='Average Concentration where Livestock Feed Root Uptake Occurs (mg/kg)'
WHERE variable='Cs_root_zone';

-- Adding columns to mirc_simulation_consumption_breakdown
ALTER TABLE mirc_simulation_consumption_breakdown
ADD COLUMN variable VARCHAR(60),
ADD COLUMN name VARCHAR(255);


-- Not MIRC but here it is!
-- WaterTemperature (K) was being stored using the parameter definition for WaterTemperature (C)
INSERT INTO parameter_definition (variable_name, full_name, domain_id, default_value, default_unit)
VALUES (
   'WaterTemperature', 
   'WaterTemperature',
   (select id from parameter_domain where name = 'Compartment [Surface_Water]'), 
   298, 
   'K'
);

-- Flush rate auto calc fix
UPDATE parameter_definition set default_formula_id = NULL where default_formula_id = (
	SELECT id FROM formula WHERE description= 'flush rate is autocalculated'
);
UPDATE custom_parameter set formula_id = NULL where formula_id = (
	SELECT id FROM formula WHERE description= 'flush rate is autocalculated'
);
DELETE from formula_argument where formula_id=(
	SELECT id FROM formula WHERE description= 'flush rate is autocalculated'
);
DELETE FROM formula WHERE description= 'flush rate is autocalculated';

-- Air concentration equation might've gotten messed up
UPDATE formula SET equation='0 if chemical.id == 28 else 0' WHERE id = (
	SELECT formula.id FROM parameter_definition 
	JOIN formula ON parameter_definition.default_formula_id=formula.id
	WHERE variable_name='aermodAirConcentration'
);

COMMIT;
