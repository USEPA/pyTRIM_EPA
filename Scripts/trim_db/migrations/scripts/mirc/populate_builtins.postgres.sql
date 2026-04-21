BEGIN TRANSACTION;

-- Default scenarios
INSERT INTO "mirc_scenario" ("id","name","is_builtin","notes","parent_id")
VALUES (1,'HHRAP/EFH11',true,NULL,NULL);

INSERT INTO "mirc_scenario" ("id","name","is_builtin","notes","parent_id")
VALUES (2,'RTR Screening',true,NULL,1);

-- Builtin products
INSERT INTO "mirc_product" ("name","category_id","is_food","is_feed","id")
VALUES ('water',NULL,true,false,1);

INSERT INTO "mirc_product" ("name","category_id","is_food","is_feed","id")
VALUES ('soil',NULL,true,true,2);

INSERT INTO "mirc_product" ("name","category_id","is_food","is_feed","id")
VALUES ('plant',NULL,false,false,3);

INSERT INTO "mirc_product" ("name","category_id","is_food","is_feed","id")
VALUES ('protected plant',3,false,false,4);

INSERT INTO "mirc_product" ("name","category_id","is_food","is_feed","id")
VALUES ('protected vegetable',4,true,false,5);

INSERT INTO "mirc_product" ("name","category_id","is_food","is_feed","id")
VALUES ('protected fruit',4,true,false,6);

INSERT INTO "mirc_product" ("name","category_id","is_food","is_feed","id")
VALUES ('root',4,true,false,7);

INSERT INTO "mirc_product" ("name","category_id","is_food","is_feed","id")
VALUES ('grain',4,false,true,8);

INSERT INTO "mirc_product" ("name","category_id","is_food","is_feed","id")
VALUES ('exposed plant',3,false,false,9);

INSERT INTO "mirc_product" ("name","category_id","is_food","is_feed","id")
VALUES ('exposed vegetable',9,true,false,10);

INSERT INTO "mirc_product" ("name","category_id","is_food","is_feed","id")
VALUES ('exposed fruit',9,true,false,11);

INSERT INTO "mirc_product" ("name","category_id","is_food","is_feed","id")
VALUES ('forage',9,false,true,12);

INSERT INTO "mirc_product" ("name","category_id","is_food","is_feed","id")
VALUES ('silage',9,false,true,13);

INSERT INTO "mirc_product" ("name","category_id","is_food","is_feed","id")
VALUES ('animal',NULL,false,false,14);

INSERT INTO "mirc_product" ("name","category_id","is_food","is_feed","id")
VALUES ('livestock',14,false,false,15);

INSERT INTO "mirc_product" ("name","category_id","is_food","is_feed","id")
VALUES ('beef',15,true,false,16);

INSERT INTO "mirc_product" ("name","category_id","is_food","is_feed","id")
VALUES ('dairy',16,true,false,17);

INSERT INTO "mirc_product" ("name","category_id","is_food","is_feed","id")
VALUES ('pork',15,true,false,18);

INSERT INTO "mirc_product" ("name","category_id","is_food","is_feed","id")
VALUES ('poultry',15,true,false,19);

INSERT INTO "mirc_product" ("name","category_id","is_food","is_feed","id")
VALUES ('eggs',19,true,false,20);

INSERT INTO "mirc_product" ("name","category_id","is_food","is_feed","id")
VALUES ('fish',14,true,false,21);

INSERT INTO "mirc_product" ("name","category_id","is_food","is_feed","id")
VALUES ('macrophyte',21,false,false,22);

INSERT INTO "mirc_product" ("name","category_id","is_food","is_feed","id")
VALUES ('zooplankton',21,false,false,23);

INSERT INTO "mirc_product" ("name","category_id","is_food","is_feed","id")
VALUES ('water column herbivore',21,false,false,24);

INSERT INTO "mirc_product" ("name","category_id","is_food","is_feed","id")
VALUES ('water column omnivore',21,false,false,25);

INSERT INTO "mirc_product" ("name","category_id","is_food","is_feed","id")
VALUES ('water column carnivore',21,false,false,26);

INSERT INTO "mirc_product" ("name","category_id","is_food","is_feed","id")
VALUES ('benthic invertebrate',21,false,false,27);

INSERT INTO "mirc_product" ("name","category_id","is_food","is_feed","id")
VALUES ('benthic omnivore',21,false,false,28);

INSERT INTO "mirc_product" ("name","category_id","is_food","is_feed","id")
VALUES ('benthic carnivore',21,false,false,29);

INSERT INTO "mirc_product" ("name","category_id","is_food","is_feed","id")
VALUES ('breast milk',NULL,true,false,30);

-- Builtin percentiles
INSERT INTO "mirc_percentile" ("name","id")
VALUES ('P05',1);

INSERT INTO "mirc_percentile" ("name","id")
VALUES ('P10',2);

INSERT INTO "mirc_percentile" ("name","id")
VALUES ('P50',3);

INSERT INTO "mirc_percentile" ("name","id")
VALUES ('P90',4);

INSERT INTO "mirc_percentile" ("name","id")
VALUES ('P95',5);

INSERT INTO "mirc_percentile" ("name","id")
VALUES ('P99',6);

INSERT INTO "mirc_percentile" ("name","id")
VALUES ('Pmean',7);

INSERT INTO "mirc_percentile" ("name","id")
VALUES ('None',8);

-- Builtin lifestages
INSERT INTO "mirc_life_stage" ("name","duration","duration_unit","id")
VALUES ('Child <1',1.0,'year',1);

INSERT INTO "mirc_life_stage" ("name","duration","duration_unit","id")
VALUES ('Child 1-2',2.0,'year',2);

INSERT INTO "mirc_life_stage" ("name","duration","duration_unit","id")
VALUES ('Child 3-5',3.0,'year',3);

INSERT INTO "mirc_life_stage" ("name","duration","duration_unit","id")
VALUES ('Child 6-11',6.0,'year',4);

INSERT INTO "mirc_life_stage" ("name","duration","duration_unit","id")
VALUES ('Child 12-19',8.0,'year',5);

INSERT INTO "mirc_life_stage" ("name","duration","duration_unit","id")
VALUES ('Adult',50.0,'year',6);

INSERT INTO "mirc_life_stage" ("name","duration","duration_unit","id")
VALUES ('Pregnant Mother',274.0,'day',7);

-- Builtin chemicals
UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Zinc', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7440 - 66 - 6';

UPDATE "chemical" SET "hap_number" = '180', "hap_name" = 'Zinc cyanide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '557 - 21 - 1';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = 'Perylene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '198 - 55 - 0';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = 'Retene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '483 - 65 - 8';

UPDATE "chemical" SET "hap_number" = '75', "hap_name" = '1,2-Epoxybutane', "epa_evidence_weight" = NULL
WHERE "cas_number" = '106 - 88 - 7';

UPDATE "chemical" SET "hap_number" = '137', "hap_name" = '1,3-Propane sultone', "epa_evidence_weight" = NULL
WHERE "cas_number" = '1120 - 71 - 4';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = '1,8-Dinitropyrene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '42397 - 65 - 9';

UPDATE "chemical" SET "hap_number" = '71', "hap_name" = '2,4/2,6-Dinitrotoluene (mixture)', "epa_evidence_weight" = NULL
WHERE "cas_number" = '25321 - 14 - 6';

UPDATE "chemical" SET "hap_number" = '154', "hap_name" = '2,4/2,6-Toluene diisocyanate mixture (TDI)', "epa_evidence_weight" = NULL
WHERE "cas_number" = '26471 - 62 - 5';

UPDATE "chemical" SET "hap_number" = '47', "hap_name" = '2,4-D, salts and esters', "epa_evidence_weight" = NULL
WHERE "cas_number" = '94 - 75 - 7';

UPDATE "chemical" SET "hap_number" = '36', "hap_name" = '2-Chloroacetophenone', "epa_evidence_weight" = NULL
WHERE "cas_number" = '532 - 27 - 4';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = '2-Nitrofluorene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '607 - 57 - 8';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = '3-Methylcholanthrene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '56 - 49 - 5';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = '4-Nitropyrene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '57835 - 92 - 4';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = '5-Methylchrysene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '3697 - 24 - 3';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = '5-Nitroacenaphthene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '602 - 87 - 9';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = '6-Nitrochrysene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7496 - 02 - 8';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = '7,12-Dimethylbenz[a]Anthracene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '57 - 97 - 6';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = '7H-Dibenzo[c,g]carbazole', "epa_evidence_weight" = NULL
WHERE "cas_number" = '194 - 59 - 2';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = 'Acenaphthene', "epa_evidence_weight" = 'D'
WHERE "cas_number" = '83 - 32 - 9';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = 'Acenaphthylene', "epa_evidence_weight" = 'D'
WHERE "cas_number" = '208 - 96 - 8';

UPDATE "chemical" SET "hap_number" = '1', "hap_name" = 'Acetaldehyde', "epa_evidence_weight" = NULL
WHERE "cas_number" = '75 - 07 - 0';

UPDATE "chemical" SET "hap_number" = '2', "hap_name" = 'Acetamide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '60 - 35 - 5';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Acetone', "epa_evidence_weight" = NULL
WHERE "cas_number" = '67 - 64 - 1';

UPDATE "chemical" SET "hap_number" = '180', "hap_name" = 'Acetone cyanohydrin', "epa_evidence_weight" = NULL
WHERE "cas_number" = '75 - 86 - 5';

