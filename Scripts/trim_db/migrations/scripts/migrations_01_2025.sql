UPDATE pytrim.formula t SET t.equation = '((environment.FractionInitialConcentrations * self.initialConcentration(chemical).to("g / m^3")) if self.media.id in {2 , 5 , 7 , 56 , 55 , 8 , 9} else ((environment.FractionInitialConcentrations * self.initialConcentration(chemical).to("g / kg")) if self.media.id in {23 , 24 , 27 , 28 , 29 , 31 , 32 , 33 , 37 , 39 , 41 , 43 , 44 , 45 , 46 , 47 , 48 , 49 , 50 , 51} else (environment.FractionInitialConcentrations * self.initialConcentration(chemical).to("g / L")) if self.media.id in {10 , 4} else 0)))' WHERE t.id = 2338;

DELETE from custom_parameter where definition_id = 479;

UPDATE pytrim.parameter_definition t SET t.full_name = 'initialConcentrationConverted' WHERE t.id = 479;
UPDATE pytrim.parameter_definition t SET t.variable_name = 'initialConcentrationConverted' WHERE t.id = 479;
UPDATE pytrim.parameter_definition t SET t.domain_id = 3 WHERE t.id = 479;

INSERT INTO pytrim.parameter_definition (variable_name, full_name, description, domain_id, default_value, default_unit, default_formula_id) VALUES ('FractionInitialConcentrations', 'FractionInitialConcentrations', null, 1, 0.000000000000000, null, null);

INSERT INTO pytrim.formula (equation, description) VALUES ('0.0 if chemical.id == 31 else 0.0 if chemical.id == 32 else 0.0 if chemical.id == 37 else 0', null);

SET @last_id_formula = LAST_INSERT_ID();

INSERT INTO pytrim.parameter_definition (variable_name, full_name, description, domain_id, default_value, default_unit, default_formula_id) VALUES ('initialConcentration', 'initialConcentration', null, 3, null, 'g/kg', @last_id_formula);

INSERT INTO pytrim.formula_argument (formula_id, name, domain_id) VALUES (@last_id_formula, "chemical", 2);

Update formula set equation=Replace(equation, 'self.initialConcentration(compartment).to("g / m^3")) if compartment.media.id in', 'self.initialConcentration(chemical).to("g / m^3")) if self.media.id in') WHERE equation like ('%self.initialConcentration(compartment)%');

Update formula set equation=Replace(equation, 'self.initialConcentration(compartment).to("g / kg")) if compartment.media.id in', 'self.initialConcentration(chemical).to("g / kg")) if self.media.id in') WHERE equation like ('%self.initialConcentration(compartment)%');

Update formula set equation=Replace(equation, 'self.initialConcentration(compartment).to("g / L")) if compartment.media.id in', 'self.initialConcentration(chemical).to("g / L")) if self.media.id in') WHERE equation like ('%self.initialConcentration(compartment)%');

UPDATE formula_argument as fa INNER JOIN formula as f ON fa.formula_id = f.id SET fa.domain_id = 3 WHERE f.equation like ('%self.initialConcentration%') AND fa.name = 'self';

UPDATE formula_argument as fa INNER JOIN formula as f ON fa.formula_id = f.id SET fa.domain_id = 2, fa.name = 'chemical' WHERE f.equation like ('%self.initialConcentration%') AND fa.name = 'compartment';

UPDATE formula as t SET t.equation = '((self.VolumeFraction_Liquid(compartment) / compartment.VolumeFraction_LiquidColloid * self.Z_Liquid(compartment) + compartment.VolumeFraction_Colloid / compartment.VolumeFraction_LiquidColloid * self.Z_Colloid(compartment)) if compartment.media.id in {8 , 7 , 56 , 55} else 0)' WHERE t.id = 2364;

UPDATE pytrim.transport_process t SET t.requirements = '(sender.media.isa("Abiotic|Soil|Surface_Soil")) and (receiver.media.isa("Abiotic|Water|Surface_Water")) and ((sender.is_next_to(receiver)) or (receiver in sender.custom_linked_compartments))' WHERE t.id = 77;

INSERT INTO pytrim.formula (equation, description) VALUES ('self.FractionOfTotalRunoff(receiver)', null);
SET @last_id_formula = LAST_INSERT_ID();
INSERT INTO pytrim.formula_argument (formula_id, name, domain_id) VALUES (@last_id_formula, "receiver”, 3);
INSERT INTO pytrim.formula_argument (formula_id, name, domain_id) VALUES (@last_id_formula, “self”, 28);
UPDATE parameter_definition t SET t.default_formula_id = @last_id_formula WHERE t.variable_name = ‘FractionOfTotalErosion’ and t.domain_id = 28;

INSERT INTO pytrim.formula (equation, description) VALUES ('self.FractionOfTotalRunoff(receiver)', null);
SET @last_id_formula = LAST_INSERT_ID();
INSERT INTO pytrim.formula_argument (formula_id, name, domain_id) VALUES (@last_id_formula, "receiver”, 3);
INSERT INTO pytrim.formula_argument (formula_id, name, domain_id) VALUES (@last_id_formula, “self”, 39);
UPDATE parameter_definition t SET t.default_formula_id = @last_id_formula WHERE t.variable_name = ‘FractionOfTotalErosion’ and t.domain_id = 39;

INSERT INTO pytrim.formula (equation, description) VALUES ('self.FractionOfTotalRunoff(receiver)', null);
SET @last_id_formula = LAST_INSERT_ID();
INSERT INTO pytrim.formula_argument (formula_id, name, domain_id) VALUES (@last_id_formula, "receiver”, 3);
INSERT INTO pytrim.formula_argument (formula_id, name, domain_id) VALUES (@last_id_formula, “self”, 40);
UPDATE parameter_definition t SET t.default_formula_id = @last_id_formula WHERE t.variable_name = ‘FractionOfTotalErosion’ and t.domain_id = 40;
