-- Creating dummy User/Role ORM
CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> 12f3b3bc93f9

CREATE TABLE chemical (
    name VARCHAR(120) NOT NULL, 
    cas_number VARCHAR(120) NOT NULL, 
    hap_number VARCHAR(255), 
    hap_name VARCHAR(255), 
    epa_evidence_weight VARCHAR(255), 
    category VARCHAR(240), 
    id INTEGER NOT NULL, 
    PRIMARY KEY (id), 
    UNIQUE (cas_number)
);

CREATE TABLE formula (
    equation VARCHAR NOT NULL, 
    description VARCHAR(240), 
    id INTEGER NOT NULL, 
    PRIMARY KEY (id)
);

CREATE TABLE transport_process (
    name VARCHAR(240) NOT NULL, 
    algorithm_id INTEGER NOT NULL, 
    category VARCHAR(240) NOT NULL, 
    requirements VARCHAR, 
    output_chemical_id INTEGER, 
    id INTEGER NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(output_chemical_id) REFERENCES chemical (id), 
    FOREIGN KEY(algorithm_id) REFERENCES formula (id), 
    UNIQUE (name)
);

CREATE TABLE media (
    name VARCHAR(120) NOT NULL, 
    parent_id INTEGER, 
    can_emit BOOLEAN NOT NULL, 
    can_absorb BOOLEAN NOT NULL, 
    id INTEGER NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(parent_id) REFERENCES media (id), 
    UNIQUE (name)
);

CREATE TABLE parameter_domain (
    name VARCHAR(120) NOT NULL, 
    entity_type VARCHAR(120) NOT NULL, 
    requirements VARCHAR, 
    description VARCHAR(240), 
    id INTEGER NOT NULL, 
    PRIMARY KEY (id), 
    UNIQUE (entity_type, requirements)
);

CREATE TABLE role (
    id INTEGER NOT NULL, 
    name VARCHAR(80), 
    description VARCHAR(255), 
    PRIMARY KEY (id), 
    UNIQUE (name)
);

CREATE TABLE user (
    active BOOLEAN NOT NULL, 
    id INTEGER NOT NULL, 
    email VARCHAR(255) NOT NULL, 
    first_name VARCHAR(255), 
    last_name VARCHAR(255), 
    company_name VARCHAR(255), 
    password_hash VARCHAR(128), 
    confirmed_at DATETIME, 
    fs_uniquifier VARCHAR(65), 
    last_login_at DATETIME, 
    current_login_at DATETIME, 
    last_login_ip VARCHAR(40), 
    current_login_ip VARCHAR(40), 
    login_count INTEGER, 
    PRIMARY KEY (id), 
    UNIQUE (email)
);

CREATE TABLE formula_argument (
    formula_id INTEGER NOT NULL, 
    name VARCHAR(60) NOT NULL, 
    domain_id INTEGER, 
    id INTEGER NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(domain_id) REFERENCES parameter_domain (id), 
    FOREIGN KEY(formula_id) REFERENCES formula (id), 
    UNIQUE (formula_id, name)
);

CREATE TABLE parameter_definition (
    variable_name VARCHAR(150) NOT NULL, 
    full_name VARCHAR(120) NOT NULL, 
    description VARCHAR(240), 
    domain_id INTEGER NOT NULL, 
    default_value FLOAT, 
    default_unit VARCHAR(150), 
    default_formula_id INTEGER, 
    id INTEGER NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(default_formula_id) REFERENCES formula (id), 
    FOREIGN KEY(domain_id) REFERENCES parameter_domain (id)
);

CREATE TABLE roles_users (
    user_id INTEGER, 
    role_id INTEGER, 
    FOREIGN KEY(role_id) REFERENCES role (id), 
    FOREIGN KEY(user_id) REFERENCES user (id)
);

CREATE TABLE scenario (
    created DATETIME NOT NULL, 
    updated DATETIME, 
    name VARCHAR(120) NOT NULL, 
    description VARCHAR(255), 
    creator_id INTEGER NOT NULL, 
    id INTEGER NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(creator_id) REFERENCES user (id)
);

-- CREATE TABLE team (
--     scenario_id INTEGER NOT NULL, 
--     member_id INTEGER NOT NULL, 
--     id INTEGER NOT NULL, 
--     PRIMARY KEY (id), 
--     FOREIGN KEY(member_id) REFERENCES user (id), 
--     FOREIGN KEY(scenario_id) REFERENCES scenario (id), 
--     UNIQUE (scenario_id, member_id)
-- );