UPDATE "chemical" SET "hap_number" = '3', "hap_name" = 'Acetonitrile', "epa_evidence_weight" = NULL
WHERE "cas_number" = '75 - 05 - 8';

UPDATE "chemical" SET "hap_number" = '4', "hap_name" = 'Acetophenone', "epa_evidence_weight" = NULL
WHERE "cas_number" = '98 - 86 - 2';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = 'Acetylaminofluorene, 2-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '53 - 96 - 3';

UPDATE "chemical" SET "hap_number" = '6', "hap_name" = 'Acrolein', "epa_evidence_weight" = NULL
WHERE "cas_number" = '107 - 02 - 8';

UPDATE "chemical" SET "hap_number" = '7', "hap_name" = 'Acrylamide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '79 - 06 - 1';

UPDATE "chemical" SET "hap_number" = '8', "hap_name" = 'Acrylic acid', "epa_evidence_weight" = NULL
WHERE "cas_number" = '79 - 10 - 7';

UPDATE "chemical" SET "hap_number" = '9', "hap_name" = 'Acrylonitrile', "epa_evidence_weight" = NULL
WHERE "cas_number" = '107 - 13 - 1';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Aldrin', "epa_evidence_weight" = NULL
WHERE "cas_number" = '309 - 00 - 2';

UPDATE "chemical" SET "hap_number" = '10', "hap_name" = 'Allyl Chloride', "epa_evidence_weight" = NULL
WHERE "cas_number" = '107 - 05 - 1';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'alpha,alpha-Dimethylphenethylamine', "epa_evidence_weight" = NULL
WHERE "cas_number" = '122 - 09 - 8';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Aluminum', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7429 - 90 - 5';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Aluminum oxide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '1344 - 28 - 1';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Amino-2-Methylanthraquinone, 1-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '82 - 28 - 0';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'amino-2-nitrophenol, 4-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '119 - 34 - 6';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Amino-4-nitrophenol, 2-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '99 - 57 - 0';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Aminoanisole, o-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '90 - 04 - 0';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = 'Aminoanthraquinone, 2-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '117 - 79 - 3';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Aminoazobenzene, 4-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '60 - 09 - 3';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Aminoazotoluene, o', "epa_evidence_weight" = NULL
WHERE "cas_number" = '97 - 56 - 3';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Aminodiphenyl, 4-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '92 - 67 - 1';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Ammonia', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7664 - 41 - 7';

UPDATE "chemical" SET "hap_number" = '12', "hap_name" = 'Aniline', "epa_evidence_weight" = NULL
WHERE "cas_number" = '62 - 53 - 3';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = 'Anthracene', "epa_evidence_weight" = 'D'
WHERE "cas_number" = '120 - 12 - 7';

UPDATE "chemical" SET "hap_number" = '173', "hap_name" = 'Antimony', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7440 - 36 - 0';

UPDATE "chemical" SET "hap_number" = '173', "hap_name" = 'Antimony pentoxide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '1314 - 60 - 9';

UPDATE "chemical" SET "hap_number" = '173', "hap_name" = 'Antimony potassium tartrate', "epa_evidence_weight" = NULL
WHERE "cas_number" = '304 - 61 - 0';

UPDATE "chemical" SET "hap_number" = '173', "hap_name" = 'Antimony tetroxide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '1332 - 81 - 6';

UPDATE "chemical" SET "hap_number" = '173', "hap_name" = 'Antimony trioxide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '1309 - 64 - 4';

UPDATE "chemical" SET "hap_number" = '136', "hap_name" = 'Aroclor 1016', "epa_evidence_weight" = NULL
WHERE "cas_number" = '12674 - 11 - 2';

UPDATE "chemical" SET "hap_number" = '136', "hap_name" = 'Aroclor 1254', "epa_evidence_weight" = NULL
WHERE "cas_number" = '11097 - 69 - 1';

UPDATE "chemical" SET "hap_number" = '174', "hap_name" = 'Arsenic compounds', "epa_evidence_weight" = 'B1'
WHERE "cas_number" = '7440 - 38 - 2';

UPDATE "chemical" SET "hap_number" = '174', "hap_name" = 'Arsenic pentoxide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '1303 - 28 - 2';

UPDATE "chemical" SET "hap_number" = '174', "hap_name" = 'Arsine', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7784 - 42 - 1';

UPDATE "chemical" SET "hap_number" = '999', "hap_name" = 'Asbestos', "epa_evidence_weight" = NULL
WHERE "cas_number" = '1332 - 21 - 4';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Atrazine', "epa_evidence_weight" = NULL
WHERE "cas_number" = '1912 - 24 - 9';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Auramine', "epa_evidence_weight" = NULL
WHERE "cas_number" = '492 - 80 - 8';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Barium', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7440 - 39 - 3';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Benz[c]acridine', "epa_evidence_weight" = NULL
WHERE "cas_number" = '225 - 51 - 4';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Benzaldehyde', "epa_evidence_weight" = NULL
WHERE "cas_number" = '100 - 52 - 7';

UPDATE "chemical" SET "hap_number" = '15', "hap_name" = 'Benzene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '71 - 43 - 2';

UPDATE "chemical" SET "hap_number" = '16', "hap_name" = 'Benzidine', "epa_evidence_weight" = NULL
WHERE "cas_number" = '92 - 87 - 5';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = 'Benz[a]anthracene', "epa_evidence_weight" = 'B2'
WHERE "cas_number" = '56 - 55 - 3';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = 'Benzo[a]pyrene', "epa_evidence_weight" = 'B2'
WHERE "cas_number" = '50 - 32 - 8';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = 'Benzo[b]fluoranthene', "epa_evidence_weight" = 'B2'
WHERE "cas_number" = '205 - 99 - 2';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = 'Benzo(e)pyrene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '192 - 97 - 2';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = 'Benzo(ghi)perylene', "epa_evidence_weight" = 'D'
WHERE "cas_number" = '191 - 24 - 2';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = 'Benzo[k]fluoranthene', "epa_evidence_weight" = 'B2'
WHERE "cas_number" = '207 - 08 - 9';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = 'Benzo[j]fluoranthene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '205 - 82 - 3';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Benzoic acid', "epa_evidence_weight" = NULL
WHERE "cas_number" = '65 - 85 - 0';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Benzonitrile', "epa_evidence_weight" = NULL
WHERE "cas_number" = '100 - 47 - 0';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Benzothiazolinone, 2-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '934 - 34 - 9';

UPDATE "chemical" SET "hap_number" = '17', "hap_name" = 'Benzotrichloride', "epa_evidence_weight" = NULL
WHERE "cas_number" = '98 - 07 - 7';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Benzyl alcohol', "epa_evidence_weight" = NULL
WHERE "cas_number" = '100 - 51 - 6';

UPDATE "chemical" SET "hap_number" = '18', "hap_name" = 'Benzyl chloride', "epa_evidence_weight" = NULL
WHERE "cas_number" = '100 - 44 - 7';

UPDATE "chemical" SET "hap_number" = '175', "hap_name" = 'Beryllium', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7440 - 41 - 7';

UPDATE "chemical" SET "hap_number" = '175', "hap_name" = 'Beryllium oxide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '1304 - 56 - 9';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'beta-Naphthylamine', "epa_evidence_weight" = NULL
WHERE "cas_number" = '91 - 59 - 8';

UPDATE "chemical" SET "hap_number" = '101', "hap_name" = 'BHC, Alpha-', "epa_evidence_weight" = 'B2'
WHERE "cas_number" = '319 - 84 - 6';

UPDATE "chemical" SET "hap_number" = '101', "hap_name" = 'BHC, Beta-', "epa_evidence_weight" = 'C'
WHERE "cas_number" = '319 - 85 - 7';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Bibenzyl', "epa_evidence_weight" = NULL
WHERE "cas_number" = '103 - 29 - 7';

UPDATE "chemical" SET "hap_number" = '19', "hap_name" = 'Biphenyl', "epa_evidence_weight" = NULL
WHERE "cas_number" = '92 - 52 - 4';

UPDATE "chemical" SET "hap_number" = '21', "hap_name" = 'Bis(chloromethyl)ether', "epa_evidence_weight" = NULL
WHERE "cas_number" = '542 - 88 - 1';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Boron', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7440 - 42 - 8';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Bromacil', "epa_evidence_weight" = NULL
WHERE "cas_number" = '314 - 40 - 9';

UPDATE "chemical" SET "hap_number" = '22', "hap_name" = 'Bromoform', "epa_evidence_weight" = NULL
WHERE "cas_number" = '75 - 25 - 2';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Bromophenol, 4-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '106 - 41 - 2';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Bromophenyl-phenylether, 4-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '101 - 55 - 3';

UPDATE "chemical" SET "hap_number" = '23', "hap_name" = 'Butadiene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '106 - 99 - 0';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Butanamide, 3-methyl-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '541 - 46 - 8';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Butanediol, 2,3-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '513 - 85 - 9';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Butanol', "epa_evidence_weight" = NULL
WHERE "cas_number" = '71 - 36 - 3';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Butoxy ethanol, 2-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '111 - 76 - 2';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Butyl benzyl phthalate', "epa_evidence_weight" = NULL
WHERE "cas_number" = '85 - 68 - 7';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Butyl Stearate', "epa_evidence_weight" = NULL
WHERE "cas_number" = '123 - 95 - 5';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Butyraldehyde', "epa_evidence_weight" = NULL
WHERE "cas_number" = '123 - 72 - 8';

