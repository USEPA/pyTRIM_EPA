BEGIN TRANSACTION;

-- Dairy Ingestion Rates

UPDATE mirc_parameter SET value = 7.25
WHERE scenario_id = 1 AND variable = 'IR' AND (
    media_id IS NULL -- human
    AND life_stage_id = 6 -- adult
    AND percentile_id = 7 -- Pmean
    AND food_id = 17 -- dairy
);

UPDATE mirc_parameter SET value = 7.52
WHERE scenario_id = 1 AND variable = 'IR' AND (
    media_id IS NULL -- human
    AND life_stage_id = 6 -- adult
    AND percentile_id = 3 -- P50
    AND food_id = 17 -- dairy
);

UPDATE mirc_parameter SET value = 17.64
WHERE scenario_id = 1 AND variable = 'IR' AND (
    media_id IS NULL -- human
    AND life_stage_id = 6 -- adult
    AND percentile_id = 5 -- P95
    AND food_id = 17 -- dairy
);

UPDATE mirc_parameter SET value = 20.89
WHERE scenario_id = 1 AND variable = 'IR' AND (
    media_id IS NULL -- human
    AND life_stage_id = 6 -- adult
    AND percentile_id = 6 -- P99
    AND food_id = 17 -- dairy
);


-- Methyl Mercury - Breast Milk parameters

-- chemical_id 37 == Methyl Mercury
-- media_id 30 == Breast Milk
INSERT INTO mirc_parameter (scenario_id, name, variable, value, unit, chemical_id, media_id)
VALUES
    (1, 'infant absorption efficiency', 'AE_inf', 1, NULL, 37, 30),
    (1, 'maternal absorption efficiency', 'AE_mat', 1, NULL, 37, 30),
    (1, 'fraction in maternal blood', 'f_bl', 0.059, NULL, 37, 30),
    (1, 'half life', 'h_bm', 50, 'day', 37, 30),
    (1, 'non-lactating elimination rate constant', 'k_elim', 0.014, 'day^-1', 37, 30),
    (1, 'lactating elimination rate constant', 'k_aq_elac', 0.014, 'day^-1', 37, 30),
    (1, 'blood-milk partition coefficient', 'PC_pl_aq', 1, 'g/g', 37, 30),
    (1, 'blood cell-plasma partition coefficient', 'PC_rbc_pl', 40, 'mL/mL', 37, 30);


-- Divalent Mercury parameters

-- chemical_id 31 == Divalent Mercury