CREATE TABLE custom_parameter (
    definition_id INTEGER NOT NULL, 
    scenario_id INTEGER NOT NULL, 
    requirements VARCHAR, 
    value FLOAT, 
    unit VARCHAR(150), 
    formula_id INTEGER, 
    id INTEGER NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(definition_id) REFERENCES parameter_definition (id), 
    FOREIGN KEY(formula_id) REFERENCES formula (id), 
    FOREIGN KEY(scenario_id) REFERENCES scenario (id)
);

CREATE TABLE parcel (
    name VARCHAR(120) NOT NULL,
    description VARCHAR(250),
    scenario_id INTEGER NOT NULL,
    vertices JSON NOT NULL,
    id INTEGER NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(scenario_id) REFERENCES scenario (id),
    UNIQUE (scenario_id, name)
);

CREATE TABLE scenario_chemicals (
    scenario_id INTEGER, 
    chemical_id INTEGER, 
    FOREIGN KEY(chemical_id) REFERENCES chemical (id), 
    FOREIGN KEY(scenario_id) REFERENCES scenario (id), 
    UNIQUE (scenario_id, chemical_id)
);

CREATE TABLE volume_element (
    name VARCHAR(120) NOT NULL, 
    parcel_id INTEGER NOT NULL, 
    top FLOAT NOT NULL, 
    bottom FLOAT NOT NULL, 
    id INTEGER NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(parcel_id) REFERENCES parcel (id), 
    UNIQUE (parcel_id, name)
);

CREATE TABLE compartment (
    name VARCHAR(120) NOT NULL, 
    volume_element_id INTEGER NOT NULL, 
    media_id INTEGER NOT NULL, 
    id INTEGER NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(media_id) REFERENCES media (id), 
    FOREIGN KEY(volume_element_id) REFERENCES volume_element (id), 
    UNIQUE (volume_element_id, name)
);

CREATE TABLE compartment_link (
    sender_id INTEGER NOT NULL, 
    receiver_id INTEGER NOT NULL, 
    id INTEGER NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(receiver_id) REFERENCES compartment (id), 
    FOREIGN KEY(sender_id) REFERENCES compartment (id), 
    UNIQUE (sender_id, receiver_id)
);

CREATE TABLE scenario_load_run_proc (
    id INTEGER NOT NULL, 
    load_status VARCHAR(140), 
    run_status VARCHAR(140), 
    run_datetime DATETIME, 
    result_file_nt VARCHAR(255), 
    result_file_conc VARCHAR(255), 
    result_file_tm VARCHAR(255),
    result_nt VARCHAR, 
    result_conc VARCHAR, 
    execution_arn VARCHAR(255), 
    scenario_id INTEGER NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(scenario_id) REFERENCES scenario (id)
);

CREATE TABLE api_key (
    active BOOLEAN NOT NULL, 
    value VARCHAR(255) NOT NULL, 
    user_id INTEGER NOT NULL, 
    id INTEGER NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(user_id) REFERENCES "user" (id), 
    UNIQUE (value)
);

CREATE TABLE scenario_permissions (
    user_id INTEGER NOT NULL, 
    scenario_id INTEGER NOT NULL, 
    level INTEGER NOT NULL, 
    id INTEGER NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(scenario_id) REFERENCES scenario (id), 
    FOREIGN KEY(user_id) REFERENCES "user" (id), 
    UNIQUE (user_id, scenario_id)
);

-- Now handled in the full_db backup script
INSERT INTO alembic_version (version_num) VALUES ('81e92f9ff252');

CREATE TABLE mirc_scenario (
    id INTEGER NOT NULL, 
    name VARCHAR(255) NOT NULL, 
    is_builtin BOOLEAN NOT NULL, 
    notes VARCHAR(800), 
    parent_id INTEGER,  
    PRIMARY KEY (id), 
    FOREIGN KEY(parent_id) REFERENCES mirc_scenario (id), 
);

CREATE TABLE mirc_scenario_permissions (
    id INTEGER NOT NULL, 
    user_id INTEGER NOT NULL, 
    mirc_scenario_id INTEGER NOT NULL, 
    level INTEGER NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(mirc_scenario_id) REFERENCES mirc_scenario (id), 
    FOREIGN KEY(user_id) REFERENCES "user" (id), 
    UNIQUE (user_id, mirc_scenario_id)
);