UPDATE "chemical" SET "hap_number" = '176', "hap_name" = 'Cadmium compounds', "epa_evidence_weight" = 'B1'
WHERE "cas_number" = '7440 - 43 - 9';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Calcium', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7440 - 70 - 2';

UPDATE "chemical" SET "hap_number" = '180', "hap_name" = 'Calcium cyanide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '592 - 01 - 8';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Camphor', "epa_evidence_weight" = NULL
WHERE "cas_number" = '76 - 22 - 2';

UPDATE "chemical" SET "hap_number" = '26', "hap_name" = 'Captan', "epa_evidence_weight" = NULL
WHERE "cas_number" = '133 - 06 - 2';

UPDATE "chemical" SET "hap_number" = '27', "hap_name" = 'Carbaryl', "epa_evidence_weight" = NULL
WHERE "cas_number" = '63 - 25 - 2';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = 'Carbazole', "epa_evidence_weight" = 'B2'
WHERE "cas_number" = '86 - 74 - 8';

UPDATE "chemical" SET "hap_number" = '28', "hap_name" = 'Carbon disulfide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '75 - 15 - 0';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Carbon Monoxide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '630 - 08 - 0';

UPDATE "chemical" SET "hap_number" = '29', "hap_name" = 'Carbon tetrachloride', "epa_evidence_weight" = NULL
WHERE "cas_number" = '56 - 23 - 5';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Cerium', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7440 - 45 - 1';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Cetyl Alcohol', "epa_evidence_weight" = NULL
WHERE "cas_number" = '36653 - 82 - 4';

UPDATE "chemical" SET "hap_number" = '32', "hap_name" = 'Chloramben', "epa_evidence_weight" = NULL
WHERE "cas_number" = '133 - 90 - 4';

UPDATE "chemical" SET "hap_number" = '33', "hap_name" = 'Chlordane', "epa_evidence_weight" = 'LH'
WHERE "cas_number" = '57 - 74 - 9';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Chlordane, cis', "epa_evidence_weight" = NULL
WHERE "cas_number" = '5103 - 71 - 9';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Chlordane, trans-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '5103 - 74 - 2';

UPDATE "chemical" SET "hap_number" = '34', "hap_name" = 'Chlorine', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7782 - 50 - 5';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'chloro-1-methylethyl ether, Bis 2-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '108 - 60 - 1';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Chloro-3-methylphenol, 4-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '35421 - 08 - 0';

UPDATE "chemical" SET "hap_number" = '35', "hap_name" = 'Chloroacetic acid', "epa_evidence_weight" = NULL
WHERE "cas_number" = '79 - 11 - 8';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'chloroaniline, 4-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '106 - 47 - 8';

UPDATE "chemical" SET "hap_number" = '37', "hap_name" = 'Chlorobenzene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '108 - 90 - 7';

UPDATE "chemical" SET "hap_number" = '38', "hap_name" = 'Chlorobenzilate', "epa_evidence_weight" = NULL
WHERE "cas_number" = '510 - 15 - 6';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Chlorodibromomethane', "epa_evidence_weight" = NULL
WHERE "cas_number" = '124 - 48 - 1';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Chlorodifluoromethane', "epa_evidence_weight" = NULL
WHERE "cas_number" = '75 - 45 - 6';

UPDATE "chemical" SET "hap_number" = '79', "hap_name" = 'Chloroethane', "epa_evidence_weight" = NULL
WHERE "cas_number" = '75 - 00 - 3';

UPDATE "chemical" SET "hap_number" = '55', "hap_name" = 'chloroethyl ether, Bis 2-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '111 - 44 - 4';

UPDATE "chemical" SET "hap_number" = '39', "hap_name" = 'Chloroform', "epa_evidence_weight" = NULL
WHERE "cas_number" = '67 - 66 - 3';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Chloroisopropylether, Bis-1,2-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '39638 - 32 - 9';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = 'Chloronaphthalene, 2-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '91 - 58 - 7';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Chlorophenol, 2-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '95 - 57 - 8';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Chlorophenol, 4-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '106 - 48 - 9';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Chlorophenyl phenyl ether, 4-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7005 - 72 - 3';

UPDATE "chemical" SET "hap_number" = '41', "hap_name" = 'Chloroprene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '126 - 99 - 8';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Chloropyrifos', "epa_evidence_weight" = NULL
WHERE "cas_number" = '2921 - 88 - 2';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Chlorothalonil', "epa_evidence_weight" = NULL
WHERE "cas_number" = '1897 - 45 - 6';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Chromium', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7440 - 47 - 3';

UPDATE "chemical" SET "hap_number" = '177', "hap_name" = 'Chromium (III) compounds', "epa_evidence_weight" = NULL
WHERE "cas_number" = '16065 - 83 - 1';

UPDATE "chemical" SET "hap_number" = '177', "hap_name" = 'Chromium (VI) trioxide, chromic acid mist', "epa_evidence_weight" = NULL
WHERE "cas_number" = '11115 - 74 - 5';

UPDATE "chemical" SET "hap_number" = '177', "hap_name" = 'Chromium(VI)', "epa_evidence_weight" = NULL
WHERE "cas_number" = '18540 - 29 - 9';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = 'Chrysene', "epa_evidence_weight" = 'B2'
WHERE "cas_number" = '218 - 01 - 9';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'cis-1,4-Dimethylcyclohexane', "epa_evidence_weight" = NULL
WHERE "cas_number" = '624 - 29 - 3';

UPDATE "chemical" SET "hap_number" = '178', "hap_name" = 'Cobalt', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7440 - 48 - 4';

UPDATE "chemical" SET "hap_number" = '179', "hap_name" = 'Coke Oven Emissions', "epa_evidence_weight" = NULL
WHERE "cas_number" = '8007 - 45 - 2';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Collodion', "epa_evidence_weight" = NULL
WHERE "cas_number" = '9004 - 70 - 0';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Copper', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7440 - 50 - 8';

UPDATE "chemical" SET "hap_number" = '180', "hap_name" = 'Copper cyanide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '544 - 92 - 3';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Cresidine, p-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '120 - 71 - 8';

UPDATE "chemical" SET "hap_number" = '44', "hap_name" = 'Cresol, m-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '108 - 39 - 4';

UPDATE "chemical" SET "hap_number" = '43', "hap_name" = 'Cresol, o-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '95 - 48 - 7';

UPDATE "chemical" SET "hap_number" = '45', "hap_name" = 'Cresol, p-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '106 - 44 - 5';

UPDATE "chemical" SET "hap_number" = '42', "hap_name" = 'Cresols (mixed)', "epa_evidence_weight" = NULL
WHERE "cas_number" = '1319 - 77 - 3';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Crotonaldehyde', "epa_evidence_weight" = NULL
WHERE "cas_number" = '4170 - 30 - 3';

UPDATE "chemical" SET "hap_number" = '46', "hap_name" = 'Cumene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '98 - 82 - 8';

UPDATE "chemical" SET "hap_number" = '180', "hap_name" = 'Cyanazine', "epa_evidence_weight" = NULL
WHERE "cas_number" = '21725 - 46 - 2';

UPDATE "chemical" SET "hap_number" = '180', "hap_name" = 'Cyanide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '57 - 12 - 5';

UPDATE "chemical" SET "hap_number" = '180', "hap_name" = 'Cyanogen', "epa_evidence_weight" = NULL
WHERE "cas_number" = '460 - 19 - 5';

UPDATE "chemical" SET "hap_number" = '180', "hap_name" = 'Cyanogen bromide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '506 - 68 - 3';

UPDATE "chemical" SET "hap_number" = '180', "hap_name" = 'Cyanogen chloride', "epa_evidence_weight" = NULL
WHERE "cas_number" = '506 - 77 - 4';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Cyclohexanol, 2-chloro-, trans-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '6628 - 80 - 4';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Cyclohexenone, 2-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '930 - 68 - 7';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Cyclotrimethylenetrinitramine', "epa_evidence_weight" = NULL
WHERE "cas_number" = '121 - 82 - 4';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'DDD', "epa_evidence_weight" = NULL
WHERE "cas_number" = '72 - 54 - 8';

UPDATE "chemical" SET "hap_number" = '48', "hap_name" = 'DDE', "epa_evidence_weight" = 'B2'
WHERE "cas_number" = '72 - 55 - 9';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'DDT', "epa_evidence_weight" = NULL
WHERE "cas_number" = '50 - 29 - 3';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Decamethylcyclopentasiloxane', "epa_evidence_weight" = NULL
WHERE "cas_number" = '541 - 02 - 6';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Decane', "epa_evidence_weight" = NULL
WHERE "cas_number" = '124 - 18 - 5';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Diaminoanisole, 2,4-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '615 - 05 - 4';

UPDATE "chemical" SET "hap_number" = '153', "hap_name" = 'Diaminotoluene, 2,4-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '95 - 80 - 7';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Diazinon', "epa_evidence_weight" = NULL
WHERE "cas_number" = '333 - 41 - 5';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = 'Dibenz[a,h]acridine', "epa_evidence_weight" = NULL
WHERE "cas_number" = '226 - 36 - 8';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = 'Dibenzo[a,h]anthracene', "epa_evidence_weight" = 'B2'
WHERE "cas_number" = '53 - 70 - 3';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = 'Dibenz[a,j]acridine', "epa_evidence_weight" = NULL
WHERE "cas_number" = '224 - 42 - 0';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = 'Dibenzo[a,e]pyrene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '192 - 65 - 4';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = 'Dibenzo[a,h]pyrene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '189 - 64 - 0';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = 'Dibenzo[a,i]pyrene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '189 - 55 - 9';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = 'Dibenzo[a,l]pyrene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '191 - 30 - 0';