INSERT INTO mirc_parameter (scenario_id, name, variable, value, unit, chemical_id, media_id)
VALUES
    -- general parameters

    (1, 'fraction wet deposition', 'Fw', 0.6, NULL, 31, NULL),
    (1, 'soil bioavailability factor', 'SoilAdjFactor', 1, NULL, 31, NULL),
    (1, 'reference dose', 'RfD', 0.0003, 'mg/kg/day', 31, NULL),

    -- plant-specific parameters

    -- * media_id 11 == Exposed Fruit
    (1, 'air-plant biotransfer factor', 'Bv_ag', 1800, NULL, 31, 11),
    (1, 'plant-soil bioconcentration factor', 'Br', 0.015, NULL, 31, 11),
    (1, 'empirical correction factor', 'VG', 1, NULL, 31, 11),

    -- * media_id 10 == Exposed Vegetable
    (1, 'air-plant biotransfer factor', 'Bv_ag', 1800, NULL, 31, 10),
    (1, 'plant-soil bioconcentration factor', 'Br', 0.015, NULL, 31, 10),
    (1, 'empirical correction factor', 'VG', 1, NULL, 31, 10),

    -- * media_id 12 == Forage
    (1, 'air-plant biotransfer factor', 'Bv_ag', 1800, NULL, 31, 12),
    (1, 'empirical correction factor', 'VG', 1, NULL, 31, 12),

    -- * media_id 8 == Grain
    (1, 'air-plant biotransfer factor', 'Bv_ag', 1800, NULL, 31, 8),
    (1, 'plant-soil bioconcentration factor', 'Br', 0.0093, NULL, 31, 8),

    -- * media_id 6 == Protected Fruit
    (1, 'air-plant biotransfer factor', 'Bv_ag', 1800, NULL, 31, 6),
    (1, 'plant-soil bioconcentration factor', 'Br', 0.015, NULL, 31, 6),

    -- * media_id 5 == Protected Vegetable
    (1, 'air-plant biotransfer factor', 'Bv_ag', 1800, NULL, 31, 5),
    (1, 'plant-soil bioconcentration factor', 'Br', 0.015, NULL, 31, 5),

    -- * media_id 7 == Root
    (1, 'air-plant biotransfer factor', 'Bv_ag', 1800, NULL, 31, 7),
    (1, 'plant-soil bioconcentration factor', 'Br', 0.036, NULL, 31, 7),
    (1, 'empirical correction factor', 'VG', 1, NULL, 31, 7),

    -- * media_id 13 == Silage
    (1, 'air-plant biotransfer factor', 'Bv_ag', 1800, NULL, 31, 13),
    (1, 'empirical correction factor', 'VG', 0.5, NULL, 31, 13),

    -- animal-specific parameters

    -- * media_id 16 == Beef
    (1, 'biotransfer factor', 'Ba', 0.00011, 'day/kg', 31, 16),

    -- * media_id 17 == Dairy
    (1, 'biotransfer factor', 'Ba', 0.0000014, 'day/kg', 31, 17),

    -- * media_id 20 == Eggs
    (1, 'biotransfer factor', 'Ba', 0.024, 'day/kg', 31, 20),

    -- * media_id 18 == Pork
    (1, 'biotransfer factor', 'Ba', 0.000034, 'day/kg', 31, 18),

    -- * media_id 19 == Poultry
    (1, 'biotransfer factor', 'Ba', 0.024, 'day/kg', 31, 19);


-- All Chemicals parameters