CREATE TABLE mirc_simulation (
    created DATETIME NOT NULL, 
    updated DATETIME, 
    name VARCHAR(120) NOT NULL, 
    description VARCHAR(800), 
    trim_scenario_id INTEGER NOT NULL, 
    mirc_scenario_id INTEGER NOT NULL, 
    chemical_id INTEGER NOT NULL, 
    use_baf BOOLEAN NOT NULL, 
    id INTEGER NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(trim_scenario_id) REFERENCES scenario (id), 
    FOREIGN KEY(mirc_scenario_id) REFERENCES mirc_scenario (id), 
    FOREIGN KEY(chemical_id) REFERENCES chemical (id)
);

CREATE TABLE mirc_life_stage (
    name VARCHAR(255) NOT NULL, 
    duration FLOAT, 
    duration_unit VARCHAR(255), 
    id INTEGER NOT NULL,  
    PRIMARY KEY (id), 
    UNIQUE (name)
);

CREATE TABLE mirc_percentile (
    name VARCHAR(255) NOT NULL, 
    id INTEGER NOT NULL,  
    PRIMARY KEY (id), 
    UNIQUE (name)
);

CREATE TABLE mirc_product (
    name VARCHAR(255) NOT NULL, 
    category_id INTEGER, 
    is_food BOOLEAN NOT NULL, 
    is_feed BOOLEAN NOT NULL, 
    id INTEGER NOT NULL,  
    PRIMARY KEY (id), 
    FOREIGN KEY(category_id) REFERENCES mirc_product (id), 
    UNIQUE (name)
);

CREATE TABLE mirc_toxicity_effect (
    description VARCHAR(255), 
    id INTEGER NOT NULL,  
    PRIMARY KEY (id), 
    UNIQUE (description)
);

CREATE TABLE mirc_parameter (
    scenario_id INTEGER NOT NULL, 
    name VARCHAR(255) NOT NULL, 
    variable VARCHAR(36), 
    value FLOAT NOT NULL, 
    unit VARCHAR(36), 
    source VARCHAR(255), 
    notes VARCHAR(255), 
    chemical_id INTEGER, 
    media_id INTEGER, 
    food_id INTEGER, 
    life_stage_id INTEGER, 
    percentile_id INTEGER, 
    id INTEGER NOT NULL,  
    PRIMARY KEY (id), 
    FOREIGN KEY(chemical_id) REFERENCES chemical (id), 
    FOREIGN KEY(food_id) REFERENCES mirc_product (id), 
    FOREIGN KEY(life_stage_id) REFERENCES mirc_life_stage (id), 
    FOREIGN KEY(media_id) REFERENCES mirc_product (id), 
    FOREIGN KEY(percentile_id) REFERENCES mirc_percentile (id), 
    FOREIGN KEY(scenario_id) REFERENCES mirc_scenario (id), 
    UNIQUE (scenario_id, chemical_id, media_id, life_stage_id, percentile_id, food_id, name)
);

CREATE TABLE mirc_parameter_toxicity (
    parameter_id INTEGER, 
    toxicity_effect_id INTEGER, 
    FOREIGN KEY(parameter_id) REFERENCES mirc_parameter (id), 
    FOREIGN KEY(toxicity_effect_id) REFERENCES mirc_toxicity_effect (id)
);

CREATE TABLE mirc_simulation_consumption_breakdown (
    simulation_id INTEGER NOT NULL, 
    subfood_id INTEGER NOT NULL, 
    fraction FLOAT NOT NULL, 
    source VARCHAR(255), 
    id INTEGER NOT NULL,  
    PRIMARY KEY (id), 
    FOREIGN KEY(simulation_id) REFERENCES mirc_simulation (id), 
    FOREIGN KEY(subfood_id) REFERENCES mirc_product (id)
);

CREATE TABLE mirc_simulation_parameter (
    simulation_id INTEGER NOT NULL, 
    variable VARCHAR(60) NOT NULL, 
    name VARCHAR(255), 
    value FLOAT NOT NULL, 
    unit VARCHAR(36), 
    source VARCHAR(255), 
    id INTEGER NOT NULL,  
    PRIMARY KEY (id), 
    FOREIGN KEY(simulation_id) REFERENCES mirc_simulation (id)
);

CREATE TABLE mirc_simulation_percentile (
    simulation_id INTEGER NOT NULL, 
    food_id INTEGER, 
    percentile_id INTEGER NOT NULL, 
    id INTEGER NOT NULL,  
    PRIMARY KEY (id), 
    FOREIGN KEY(food_id) REFERENCES mirc_product (id), 
    FOREIGN KEY(percentile_id) REFERENCES mirc_percentile (id), 
    FOREIGN KEY(simulation_id) REFERENCES mirc_simulation (id)
);

INSERT INTO alembic_version (version_num) VALUES ('e5524555573a');