UPDATE "chemical" SET "hap_number" = '148', "hap_name" = 'Dibenzofuran', "epa_evidence_weight" = NULL
WHERE "cas_number" = '132 - 64 - 9';

UPDATE "chemical" SET "hap_number" = '51', "hap_name" = 'Dibromo-3-Chloropropane, 1,2-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '96 - 12 - 8';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Dibromomethane', "epa_evidence_weight" = NULL
WHERE "cas_number" = '74 - 95 - 3';

UPDATE "chemical" SET "hap_number" = '52', "hap_name" = 'Dibutyl phthalate', "epa_evidence_weight" = NULL
WHERE "cas_number" = '84 - 74 - 2';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Dichlorobenzene, m-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '541 - 73 - 1';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Dichlorobenzene, o-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '95 - 50 - 1';

UPDATE "chemical" SET "hap_number" = '53', "hap_name" = 'Dichlorobenzene, p-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '106 - 46 - 7';

UPDATE "chemical" SET "hap_number" = '54', "hap_name" = 'Dichlorobenzidine, 3,3''-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '106 - 46 - 7';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Dichlorobromomethane', "epa_evidence_weight" = NULL
WHERE "cas_number" = '75 - 27 - 4';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Dichlorodifluoromethane', "epa_evidence_weight" = NULL
WHERE "cas_number" = '75 - 71 - 8';

UPDATE "chemical" SET "hap_number" = '86', "hap_name" = 'Dichloroethane, 1,1-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '75 - 34 - 3';

UPDATE "chemical" SET "hap_number" = '81', "hap_name" = 'Dichloroethane, 1,2-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '107 - 06 - 2';

UPDATE "chemical" SET "hap_number" = '168', "hap_name" = 'Dichloroethylene, 1,1-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '75 - 35 - 4';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Dichloroethylene, cis-1,2-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '156 - 59 - 2';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Dichloroethylene, trans-1,2-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '156 - 60 - 5';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Dichloromonofluoromethane', "epa_evidence_weight" = NULL
WHERE "cas_number" = '75 - 43 - 4';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Dichlorophenol, 2,4-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '120 - 83 - 2';

UPDATE "chemical" SET "hap_number" = '141', "hap_name" = 'Dichloropropane, 1,2-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '78 - 87 - 5';

UPDATE "chemical" SET "hap_number" = '56', "hap_name" = 'Dichloropropene, 1,3-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '542 - 75 - 6';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Dichloropropylene, 1,3 (CIS)-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '10061 - 01 - 5';

UPDATE "chemical" SET "hap_number" = '57', "hap_name" = 'Dichlorvos', "epa_evidence_weight" = NULL
WHERE "cas_number" = '62 - 73 - 7';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Dieldrin', "epa_evidence_weight" = NULL
WHERE "cas_number" = '60 - 57 - 1';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Diepoxybutane', "epa_evidence_weight" = NULL
WHERE "cas_number" = '1464 - 53 - 5';

UPDATE "chemical" SET "hap_number" = '999', "hap_name" = 'Diesel engine emissions', "epa_evidence_weight" = NULL
WHERE "cas_number" = 'DIESEL EMIS.';

UPDATE "chemical" SET "hap_number" = '58', "hap_name" = 'Diethanolamine', "epa_evidence_weight" = NULL
WHERE "cas_number" = '111 - 42 - 2';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Diethoxydimethylsilane', "epa_evidence_weight" = NULL
WHERE "cas_number" = '78 - 62 - 6';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Diethyl phthalate', "epa_evidence_weight" = NULL
WHERE "cas_number" = '84 - 66 - 2';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Diethyl Sulfate', "epa_evidence_weight" = NULL
WHERE "cas_number" = '64 - 67 - 5';

UPDATE "chemical" SET "hap_number" = '181', "hap_name" = 'Diethylene glycol monobutyl ether', "epa_evidence_weight" = NULL
WHERE "cas_number" = '112 - 34 - 5';

UPDATE "chemical" SET "hap_number" = '181', "hap_name" = 'Diethylene glycol monoethyl ether', "epa_evidence_weight" = NULL
WHERE "cas_number" = '111 - 90 - 0';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Difluorodimethylsilane', "epa_evidence_weight" = NULL
WHERE "cas_number" = '353 - 66 - 2';

UPDATE "chemical" SET "hap_number" = '61', "hap_name" = 'Dimethoxybenzidine, 3,3''-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '119 - 90 - 4';

UPDATE "chemical" SET "hap_number" = '65', "hap_name" = 'Dimethyl formamide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '68 - 12 - 2';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Dimethyl phthalate', "epa_evidence_weight" = NULL
WHERE "cas_number" = '131 - 11 - 3';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Dimethyl Sulfate', "epa_evidence_weight" = NULL
WHERE "cas_number" = '77 - 78 - 1';

UPDATE "chemical" SET "hap_number" = '62', "hap_name" = 'Dimethylaminoazobenzene, 4-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '60 - 11 - 7';

UPDATE "chemical" SET "hap_number" = '63', "hap_name" = 'Dimethylbenzidine, 3,3-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '119 - 93 - 7';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Dimethylcarbamoyl Chloride', "epa_evidence_weight" = NULL
WHERE "cas_number" = '79 - 44 - 7';

UPDATE "chemical" SET "hap_number" = '66', "hap_name" = 'Dimethylhydrazine, 1,1-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '57 - 14 - 7';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Dimethylnaphthalene, 1,6-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '575 - 43 - 9';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Dimethylphenol, 2,4-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '105 - 67 - 9';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Dimethylphenol, 3,4-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '95 - 65 - 8';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Dinitrobenzene,1,3-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '99 - 65 - 0';

UPDATE "chemical" SET "hap_number" = '70', "hap_name" = 'Dinitrophenol, 2,4-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '51 - 28 - 5';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = 'Dinitropyrene, 1,6-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '42397 - 64 - 8';

UPDATE "chemical" SET "hap_number" = '71', "hap_name" = 'Dinitrotoluene, 2,4-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '121 - 14 - 2';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Dinitrotoluene, 2,6-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '606 - 20 - 2';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Di-n-octyl phthalate', "epa_evidence_weight" = NULL
WHERE "cas_number" = '117 - 84 - 0';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'dioctyl cebacate', "epa_evidence_weight" = NULL
WHERE "cas_number" = '2432 - 87 - 3';

UPDATE "chemical" SET "hap_number" = '72', "hap_name" = 'Dioxane, 1,4-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '123 - 91 - 1';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Diphenyl amine', "epa_evidence_weight" = NULL
WHERE "cas_number" = '122 - 39 - 4';

UPDATE "chemical" SET "hap_number" = '73', "hap_name" = 'Diphenylhydrazine, 1,2-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '122 - 66 - 7';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Dipropyl adipate', "epa_evidence_weight" = NULL
WHERE "cas_number" = '106 - 19 - 4';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Disulfoton', "epa_evidence_weight" = NULL
WHERE "cas_number" = '298 - 04 - 4';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Endosulfan', "epa_evidence_weight" = NULL
WHERE "cas_number" = '115 - 29 - 7';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Endrin', "epa_evidence_weight" = NULL
WHERE "cas_number" = '72 - 20 - 8';

UPDATE "chemical" SET "hap_number" = '74', "hap_name" = 'Epichlorohydrin', "epa_evidence_weight" = NULL
WHERE "cas_number" = '106 - 89 - 8';

UPDATE "chemical" SET "hap_number" = '147', "hap_name" = 'Epoxyethylbenzene, 1,2-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '96 - 09 - 3';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Ethanol', "epa_evidence_weight" = NULL
WHERE "cas_number" = '628 - 68 - 2';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Ether', "epa_evidence_weight" = NULL
WHERE "cas_number" = '60 - 29 - 7';

UPDATE "chemical" SET "hap_number" = '181', "hap_name" = 'Ethoxyethanol, 2-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '110 - 80 - 5';

UPDATE "chemical" SET "hap_number" = '181', "hap_name" = 'Ethoxyethyl acetate, 2-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '111 - 15 - 9';

UPDATE "chemical" SET "hap_number" = '76', "hap_name" = 'Ethyl Acrylate', "epa_evidence_weight" = NULL
WHERE "cas_number" = '140 - 88 - 5';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Ethyl Alcohol', "epa_evidence_weight" = NULL
WHERE "cas_number" = '64 - 17 - 5';

UPDATE "chemical" SET "hap_number" = '77', "hap_name" = 'Ethyl Benzene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '100 - 41 - 4';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Ethyl Methacrylate', "epa_evidence_weight" = NULL
WHERE "cas_number" = '97 - 63 - 2';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Ethyl methanesulfonate', "epa_evidence_weight" = NULL
WHERE "cas_number" = '62 - 50 - 0';

UPDATE "chemical" SET "hap_number" = '180', "hap_name" = 'Ethylene cyanohydrin', "epa_evidence_weight" = NULL
WHERE "cas_number" = '109 - 78 - 4';

UPDATE "chemical" SET "hap_number" = '80', "hap_name" = 'Ethylene Dibromide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '106 - 93 - 4';

UPDATE "chemical" SET "hap_number" = '82', "hap_name" = 'Ethylene glycol', "epa_evidence_weight" = NULL
WHERE "cas_number" = '107 - 21 - 1';