INSERT INTO mirc_parameter (scenario_id, name, variable, value, unit, chemical_id, media_id)
VALUES
    -- * chemical_id 1 == 1,2,3,4,6,7,8,9-OCDD
    (1, 'metabolism factor', 'MF', 1, NULL, 1, 16), -- media_id 16 == Beef
    (1, 'metabolism factor', 'MF', 1, NULL, 1, 17), -- media_id 17 == Dairy
    (1, 'metabolism factor', 'MF', 1, NULL, 1, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 1, 16), -- media_id 16 == Beef
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 1, 17), -- media_id 17 == Dairy
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 1, 20), -- media_id 20 == Eggs
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 1, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 1, 19), -- media_id 19 == Poultry

    -- * chemical_id 2 == 1,2,3,4,6,7,8,9-OCDF
    (1, 'metabolism factor', 'MF', 1, NULL, 2, 16), -- media_id 16 == Beef
    (1, 'metabolism factor', 'MF', 1, NULL, 2, 17), -- media_id 17 == Dairy
    (1, 'metabolism factor', 'MF', 1, NULL, 2, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 2, 16), -- media_id 16 == Beef
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 2, 17), -- media_id 17 == Dairy
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 2, 20), -- media_id 20 == Eggs
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 2, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 2, 19), -- media_id 19 == Poultry

    -- * chemical_id 3 == 1,2,3,4,6,7,8-HpCDD
    (1, 'metabolism factor', 'MF', 1, NULL, 3, 16), -- media_id 16 == Beef
    (1, 'metabolism factor', 'MF', 1, NULL, 3, 17), -- media_id 17 == Dairy
    (1, 'metabolism factor', 'MF', 1, NULL, 3, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 3, 16), -- media_id 16 == Beef
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 3, 17), -- media_id 17 == Dairy
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 3, 20), -- media_id 20 == Eggs
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 3, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 3, 19), -- media_id 19 == Poultry

    -- * chemical_id 4 == 1,2,3,4,6,7,8-HpCDF
    (1, 'metabolism factor', 'MF', 1, NULL, 4, 16), -- media_id 16 == Beef
    (1, 'metabolism factor', 'MF', 1, NULL, 4, 17), -- media_id 17 == Dairy
    (1, 'metabolism factor', 'MF', 1, NULL, 4, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 4, 16), -- media_id 16 == Beef
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 4, 17), -- media_id 17 == Dairy
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 4, 20), -- media_id 20 == Eggs
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 4, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 4, 19), -- media_id 19 == Poultry

    -- * chemical_id 5 == 1,2,3,4,7,8,9-HpCDF
    (1, 'metabolism factor', 'MF', 1, NULL, 5, 16), -- media_id 16 == Beef
    (1, 'metabolism factor', 'MF', 1, NULL, 5, 17), -- media_id 17 == Dairy
    (1, 'metabolism factor', 'MF', 1, NULL, 5, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 5, 16), -- media_id 16 == Beef
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 5, 17), -- media_id 17 == Dairy
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 5, 20), -- media_id 20 == Eggs
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 5, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 5, 19), -- media_id 19 == Poultry

    -- * chemical_id 6 == 1,2,3,4,7,8-HxCDD
    (1, 'metabolism factor', 'MF', 1, NULL, 6, 16), -- media_id 16 == Beef
    (1, 'metabolism factor', 'MF', 1, NULL, 6, 17), -- media_id 17 == Dairy
    (1, 'metabolism factor', 'MF', 1, NULL, 6, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 6, 16), -- media_id 16 == Beef
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 6, 17), -- media_id 17 == Dairy
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 6, 20), -- media_id 20 == Eggs
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 6, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 6, 19), -- media_id 19 == Poultry

    -- * chemical_id 7 == 1,2,3,4,7,8-HxCDF
    (1, 'metabolism factor', 'MF', 1, NULL, 7, 16), -- media_id 16 == Beef
    (1, 'metabolism factor', 'MF', 1, NULL, 7, 17), -- media_id 17 == Dairy
    (1, 'metabolism factor', 'MF', 1, NULL, 7, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 7, 16), -- media_id 16 == Beef
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 7, 17), -- media_id 17 == Dairy
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 7, 20), -- media_id 20 == Eggs
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 7, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 7, 19), -- media_id 19 == Poultry

    -- * chemical_id 8 == 1,2,3,6,7,8-HxCDD
    (1, 'metabolism factor', 'MF', 1, NULL, 8, 16), -- media_id 16 == Beef
    (1, 'metabolism factor', 'MF', 1, NULL, 8, 17), -- media_id 17 == Dairy
    (1, 'metabolism factor', 'MF', 1, NULL, 8, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 8, 16), -- media_id 16 == Beef
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 8, 17), -- media_id 17 == Dairy
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 8, 20), -- media_id 20 == Eggs
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 8, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 8, 19), -- media_id 19 == Poultry

    -- * chemical_id 9 == 1,2,3,6,7,8-HxCDF
    (1, 'metabolism factor', 'MF', 1, NULL, 9, 16), -- media_id 16 == Beef
    (1, 'metabolism factor', 'MF', 1, NULL, 9, 17), -- media_id 17 == Dairy
    (1, 'metabolism factor', 'MF', 1, NULL, 9, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 9, 16), -- media_id 16 == Beef
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 9, 17), -- media_id 17 == Dairy
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 9, 20), -- media_id 20 == Eggs
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 9, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 9, 19), -- media_id 19 == Poultry

    -- * chemical_id 10 == 1,2,3,7,8,9-HxCDD
    (1, 'metabolism factor', 'MF', 1, NULL, 10, 16), -- media_id 16 == Beef
    (1, 'metabolism factor', 'MF', 1, NULL, 10, 17), -- media_id 17 == Dairy
    (1, 'metabolism factor', 'MF', 1, NULL, 10, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 10, 16), -- media_id 16 == Beef
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 10, 17), -- media_id 17 == Dairy
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 10, 20), -- media_id 20 == Eggs
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 10, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 10, 19), -- media_id 19 == Poultry

    -- * chemical_id 11 == 1,2,3,7,8,9-HxCDF
    (1, 'metabolism factor', 'MF', 1, NULL, 11, 16), -- media_id 16 == Beef
    (1, 'metabolism factor', 'MF', 1, NULL, 11, 17), -- media_id 17 == Dairy
    (1, 'metabolism factor', 'MF', 1, NULL, 11, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 11, 16), -- media_id 16 == Beef
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 11, 17), -- media_id 17 == Dairy
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 11, 20), -- media_id 20 == Eggs
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 11, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 11, 19), -- media_id 19 == Poultry

    -- * chemical_id 12 == 1,2,3,7,8-PeCDD
    (1, 'metabolism factor', 'MF', 1, NULL, 12, 16), -- media_id 16 == Beef
    (1, 'metabolism factor', 'MF', 1, NULL, 12, 17), -- media_id 17 == Dairy
    (1, 'metabolism factor', 'MF', 1, NULL, 12, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 12, 16), -- media_id 16 == Beef
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 12, 17), -- media_id 17 == Dairy
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 12, 20), -- media_id 20 == Eggs
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 12, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 12, 19), -- media_id 19 == Poultry

    -- * chemical_id 13 == 1,2,3,7,8-PeCDF
    (1, 'metabolism factor', 'MF', 1, NULL, 13, 16), -- media_id 16 == Beef
    (1, 'metabolism factor', 'MF', 1, NULL, 13, 17), -- media_id 17 == Dairy
    (1, 'metabolism factor', 'MF', 1, NULL, 13, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 13, 16), -- media_id 16 == Beef
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 13, 17), -- media_id 17 == Dairy
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 13, 20), -- media_id 20 == Eggs
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 13, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 13, 19), -- media_id 19 == Poultry

    -- * chemical_id 14 == 2,3,4,6,7,8-HxCDF
    (1, 'metabolism factor', 'MF', 1, NULL, 14, 16), -- media_id 16 == Beef
    (1, 'metabolism factor', 'MF', 1, NULL, 14, 17), -- media_id 17 == Dairy
    (1, 'metabolism factor', 'MF', 1, NULL, 14, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 14, 16), -- media_id 16 == Beef
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 14, 17), -- media_id 17 == Dairy
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 14, 20), -- media_id 20 == Eggs
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 14, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 14, 19), -- media_id 19 == Poultry

    -- * chemical_id 15 == 2,3,4,7,8-PeCDF
    (1, 'metabolism factor', 'MF', 1, NULL, 15, 16), -- media_id 16 == Beef
    (1, 'metabolism factor', 'MF', 1, NULL, 15, 17), -- media_id 17 == Dairy
    (1, 'metabolism factor', 'MF', 1, NULL, 15, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 15, 16), -- media_id 16 == Beef
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 15, 17), -- media_id 17 == Dairy
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 15, 20), -- media_id 20 == Eggs
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 15, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 15, 19), -- media_id 19 == Poultry

    -- * chemical_id 16 == 2,3,7,8-TCDD
    (1, 'metabolism factor', 'MF', 1, NULL, 16, 16), -- media_id 16 == Beef
    (1, 'metabolism factor', 'MF', 1, NULL, 16, 17), -- media_id 17 == Dairy
    (1, 'metabolism factor', 'MF', 1, NULL, 16, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 16, 16), -- media_id 16 == Beef
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 16, 17), -- media_id 17 == Dairy
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 16, 20), -- media_id 20 == Eggs
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 16, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 16, 19), -- media_id 19 == Poultry

    -- * chemical_id 17 == 2,3,7,8-TCDF
    (1, 'metabolism factor', 'MF', 1, NULL, 17, 16), -- media_id 16 == Beef
    (1, 'metabolism factor', 'MF', 1, NULL, 17, 17), -- media_id 17 == Dairy
    (1, 'metabolism factor', 'MF', 1, NULL, 17, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 17, 16), -- media_id 16 == Beef
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 17, 17), -- media_id 17 == Dairy
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 17, 20), -- media_id 20 == Eggs
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 17, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 17, 19), -- media_id 19 == Poultry

    -- * chemical_id 18 == 2-Methylnaphthalene (PAH)
    (1, 'metabolism factor', 'MF', 0.01, NULL, 18, 16), -- media_id 16 == Beef
    (1, 'metabolism factor', 'MF', 0.01, NULL, 18, 17), -- media_id 17 == Dairy
    (1, 'metabolism factor', 'MF', 0.01, NULL, 18, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 18, 16), -- media_id 16 == Beef
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 18, 17), -- media_id 17 == Dairy
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 18, 20), -- media_id 20 == Eggs
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 18, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 18, 19), -- media_id 19 == Poultry

    -- * chemical_id 19 == 7,12-Dimethylbenz(a)anthracene (PAH)
    (1, 'metabolism factor', 'MF', 0.01, NULL, 19, 16), -- media_id 16 == Beef
    (1, 'metabolism factor', 'MF', 0.01, NULL, 19, 17), -- media_id 17 == Dairy
    (1, 'metabolism factor', 'MF', 0.01, NULL, 19, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 19, 16), -- media_id 16 == Beef
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 19, 17), -- media_id 17 == Dairy
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 19, 20), -- media_id 20 == Eggs
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 19, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 19, 19), -- media_id 19 == Poultry

    -- * chemical_id 20 == Acenaphthene (PAH)
    (1, 'metabolism factor', 'MF', 0.01, NULL, 20, 16), -- media_id 16 == Beef
    (1, 'metabolism factor', 'MF', 0.01, NULL, 20, 17), -- media_id 17 == Dairy
    (1, 'metabolism factor', 'MF', 0.01, NULL, 20, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 20, 16), -- media_id 16 == Beef
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 20, 17), -- media_id 17 == Dairy
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 20, 20), -- media_id 20 == Eggs
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 20, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 20, 19), -- media_id 19 == Poultry

    -- * chemical_id 21 == Acenaphthylene (PAH)
    (1, 'metabolism factor', 'MF', 0.01, NULL, 21, 16), -- media_id 16 == Beef
    (1, 'metabolism factor', 'MF', 0.01, NULL, 21, 17), -- media_id 17 == Dairy
    (1, 'metabolism factor', 'MF', 0.01, NULL, 21, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 21, 16), -- media_id 16 == Beef
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 21, 17), -- media_id 17 == Dairy
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 21, 20), -- media_id 20 == Eggs
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 21, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 21, 19), -- media_id 19 == Poultry

    -- * chemical_id 22 == Arsenic
    (1, 'metabolism factor', 'MF', 1, NULL, 22, 16), -- media_id 16 == Beef
    (1, 'metabolism factor', 'MF', 1, NULL, 22, 17), -- media_id 17 == Dairy
    (1, 'metabolism factor', 'MF', 1, NULL, 22, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 22, 16), -- media_id 16 == Beef
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 22, 17), -- media_id 17 == Dairy
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 22, 20), -- media_id 20 == Eggs
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 22, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 22, 19), -- media_id 19 == Poultry

    -- * chemical_id 23 == Benz(a)anthracene (PAH)
    (1, 'metabolism factor', 'MF', 0.01, NULL, 23, 16), -- media_id 16 == Beef
    (1, 'metabolism factor', 'MF', 0.01, NULL, 23, 17), -- media_id 17 == Dairy
    (1, 'metabolism factor', 'MF', 0.01, NULL, 23, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 23, 16), -- media_id 16 == Beef
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 23, 17), -- media_id 17 == Dairy
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 23, 20), -- media_id 20 == Eggs
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 23, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 23, 19), -- media_id 19 == Poultry

    -- * chemical_id 24 == Benzo(A)Pyrene (PAH)
    (1, 'metabolism factor', 'MF', 0.01, NULL, 24, 16), -- media_id 16 == Beef
    (1, 'metabolism factor', 'MF', 0.01, NULL, 24, 17), -- media_id 17 == Dairy
    (1, 'metabolism factor', 'MF', 0.01, NULL, 24, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 24, 16), -- media_id 16 == Beef
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 24, 17), -- media_id 17 == Dairy
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 24, 20), -- media_id 20 == Eggs
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 24, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 24, 19), -- media_id 19 == Poultry

    -- * chemical_id 25 == Benzo(b)fluoranthene (PAH)
    (1, 'metabolism factor', 'MF', 0.01, NULL, 25, 16), -- media_id 16 == Beef
    (1, 'metabolism factor', 'MF', 0.01, NULL, 25, 17), -- media_id 17 == Dairy
    (1, 'metabolism factor', 'MF', 0.01, NULL, 25, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 25, 16), -- media_id 16 == Beef
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 25, 17), -- media_id 17 == Dairy
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 25, 20), -- media_id 20 == Eggs
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 25, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 25, 19), -- media_id 19 == Poultry

    -- * chemical_id 26 == Benzo(g,h,i)perylene (PAH)
    (1, 'metabolism factor', 'MF', 0.01, NULL, 26, 16), -- media_id 16 == Beef
    (1, 'metabolism factor', 'MF', 0.01, NULL, 26, 17), -- media_id 17 == Dairy
    (1, 'metabolism factor', 'MF', 0.01, NULL, 26, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 26, 16), -- media_id 16 == Beef
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 26, 17), -- media_id 17 == Dairy
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 26, 20), -- media_id 20 == Eggs
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 26, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 26, 19), -- media_id 19 == Poultry

    -- * chemical_id 27 == Benzo(k)fluoranthene (PAH)
    (1, 'metabolism factor', 'MF', 0.01, NULL, 27, 16), -- media_id 16 == Beef
    (1, 'metabolism factor', 'MF', 0.01, NULL, 27, 17), -- media_id 17 == Dairy
    (1, 'metabolism factor', 'MF', 0.01, NULL, 27, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 27, 16), -- media_id 16 == Beef
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 27, 17), -- media_id 17 == Dairy
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 27, 20), -- media_id 20 == Eggs
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 27, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 27, 19), -- media_id 19 == Poultry

    -- * chemical_id 28 == Cadmium
    (1, 'metabolism factor', 'MF', 1, NULL, 28, 16), -- media_id 16 == Beef
    (1, 'metabolism factor', 'MF', 1, NULL, 28, 17), -- media_id 17 == Dairy
    (1, 'metabolism factor', 'MF', 1, NULL, 28, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 28, 16), -- media_id 16 == Beef
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 28, 17), -- media_id 17 == Dairy
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 28, 20), -- media_id 20 == Eggs
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 28, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 28, 19), -- media_id 19 == Poultry

    -- * chemical_id 29 == Chrysene (PAH)
    (1, 'metabolism factor', 'MF', 0.01, NULL, 29, 16), -- media_id 16 == Beef
    (1, 'metabolism factor', 'MF', 0.01, NULL, 29, 17), -- media_id 17 == Dairy
    (1, 'metabolism factor', 'MF', 0.01, NULL, 29, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 29, 16), -- media_id 16 == Beef
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 29, 17), -- media_id 17 == Dairy
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 29, 20), -- media_id 20 == Eggs
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 29, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 29, 19), -- media_id 19 == Poultry

    -- * chemical_id 30 == Dibenz(a,h)anthracene (PAH)
    (1, 'metabolism factor', 'MF', 0.01, NULL, 30, 16), -- media_id 16 == Beef
    (1, 'metabolism factor', 'MF', 0.01, NULL, 30, 17), -- media_id 17 == Dairy
    (1, 'metabolism factor', 'MF', 0.01, NULL, 30, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 30, 16), -- media_id 16 == Beef
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 30, 17), -- media_id 17 == Dairy
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 30, 20), -- media_id 20 == Eggs
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 30, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 30, 19), -- media_id 19 == Poultry

    -- * chemical_id 31 == Divalent Mercury
    (1, 'metabolism factor', 'MF', 1, NULL, 31, 16), -- media_id 16 == Beef
    (1, 'metabolism factor', 'MF', 1, NULL, 31, 17), -- media_id 17 == Dairy
    (1, 'metabolism factor', 'MF', 1, NULL, 31, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 31, 16), -- media_id 16 == Beef
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 31, 17), -- media_id 17 == Dairy
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 31, 20), -- media_id 20 == Eggs
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 31, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 31, 19), -- media_id 19 == Poultry

    -- * chemical_id 32 == Elemental Mercury
    (1, 'metabolism factor', 'MF', 1, NULL, 32, 16), -- media_id 16 == Beef
    (1, 'metabolism factor', 'MF', 1, NULL, 32, 17), -- media_id 17 == Dairy
    (1, 'metabolism factor', 'MF', 1, NULL, 32, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 32, 16), -- media_id 16 == Beef
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 32, 17), -- media_id 17 == Dairy
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 32, 20), -- media_id 20 == Eggs
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 32, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 32, 19), -- media_id 19 == Poultry

    -- * chemical_id 33 == Fluoranthene (PAH)
    (1, 'metabolism factor', 'MF', 0.01, NULL, 33, 16), -- media_id 16 == Beef
    (1, 'metabolism factor', 'MF', 0.01, NULL, 33, 17), -- media_id 17 == Dairy
    (1, 'metabolism factor', 'MF', 0.01, NULL, 33, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 33, 16), -- media_id 16 == Beef
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 33, 17), -- media_id 17 == Dairy
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 33, 20), -- media_id 20 == Eggs
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 33, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 33, 19), -- media_id 19 == Poultry

    -- * chemical_id 34 == Fluorene (PAH)
    (1, 'metabolism factor', 'MF', 0.01, NULL, 34, 16), -- media_id 16 == Beef
    (1, 'metabolism factor', 'MF', 0.01, NULL, 34, 17), -- media_id 17 == Dairy
    (1, 'metabolism factor', 'MF', 0.01, NULL, 34, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 34, 16), -- media_id 16 == Beef
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 34, 17), -- media_id 17 == Dairy
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 34, 20), -- media_id 20 == Eggs
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 34, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 34, 19), -- media_id 19 == Poultry

    -- * chemical_id 35 == Indeno(1,2,3-cd)pyrene (PAH)
    (1, 'metabolism factor', 'MF', 0.01, NULL, 35, 16), -- media_id 16 == Beef
    (1, 'metabolism factor', 'MF', 0.01, NULL, 35, 17), -- media_id 17 == Dairy
    (1, 'metabolism factor', 'MF', 0.01, NULL, 35, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 35, 16), -- media_id 16 == Beef
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 35, 17), -- media_id 17 == Dairy
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 35, 20), -- media_id 20 == Eggs
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 35, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 35, 19), -- media_id 19 == Poultry

    -- * chemical_id 36 == Lead
    (1, 'metabolism factor', 'MF', 1, NULL, 36, 16), -- media_id 16 == Beef
    (1, 'metabolism factor', 'MF', 1, NULL, 36, 17), -- media_id 17 == Dairy
    (1, 'metabolism factor', 'MF', 1, NULL, 36, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 36, 16), -- media_id 16 == Beef
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 36, 17), -- media_id 17 == Dairy
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 36, 20), -- media_id 20 == Eggs
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 36, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 36, 19), -- media_id 19 == Poultry

    -- * chemical_id 37 == MethylMercury
    (1, 'metabolism factor', 'MF', 1, NULL, 37, 16), -- media_id 16 == Beef
    (1, 'metabolism factor', 'MF', 1, NULL, 37, 17), -- media_id 17 == Dairy
    (1, 'metabolism factor', 'MF', 1, NULL, 37, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 37, 16), -- media_id 16 == Beef
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 37, 17), -- media_id 17 == Dairy
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 37, 20), -- media_id 20 == Eggs
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 37, 18), -- media_id 18 == Pork
    (1, 'livestock soil bioavailability factor', 'Bs', 1, NULL, 37, 19); -- media_id 19 == Poultry


COMMIT;
