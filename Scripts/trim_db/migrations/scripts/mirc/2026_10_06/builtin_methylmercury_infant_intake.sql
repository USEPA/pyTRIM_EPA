BEGIN TRANSACTION;

DO $$
DECLARE
    rtr_screening_id INT;
    rtr_site_specific_id INT;
    methyl_mercury_id INT;
    breast_milk_id INT;
BEGIN
    rtr_screening_id := (SELECT id FROM mirc_scenario WHERE name='RTR Screening' AND is_builtin=true);
    rtr_site_specific_id := (SELECT id FROM mirc_scenario WHERE name='RTR Site-Specific' AND is_builtin=true);
    methyl_mercury_id := (SELECT id FROM chemical WHERE name='MethylMercury');
    breast_milk_id := (SELECT id FROM mirc_product WHERE name='breast milk');

    INSERT INTO mirc_parameter (scenario_id, name, variable, value, unit, source, notes, chemical_id, media_id, food_id, life_stage_id, percentile_id)
    VALUES
        (rtr_screening_id,'set infant add equal to adult ladd','infant_add_equals_adult_lifetime',1,NULL,NULL,NULL,methyl_mercury_id,breast_milk_id,NULL,NULL,NULL),
        (rtr_screening_id,'set infant add equal to adult ladd','infant_add_equals_adult_lifetime',1,NULL,NULL,NULL,methyl_mercury_id,breast_milk_id,NULL,NULL,NULL),
        (rtr_site_specific_id,'set infant add equal to adult ladd','infant_add_equals_adult_lifetime',1,NULL,NULL,NULL,methyl_mercury_id,breast_milk_id,NULL,NULL,NULL),
        (rtr_site_specific_id,'set infant add equal to adult ladd','infant_add_equals_adult_lifetime',1,NULL,NULL,NULL,methyl_mercury_id,breast_milk_id,NULL,NULL,NULL);

END $$;

COMMIT;