UPDATE "chemical" SET "hap_number" = '181', "hap_name" = 'Ethylene glycol methyl ether acetate', "epa_evidence_weight" = NULL
WHERE "cas_number" = '110 - 49 - 6';

UPDATE "chemical" SET "hap_number" = '84', "hap_name" = 'Ethylene Oxide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '75 - 21 - 8';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Ethyleneimine', "epa_evidence_weight" = NULL
WHERE "cas_number" = '151 - 56 - 4';

UPDATE "chemical" SET "hap_number" = '85', "hap_name" = 'Ethylenethiourea', "epa_evidence_weight" = NULL
WHERE "cas_number" = '96 - 45 - 7';

UPDATE "chemical" SET "hap_number" = '20', "hap_name" = 'Ethylhexyl Phthalate, Bis 2', "epa_evidence_weight" = NULL
WHERE "cas_number" = '117 - 81 - 7';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Ethylphenol, 4-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '123 - 07 - 9';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = 'Fluoranthene', "epa_evidence_weight" = 'D'
WHERE "cas_number" = '206 - 44 - 0';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = 'Fluorene', "epa_evidence_weight" = 'D'
WHERE "cas_number" = '86 - 73 - 7';

UPDATE "chemical" SET "hap_number" = '87', "hap_name" = 'Formaldehyde', "epa_evidence_weight" = NULL
WHERE "cas_number" = '50 - 00 - 0';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Formic acid', "epa_evidence_weight" = NULL
WHERE "cas_number" = '64 - 18 - 6';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Glycerin', "epa_evidence_weight" = NULL
WHERE "cas_number" = '56 - 81 - 5';

UPDATE "chemical" SET "hap_number" = '148', "hap_name" = '1,2,3,4,6,7,8-Heptachlorodibenzo-p-dioxin', "epa_evidence_weight" = NULL
WHERE "cas_number" = '35822 - 46 - 9';

UPDATE "chemical" SET "hap_number" = '148', "hap_name" = '1,2,3,4,6,7,8-Heptachlorodibenzofuran', "epa_evidence_weight" = NULL
WHERE "cas_number" = '67562 - 39 - 4';

UPDATE "chemical" SET "hap_number" = '148', "hap_name" = '1,2,3,4,7,8,9-Heptachlorodibenzofuran', "epa_evidence_weight" = NULL
WHERE "cas_number" = '55673 - 89 - 7';

UPDATE "chemical" SET "hap_number" = '88', "hap_name" = 'Heptachlor', "epa_evidence_weight" = 'B2'
WHERE "cas_number" = '76 - 44 - 8';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Heptachlor epoxide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '1024 - 57 - 3';

UPDATE "chemical" SET "hap_number" = '148', "hap_name" = '1,2,3,4,7,8-Hexachlorodibenzo-p-dioxin', "epa_evidence_weight" = NULL
WHERE "cas_number" = '39227 - 28 - 6';

UPDATE "chemical" SET "hap_number" = '148', "hap_name" = '1,2,3,6,7,8-Hexachlorodibenzo-p-dioxin', "epa_evidence_weight" = NULL
WHERE "cas_number" = '57653 - 85 - 7';

UPDATE "chemical" SET "hap_number" = '148', "hap_name" = '1,2,3,7,8,9-Hexachlorodibenzo-p-dioxin', "epa_evidence_weight" = 'B2'
WHERE "cas_number" = '19408 - 74 - 3';

UPDATE "chemical" SET "hap_number" = '148', "hap_name" = 'HexaCDD, 2,3,7,8-;', "epa_evidence_weight" = NULL
WHERE "cas_number" = '34465 - 46 - 8';

UPDATE "chemical" SET "hap_number" = '148', "hap_name" = '1,2,3,4,7,8-Hexachlorodibenzofuran', "epa_evidence_weight" = NULL
WHERE "cas_number" = '70648 - 26 - 9';

UPDATE "chemical" SET "hap_number" = '148', "hap_name" = '1,2,3,6,7,8-Hexachlorodibenzofuran', "epa_evidence_weight" = NULL
WHERE "cas_number" = '57117 - 44 - 9';

UPDATE "chemical" SET "hap_number" = '148', "hap_name" = '1,2,3,7,8,9-Hexachlorodibenzofuran', "epa_evidence_weight" = NULL
WHERE "cas_number" = '72918 - 21 - 9';

UPDATE "chemical" SET "hap_number" = '148', "hap_name" = '2,3,4,6,7,8-Hexachlorodibenzofuran', "epa_evidence_weight" = NULL
WHERE "cas_number" = '60851 - 34 - 5';

UPDATE "chemical" SET "hap_number" = '89', "hap_name" = 'Hexachlorobenzene', "epa_evidence_weight" = 'B2'
WHERE "cas_number" = '118 - 74 - 1';

UPDATE "chemical" SET "hap_number" = '90', "hap_name" = 'Hexachlorobutadiene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '87 - 68 - 3';

UPDATE "chemical" SET "hap_number" = '91', "hap_name" = 'Hexachlorocyclopentadiene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '77 - 47 - 4';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Hexachlorodibenzofuran', "epa_evidence_weight" = NULL
WHERE "cas_number" = '55684 - 94 - 1';

UPDATE "chemical" SET "hap_number" = '92', "hap_name" = 'hexachloroethane', "epa_evidence_weight" = NULL
WHERE "cas_number" = '67 - 72 - 1';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Hexachlorophene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '70 - 30 - 4';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Hexamethylcyclotrisiloxane', "epa_evidence_weight" = NULL
WHERE "cas_number" = '541 - 05 - 9';

UPDATE "chemical" SET "hap_number" = '93', "hap_name" = 'Hexamethylene-1,6-diisocyanate', "epa_evidence_weight" = NULL
WHERE "cas_number" = '822 - 06 - 0';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Hexamethylphosphoramide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '680 - 31 - 9';

UPDATE "chemical" SET "hap_number" = '95', "hap_name" = 'Hexane', "epa_evidence_weight" = NULL
WHERE "cas_number" = '110 - 54 - 3';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Hexanol, 2-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '626 - 93 - 7';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Hexanol, n-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '111 - 27 - 3';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Hexanone, 2-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '591 - 78 - 6';

UPDATE "chemical" SET "hap_number" = '96', "hap_name" = 'Hydrazine', "epa_evidence_weight" = NULL
WHERE "cas_number" = '302 - 01 - 2';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Hydrindene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '496 - 11 - 7';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Hydrobromic acid', "epa_evidence_weight" = NULL
WHERE "cas_number" = '10035 - 10 - 6';

UPDATE "chemical" SET "hap_number" = '97', "hap_name" = 'Hydrochloric acid', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7647 - 01 - 0';

UPDATE "chemical" SET "hap_number" = '98', "hap_name" = 'Hydrofluoric Acid', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7664 - 39 - 3';

UPDATE "chemical" SET "hap_number" = '180', "hap_name" = 'Hydrogen Cyanide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '74 - 90 - 8';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Hydrogen fluoride', "epa_evidence_weight" = NULL
WHERE "cas_number" = '73602 - 61 - 6';

UPDATE "chemical" SET "hap_number" = '189', "hap_name" = 'Hydrogen selenide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7783 - 07 - 5';

UPDATE "chemical" SET "hap_number" = '999', "hap_name" = 'Hydrogen sulfide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7783 - 06 - 4';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Hydroperoxide, 1-methylethyl', "epa_evidence_weight" = NULL
WHERE "cas_number" = '3031 - 75 - 2';

UPDATE "chemical" SET "hap_number" = '99', "hap_name" = 'Hydroquinone', "epa_evidence_weight" = NULL
WHERE "cas_number" = '123 - 31 - 9';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Hydroxy-4-methyl-2-pentanone, 4-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '123 - 42 - 2';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = 'Indeno[1,2,3-c,d]pyrene', "epa_evidence_weight" = 'B2'
WHERE "cas_number" = '193 - 39 - 5';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Iodomethane', "epa_evidence_weight" = NULL
WHERE "cas_number" = '74 - 88 - 4';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Iron chloride', "epa_evidence_weight" = NULL
WHERE "cas_number" = '27846 - 09 - 9';

UPDATE "chemical" SET "hap_number" = '100', "hap_name" = 'Isophorone', "epa_evidence_weight" = NULL
WHERE "cas_number" = '78 - 59 - 1';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Isophorone Diisocyanate', "epa_evidence_weight" = NULL
WHERE "cas_number" = '4098 - 71 - 9';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'isovaleraldehyde', "epa_evidence_weight" = NULL
WHERE "cas_number" = '590 - 86 - 3';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Lauric acid', "epa_evidence_weight" = NULL
WHERE "cas_number" = '143 - 07 - 7';

UPDATE "chemical" SET "hap_number" = '182', "hap_name" = 'Lead', "epa_evidence_weight" = 'B2'
WHERE "cas_number" = '7439 - 92 - 1';

UPDATE "chemical" SET "hap_number" = '101', "hap_name" = 'Lindane', "epa_evidence_weight" = 'B2-C'
WHERE "cas_number" = '58 - 89 - 9';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Magnesium', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7439 - 95 - 4';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Malathion', "epa_evidence_weight" = NULL
WHERE "cas_number" = '121 - 75 - 5';

UPDATE "chemical" SET "hap_number" = '102', "hap_name" = 'Maleic anhydride', "epa_evidence_weight" = NULL
WHERE "cas_number" = '108 - 31 - 6';

UPDATE "chemical" SET "hap_number" = '183', "hap_name" = 'Manganese', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7439 - 96 - 5';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Mechloroethamine', "epa_evidence_weight" = NULL
WHERE "cas_number" = '51 - 75 - 2';

UPDATE "chemical" SET "hap_number" = '184', "hap_name" = 'Mercuric chloride', "epa_evidence_weight" = 'C'
WHERE "cas_number" = '7487 - 94 - 7';

UPDATE "chemical" SET "hap_number" = '184', "hap_name" = 'Mercury', "epa_evidence_weight" = 'D'
WHERE "cas_number" = '7439 - 97 - 6';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Methacrylonitrile', "epa_evidence_weight" = NULL
WHERE "cas_number" = '126 - 98 - 7';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Methane', "epa_evidence_weight" = NULL
WHERE "cas_number" = '74 - 82 - 8';

UPDATE "chemical" SET "hap_number" = '103', "hap_name" = 'Methanol', "epa_evidence_weight" = NULL
WHERE "cas_number" = '67 - 56 - 1';

UPDATE "chemical" SET "hap_number" = '104', "hap_name" = 'Methoxychlor', "epa_evidence_weight" = 'D'
WHERE "cas_number" = '72 - 43 - 5';

UPDATE "chemical" SET "hap_number" = '181', "hap_name" = 'Methoxyethanol, 2-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '109 - 86 - 4';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Methyl 4-hydroxybenzoate', "epa_evidence_weight" = NULL
WHERE "cas_number" = '99 - 76 - 3';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Methyl acetate', "epa_evidence_weight" = NULL
WHERE "cas_number" = '79 - 20 - 9';

UPDATE "chemical" SET "hap_number" = '105', "hap_name" = 'Methyl bromide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '74 - 83 - 9';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Methyl butyrate', "epa_evidence_weight" = NULL
WHERE "cas_number" = '623 - 42 - 7';

UPDATE "chemical" SET "hap_number" = '106', "hap_name" = 'Methyl chloride', "epa_evidence_weight" = NULL
WHERE "cas_number" = '74 - 87 - 3';

UPDATE "chemical" SET "hap_number" = '108', "hap_name" = 'Methyl ethyl ketone', "epa_evidence_weight" = NULL
WHERE "cas_number" = '78 - 93 - 3';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Methyl Isobutyl Carbinol', "epa_evidence_weight" = NULL
WHERE "cas_number" = '108 - 11 - 2';

UPDATE "chemical" SET "hap_number" = '111', "hap_name" = 'Methyl isobutyl ketone', "epa_evidence_weight" = NULL
WHERE "cas_number" = '108 - 10 - 1';

UPDATE "chemical" SET "hap_number" = '112', "hap_name" = 'Methyl isocyanate', "epa_evidence_weight" = NULL
WHERE "cas_number" = '624 - 83 - 9';

UPDATE "chemical" SET "hap_number" = '184', "hap_name" = 'Methyl Mercury', "epa_evidence_weight" = 'C'
WHERE "cas_number" = '22967 - 92 - 6';

UPDATE "chemical" SET "hap_number" = '113', "hap_name" = 'Methyl methacrylate', "epa_evidence_weight" = NULL
WHERE "cas_number" = '80 - 62 - 6';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Methyl Parathion', "epa_evidence_weight" = NULL
WHERE "cas_number" = '298 - 00 - 0';

UPDATE "chemical" SET "hap_number" = '114', "hap_name" = 'Methyl tert-butyl ether', "epa_evidence_weight" = NULL
WHERE "cas_number" = '1634 - 04 - 4';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Methyl-1-propen-1-one, 2-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '598 - 26 - 5';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Methyl-2,3-dihydrofuran, 4-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '34314 - 83 - 5';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Methyl-2-cyclohexen-1-one, 3-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '1193 - 18 - 6';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Methyl-4-penten-2-one, 4-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '3744 - 02 - 3';

UPDATE "chemical" SET "hap_number" = '118', "hap_name" = 'Methylene bisbenzeneamine, 4,4''-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '101 - 77 - 9';

UPDATE "chemical" SET "hap_number" = '116', "hap_name" = 'Methylene chloride', "epa_evidence_weight" = NULL
WHERE "cas_number" = '75 - 09 - 2';

UPDATE "chemical" SET "hap_number" = '117', "hap_name" = 'Methylene diphenyl diisocyanate', "epa_evidence_weight" = NULL
WHERE "cas_number" = '101 - 68 - 8';

UPDATE "chemical" SET "hap_number" = '115', "hap_name" = 'Methylenebis-(2-Chlorobenzenamine), 4,4''', "epa_evidence_weight" = NULL
WHERE "cas_number" = '101 - 14 - 4';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Methylenebis(N,N-Dimethylaniline), 4,4''', "epa_evidence_weight" = NULL
WHERE "cas_number" = '101 - 61 - 1';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = 'Methylnaphthalene, 1-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '90 - 12 - 0';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = '2-Methylnaphthalene', "epa_evidence_weight" = 'InI'
WHERE "cas_number" = '91 - 57 - 6';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'methylphenol, 4-Chloro-3-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '59 - 50 - 7';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'methylphosphonothioic acid S-[2-[bis(1-methylethyl)amino]ethyl] O-ethyl ester', "epa_evidence_weight" = NULL
WHERE "cas_number" = '50782 - 69 - 9';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Molybdenum', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7439 - 98 - 7';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Mustard Gas', "epa_evidence_weight" = NULL
WHERE "cas_number" = '505 - 60 - 2';

UPDATE "chemical" SET "hap_number" = '59', "hap_name" = 'N,N-dimethylaniline', "epa_evidence_weight" = NULL
WHERE "cas_number" = '121 - 69 - 7';

UPDATE "chemical" SET "hap_number" = '119', "hap_name" = 'Naphthalene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '91 - 20 - 3';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Naphthol, 2-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '135 - 19 - 3';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Naphthylamine, 1-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '134 - 32 - 7';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'n-Hexanoic Acid', "epa_evidence_weight" = NULL
WHERE "cas_number" = '142 - 62 - 1';

UPDATE "chemical" SET "hap_number" = '186', "hap_name" = 'Nickel', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7440 - 02 - 0';

UPDATE "chemical" SET "hap_number" = '186', "hap_name" = 'Nickel oxide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '1313 - 99 - 1';

UPDATE "chemical" SET "hap_number" = '186', "hap_name" = 'Nickel refinery dust', "epa_evidence_weight" = NULL
WHERE "cas_number" = 'NI_DUST';
 
UPDATE "chemical" SET "hap_number" = '186', "hap_name" = 'Nickel subsulfide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '12035 - 72 - 2';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Nitric acid', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7697 - 37 - 2';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Nitric Oxide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '10102 - 43 - 9';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Nitrilotriacetic acid', "epa_evidence_weight" = NULL
WHERE "cas_number" = '139 - 13 - 9';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Nitroaniline, 2-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '88 - 74 - 4';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Nitroaniline, 3-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '99 - 09 - 2';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Nitroaniline, 4-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '100 - 01 - 6';

UPDATE "chemical" SET "hap_number" = '120', "hap_name" = 'nitro-Benzene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '98 - 95 - 3';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Nitrobiphenyl, 4-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '92 - 93 - 3';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Nitrodiphenylamine, 2-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '119 - 75 - 5';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Nitrofen', "epa_evidence_weight" = NULL
WHERE "cas_number" = '1836 - 75 - 5';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Nitrogen dioxide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '10102 - 44 - 0';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Nitroglycerine', "epa_evidence_weight" = NULL
WHERE "cas_number" = '55 - 63 - 0';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'nitroguanidine', "epa_evidence_weight" = NULL
WHERE "cas_number" = '556 - 88 - 7';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Nitronaphthalene, 2-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '581 - 89 - 5';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Nitro-o-anisidine, 5-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '99 - 59 - 2';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Nitrophenol, 2-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '88 - 75 - 5';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Nitrophenol, 3-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '554 - 84 - 7';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Nitrophenol, 4-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '100 - 02 - 7';

UPDATE "chemical" SET "hap_number" = '123', "hap_name" = 'Nitropropane, 2-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '79 - 46 - 9';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = 'Nitropyrene, 1-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '5522 - 43 - 0';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Nitroso(methyl)vinylamine, N-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '4549 - 40 - 0';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Nitrosodibutylamine, N-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '924 - 16 - 3';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Nitrosodiethanolamine, N-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '1116 - 54 - 7';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Nitrosodiphenylamine, 4-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '156 - 10 - 5';

UPDATE "chemical" SET "hap_number" = '126', "hap_name" = 'Nitrosomorpholine, N-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '59 - 89 - 2';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Nitroso-N-Ethylurea, N-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '759 - 73 - 9';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Nitrosonornicotine, N''-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '16543 - 55 - 8';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'N-Nitrosodiethylamine', "epa_evidence_weight" = NULL
WHERE "cas_number" = '55 - 18 - 5';

UPDATE "chemical" SET "hap_number" = '125', "hap_name" = 'N-Nitrosodimethylamine', "epa_evidence_weight" = NULL
WHERE "cas_number" = '62 - 75 - 9';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'N-Nitrosodiphenylamine', "epa_evidence_weight" = NULL
WHERE "cas_number" = '86 - 30 - 6';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'N-nitrosodipropylamine', "epa_evidence_weight" = NULL
WHERE "cas_number" = '621 - 64 - 7';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'N-Nitroso-N-Methylurea Nitroso-N-Methylurea, N-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '684 - 93 - 5';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'N-Nitrosopiperidine', "epa_evidence_weight" = NULL
WHERE "cas_number" = '100 - 75 - 4';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Nonane', "epa_evidence_weight" = NULL
WHERE "cas_number" = '111 - 84 - 2';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Nonanol', "epa_evidence_weight" = NULL
WHERE "cas_number" = '143 - 08 - 8';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = 'Octabromodiphenyl ether', "epa_evidence_weight" = 'D'
WHERE "cas_number" = '32536 - 52 - 0';

UPDATE "chemical" SET "hap_number" = '148', "hap_name" = '1,2,3,4,6,7,8,9-Octachlorodibenzo-p-dioxin', "epa_evidence_weight" = NULL
WHERE "cas_number" = '3268 - 87 - 9';

UPDATE "chemical" SET "hap_number" = '148', "hap_name" = '1,2,3,4,6,7,8,9-Octachlorodibenzofuran', "epa_evidence_weight" = NULL
WHERE "cas_number" = '39001 - 02 - 0';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Octahydro-1,3,5,7-Tetranitro-1,3,5,7-Tetrazocine', "epa_evidence_weight" = NULL
WHERE "cas_number" = '2691 - 41 - 0';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Octanedione, 2,5-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '3214 - 41 - 3';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Octyl alcohol', "epa_evidence_weight" = NULL
WHERE "cas_number" = '111 - 87 - 5';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Oxybisbenzenamine, 4,4''-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '101 - 80 - 4';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Palmitic acid', "epa_evidence_weight" = NULL
WHERE "cas_number" = '57 - 10 - 3';

UPDATE "chemical" SET "hap_number" = '127', "hap_name" = 'Parathion', "epa_evidence_weight" = NULL
WHERE "cas_number" = '56 - 38 - 2';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'PCB-chlorobiphenyl, 4-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '2051 - 62 - 9';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'PCB-hexachlorobiphenyl', "epa_evidence_weight" = NULL
WHERE "cas_number" = '26601 - 64 - 9';

UPDATE "chemical" SET "hap_number" = '148', "hap_name" = '1,2,3,7,8-Pentachlorodibenzo-p-dioxin', "epa_evidence_weight" = NULL
WHERE "cas_number" = '40321 - 76 - 4';

UPDATE "chemical" SET "hap_number" = '148', "hap_name" = 'PentaCDD, 2,3,7,8-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '36088 - 22 - 9';

UPDATE "chemical" SET "hap_number" = '148', "hap_name" = '1,2,3,7,8-Pentachlorodibenzofuran', "epa_evidence_weight" = NULL
WHERE "cas_number" = '57117 - 41 - 6';

UPDATE "chemical" SET "hap_number" = '148', "hap_name" = '2,3,4,7,8-Pentachlorodibenzofuran', "epa_evidence_weight" = NULL
WHERE "cas_number" = '57117 - 31 - 4';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Pentachlorobenzene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '608 - 93 - 5';

UPDATE "chemical" SET "hap_number" = '128', "hap_name" = 'Pentachloronitrobenzene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '82 - 68 - 8';

UPDATE "chemical" SET "hap_number" = '129', "hap_name" = 'pentachloro-Phenol', "epa_evidence_weight" = NULL
WHERE "cas_number" = '87 - 86 - 5';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Pentanol', "epa_evidence_weight" = NULL
WHERE "cas_number" = '71 - 41 - 0';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Penten-2-ol, 3-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '1569 - 50 - 2';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = 'Phenanthrene', "epa_evidence_weight" = 'D'
WHERE "cas_number" = '85 - 01 - 8';

UPDATE "chemical" SET "hap_number" = '130', "hap_name" = 'Phenol', "epa_evidence_weight" = NULL
WHERE "cas_number" = '108 - 95 - 2';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Phenol, 4,6-Dinitro-2-Methyl-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '534 - 52 - 1';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Phenyl-1,2-propanedione, 1-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '579 - 07 - 7';

UPDATE "chemical" SET "hap_number" = '184', "hap_name" = 'Phenylmercuric acetate', "epa_evidence_weight" = NULL
WHERE "cas_number" = '62 - 38 - 4';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Phorate', "epa_evidence_weight" = NULL
WHERE "cas_number" = '298 - 02 - 2';

UPDATE "chemical" SET "hap_number" = '132', "hap_name" = 'Phosgene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '75 - 44 - 5';

UPDATE "chemical" SET "hap_number" = '133', "hap_name" = 'Phosphine', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7803 - 51 - 2';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Phosphoric acid', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7664 - 38 - 2';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Phosphoric acid diisodecyl phenyl ester', "epa_evidence_weight" = NULL
WHERE "cas_number" = '51363 - 64 - 5';

UPDATE "chemical" SET "hap_number" = '134', "hap_name" = 'Phosphorus', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7723 - 14 - 0';

UPDATE "chemical" SET "hap_number" = '135', "hap_name" = 'Phthalic anhydride', "epa_evidence_weight" = NULL
WHERE "cas_number" = '85 - 44 - 9';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = 'Polybrominated biphenyls', "epa_evidence_weight" = 'B2'
WHERE "cas_number" = '59536 - 65 - 1';

UPDATE "chemical" SET "hap_number" = '136', "hap_name" = 'polychlorinated biphenyls', "epa_evidence_weight" = 'B2'
WHERE "cas_number" = '1336 - 36 - 3';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Potassium', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7440 - 09 - 7';

UPDATE "chemical" SET "hap_number" = '180', "hap_name" = 'Potassium cyanide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '151 - 50 - 8';

UPDATE "chemical" SET "hap_number" = '180', "hap_name" = 'Potassium silver cyanide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '506 - 61 - 6';

UPDATE "chemical" SET "hap_number" = '131', "hap_name" = 'p-Phenylenediamine', "epa_evidence_weight" = NULL
WHERE "cas_number" = '106 - 50 - 3';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Pronamide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '23950 - 58 - 5';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Propanol', "epa_evidence_weight" = NULL
WHERE "cas_number" = '71 - 23 - 8';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Propanol, 2- (isopropanol)', "epa_evidence_weight" = NULL
WHERE "cas_number" = '67 - 63 - 0';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Propiolactone, beta-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '57 - 57 - 8';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Propionaldehyde', "epa_evidence_weight" = NULL
WHERE "cas_number" = '123 - 38 - 6';

UPDATE "chemical" SET "hap_number" = '140', "hap_name" = 'Propoxur', "epa_evidence_weight" = NULL
WHERE "cas_number" = '114 - 26 - 1';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Propylene Glycol Monomethyl Ether', "epa_evidence_weight" = NULL
WHERE "cas_number" = '107 - 98 - 2';

UPDATE "chemical" SET "hap_number" = '142', "hap_name" = 'Propylene oxide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '75 - 56 - 9';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Propylenimine', "epa_evidence_weight" = NULL
WHERE "cas_number" = '75 - 55 - 8';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = 'Pyrene', "epa_evidence_weight" = 'D'
WHERE "cas_number" = '129 - 00 - 0';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Pyridine', "epa_evidence_weight" = NULL
WHERE "cas_number" = '110 - 86 - 1';

UPDATE "chemical" SET "hap_number" = '144', "hap_name" = 'Quinoline', "epa_evidence_weight" = NULL
WHERE "cas_number" = '91 - 22 - 5';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Resorcinol', "epa_evidence_weight" = NULL
WHERE "cas_number" = '108 - 46 - 3';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Ronnel', "epa_evidence_weight" = NULL
WHERE "cas_number" = '299 - 84 - 3';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Safrole', "epa_evidence_weight" = NULL
WHERE "cas_number" = '94 - 59 - 7';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Salicylic acid', "epa_evidence_weight" = NULL
WHERE "cas_number" = '69 - 72 - 7';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Sarin', "epa_evidence_weight" = NULL
WHERE "cas_number" = '107 - 44 - 8';

UPDATE "chemical" SET "hap_number" = '189', "hap_name" = 'Selenious acid', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7783 - 00 - 8';

UPDATE "chemical" SET "hap_number" = '189', "hap_name" = 'Selenium', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7782 - 49 - 2';

UPDATE "chemical" SET "hap_number" = '189', "hap_name" = 'Selenium dioxide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7446 - 08 - 4';

UPDATE "chemical" SET "hap_number" = '189', "hap_name" = 'Selenium disulfide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7488 - 56 - 4';

UPDATE "chemical" SET "hap_number" = '189', "hap_name" = 'Selenium sulfide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7446 - 34 - 6';

UPDATE "chemical" SET "hap_number" = '189', "hap_name" = 'Selenourea', "epa_evidence_weight" = NULL
WHERE "cas_number" = '630 - 10 - 4';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Silane, fluorotrimethyl', "epa_evidence_weight" = NULL
WHERE "cas_number" = '420 - 56 - 4';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Silicon', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7440 - 21 - 3';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Silver', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7440 - 22 - 4';

UPDATE "chemical" SET "hap_number" = '180', "hap_name" = 'Silver cyanide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '506 - 64 - 9';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Sodium', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7440 - 23 - 5';

UPDATE "chemical" SET "hap_number" = '180', "hap_name" = 'Sodium cyanide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '143 - 33 - 9';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Strontium', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7440 - 24 - 6';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Strychnine', "epa_evidence_weight" = NULL
WHERE "cas_number" = '57 - 24 - 9';

UPDATE "chemical" SET "hap_number" = '146', "hap_name" = 'Styrene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '100 - 42 - 5';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Sulfur dioxide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7446 - 09 - 5';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Sulfuric acid', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7664 - 93 - 9';

UPDATE "chemical" SET "hap_number" = '101', "hap_name" = 'technical Hexachlorocyclohexane (HCH)', "epa_evidence_weight" = 'B2'
WHERE "cas_number" = '608 - 73 - 1';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'tert-butyl hydroperoxide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '75 - 91 - 2';

UPDATE "chemical" SET "hap_number" = '148', "hap_name" = '2,3,7,8-Tetrachlorodibenzo-p-dioxin', "epa_evidence_weight" = 'B2'
WHERE "cas_number" = '1746 - 01 - 6';

UPDATE "chemical" SET "hap_number" = '148', "hap_name" = '2,3,7,8-Tetrachlorodibenzofuran', "epa_evidence_weight" = NULL
WHERE "cas_number" = '51207 - 31 - 9';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Tetrachlorobenzene, 1,2,4,5-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '95 - 94 - 3';

UPDATE "chemical" SET "hap_number" = '148', "hap_name" = 'Tetrachloro-Dibenzofuran, 1,2,7,8-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '58802 - 20 - 3';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Tetrachloroethane, 1,1,1,2-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '630 - 20 - 6';

UPDATE "chemical" SET "hap_number" = '149', "hap_name" = 'Tetrachloroethane, 1,1,2,2-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '79 - 34 - 5';

UPDATE "chemical" SET "hap_number" = '150', "hap_name" = 'Tetrachloroethylene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '127 - 18 - 4';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Tetrachlorophenol, 2,3,4,6-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '58 - 90 - 2';

UPDATE "chemical" SET "hap_number" = '182', "hap_name" = 'Tetraethyl lead', "epa_evidence_weight" = NULL
WHERE "cas_number" = '78 - 00 - 2';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Tetrahydro-2,5-dimethyl furan', "epa_evidence_weight" = NULL
WHERE "cas_number" = '1003 - 38 - 9';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Tetrahydrofuran', "epa_evidence_weight" = NULL
WHERE "cas_number" = '109 - 99 - 9';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Tetramethyldiaminobenzophenone', "epa_evidence_weight" = NULL
WHERE "cas_number" = '90 - 94 - 8';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'tetryl', "epa_evidence_weight" = NULL
WHERE "cas_number" = '479 - 45 - 8';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Thallium', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7440 - 28 - 0';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Thioacetamide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '62 - 55 - 5';

UPDATE "chemical" SET "hap_number" = '180', "hap_name" = 'Thiocyanic acid, 2-(benzothiazolylthio) methyl est', "epa_evidence_weight" = NULL
WHERE "cas_number" = '21564 - 17 - 0';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Thiodianiline, 4,4''-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '139 - 65 - 1';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Thiourea', "epa_evidence_weight" = NULL
WHERE "cas_number" = '62 - 56 - 6';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Thymol', "epa_evidence_weight" = NULL
WHERE "cas_number" = '89 - 83 - 8';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Tin', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7440 - 31 - 5';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Titanium', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7440 - 32 - 6';

UPDATE "chemical" SET "hap_number" = '151', "hap_name" = 'Titanium tetrachloride', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7550 - 45 - 0';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Tolbutamide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '64 - 77 - 7';

UPDATE "chemical" SET "hap_number" = '152', "hap_name" = 'Toluene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '108 - 88 - 3';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Toluidine hydrochloride, ortho-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '636 - 21 - 5';

UPDATE "chemical" SET "hap_number" = '155', "hap_name" = 'Toluidine, o-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '95 - 53 - 4';

UPDATE "chemical" SET "hap_number" = '156', "hap_name" = 'Toxaphene', "epa_evidence_weight" = 'B2'
WHERE "cas_number" = '8001 - 35 - 2';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'trans-1,2-Dichloro-cyclohexane', "epa_evidence_weight" = NULL
WHERE "cas_number" = '822 - 86 - 6';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'trans-1,3-Dichloropropene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '10061 - 02 - 6';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Trenimon', "epa_evidence_weight" = NULL
WHERE "cas_number" = '68 - 76 - 8';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Triacetin', "epa_evidence_weight" = NULL
WHERE "cas_number" = '102 - 76 - 1';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Tributyl phosphate', "epa_evidence_weight" = NULL
WHERE "cas_number" = '126 - 73 - 8';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Trichlorobenzene, 1,2,3-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '87 - 61 - 6';

UPDATE "chemical" SET "hap_number" = '157', "hap_name" = 'Trichlorobenzene, 1,2,4-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '120 - 82 - 1';

UPDATE "chemical" SET "hap_number" = '107', "hap_name" = 'Trichloroethane, 1,1,1-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '71 - 55 - 6';

UPDATE "chemical" SET "hap_number" = '158', "hap_name" = 'Trichloroethane, 1,1,2-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '79 - 00 - 5';

UPDATE "chemical" SET "hap_number" = '159', "hap_name" = 'Trichloroethylene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '79 - 01 - 6';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Trichlorofluoromethane', "epa_evidence_weight" = NULL
WHERE "cas_number" = '75 - 69 - 4';

UPDATE "chemical" SET "hap_number" = '160', "hap_name" = 'Trichlorophenol, 2,4,5-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '95 - 95 - 4';

UPDATE "chemical" SET "hap_number" = '161', "hap_name" = 'Trichlorophenol, 2,4,6-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '88 - 06 - 2';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Trichloropropane, 1,2,3-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '96 - 18 - 4';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Tridecane, n-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '629 - 50 - 5';

UPDATE "chemical" SET "hap_number" = '162', "hap_name" = 'Triethylamine', "epa_evidence_weight" = NULL
WHERE "cas_number" = '121 - 44 - 8';

UPDATE "chemical" SET "hap_number" = '163', "hap_name" = 'Trifluralin', "epa_evidence_weight" = 'C'
WHERE "cas_number" = '1582 - 09 - 8';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Trimethyl-2,5,8,11-tetraoxatetradecan-13-ol, 4,7,10-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '20324 - 34 - 9';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Trimethyl-2-hexene, 4,4,5-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '55702 - 61 - 9';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Trimethylbenzene, 1,2,3-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '526 - 73 - 8';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Trimethylbenzene, 1,3,4-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '95 - 63 - 6';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Trimethylbenzene, 1,3,5-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '108 - 67 - 8';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Trimethyldecane, 2,2,3-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '62338 - 09 - 4';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Trinitrobenzene, 1,3,5-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '99 - 35 - 4';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Trinitrotoluene, 2,4,6-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '118 - 96 - 7';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Tris(2,3-dibromopropyl) phosphate', "epa_evidence_weight" = NULL
WHERE "cas_number" = '126 - 72 - 7';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Tris(2-chloroethyl)phosphate', "epa_evidence_weight" = NULL
WHERE "cas_number" = '115 - 96 - 8';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'TSP', "epa_evidence_weight" = NULL
WHERE "cas_number" = '12789 - 66 - 1';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Undecane', "epa_evidence_weight" = NULL
WHERE "cas_number" = '1120 - 21 - 4';

UPDATE "chemical" SET "hap_number" = '188', "hap_name" = 'Uranium compounds', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7440 - 61 - 1';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Uranium trioxide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '1344 - 58 - 7';

UPDATE "chemical" SET "hap_number" = '188', "hap_name" = 'Uranium, soluble salts', "epa_evidence_weight" = NULL
WHERE "cas_number" = 'URANSOLS';
 
UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Urea', "epa_evidence_weight" = NULL
WHERE "cas_number" = '57 - 13 - 6';

UPDATE "chemical" SET "hap_number" = '78', "hap_name" = 'Urethane', "epa_evidence_weight" = NULL
WHERE "cas_number" = '51 - 79 - 6';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Vanadium', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7440 - 62 - 2';

UPDATE "chemical" SET "hap_number" = '165', "hap_name" = 'Vinyl acetate', "epa_evidence_weight" = NULL
WHERE "cas_number" = '108 - 05 - 4';

UPDATE "chemical" SET "hap_number" = '166', "hap_name" = 'Vinyl bromide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '593 - 60 - 2';

UPDATE "chemical" SET "hap_number" = '167', "hap_name" = 'Vinyl chloride', "epa_evidence_weight" = NULL
WHERE "cas_number" = '75 - 01 - 4';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Water', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7732 - 18 - 5';

UPDATE "chemical" SET "hap_number" = '171', "hap_name" = 'Xylene, meta-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '108 - 38 - 3';

UPDATE "chemical" SET "hap_number" = '170', "hap_name" = 'Xylene, ortho-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '95 - 47 - 6';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Xylene, para-', "epa_evidence_weight" = NULL
WHERE "cas_number" = '106 - 42 - 3';

UPDATE "chemical" SET "hap_number" = '169', "hap_name" = 'Xylenes', "epa_evidence_weight" = NULL
WHERE "cas_number" = '1330 - 20 - 7';

UPDATE "chemical" SET "hap_number" = NULL, "hap_name" = 'Zinc', "epa_evidence_weight" = NULL
WHERE "cas_number" = '7440 - 66 - 6';

UPDATE "chemical" SET "hap_number" = '180', "hap_name" = 'Zinc cyanide', "epa_evidence_weight" = NULL
WHERE "cas_number" = '557 - 21 - 1';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = 'Perylene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '198 - 55 - 0';

UPDATE "chemical" SET "hap_number" = '187', "hap_name" = 'Retene', "epa_evidence_weight" = NULL
WHERE "cas_number" = '483 - 65 - 8';

COMMIT;

