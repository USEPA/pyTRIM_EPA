-- V2
-- Drop Database if it exists
DROP DATABASE IF EXISTS `pytrim`;
-- DROP DATABASE IF EXISTS `ebdb`;
-- Create the Database
CREATE DATABASE `pytrim`;
-- CREATE DATABASE `ebdb`;
USE `pytrim`;
-- USE `ebdb`;

-- Creating dummy User/Role ORM
CREATE TABLE `alembic_version` (
    `version_num` VARCHAR(32) NOT NULL, 
    CONSTRAINT `alembic_version_pkc` PRIMARY KEY (`version_num`)
);

-- Running upgrade  -> 12f3b3bc93f9

CREATE TABLE `chemical` (
    `name` VARCHAR(120) NOT NULL, 
    `cas_number` VARCHAR(120) NOT NULL, 
    `category` VARCHAR(240), 
    `id` INTEGER NOT NULL AUTO_INCREMENT, 
    PRIMARY KEY (`id`), 
    UNIQUE (`cas_number`)
);

CREATE TABLE `formula` (
    `equation` VARCHAR(10000) NOT NULL, 
    `description` VARCHAR(240), 
    `id` INTEGER NOT NULL AUTO_INCREMENT, 
    PRIMARY KEY (`id`)
);

CREATE TABLE `transport_process` (
    `name` VARCHAR(240) NOT NULL, 
    `algorithm_id` INTEGER NOT NULL, 
    `category` VARCHAR(240) NOT NULL, 
    `requirements` VARCHAR(10000), 
    `output_chemical_id` INTEGER, 
    `id` INTEGER NOT NULL AUTO_INCREMENT, 
    PRIMARY KEY (`id`), 
    FOREIGN KEY(`output_chemical_id`) REFERENCES chemical (`id`), 
    FOREIGN KEY(`algorithm_id`) REFERENCES formula (`id`), 
    UNIQUE (`name`)
);

CREATE TABLE `media` (
    `name` VARCHAR(120) NOT NULL, 
    `parent_id` INTEGER, 
    `can_emit` BOOLEAN NOT NULL, 
    `can_absorb` BOOLEAN NOT NULL, 
    `id` INTEGER NOT NULL AUTO_INCREMENT, 
    PRIMARY KEY (`id`), 
    FOREIGN KEY(`parent_id`) REFERENCES `media` (`id`), 
    UNIQUE (`name`)
);

CREATE TABLE `parameter_domain` (
    `name` VARCHAR(120) NOT NULL, 
    `entity_type` VARCHAR(120) NOT NULL, 
    `requirements` VARCHAR(500), 
    `description` VARCHAR(240), 
    `id` INTEGER NOT NULL AUTO_INCREMENT, 
    PRIMARY KEY (`id`), 
    UNIQUE (`entity_type`, `requirements`)
);

CREATE TABLE `role` (
    `id` INTEGER NOT NULL AUTO_INCREMENT, 
    `name` VARCHAR(80), 
    `description` VARCHAR(255), 
    PRIMARY KEY (`id`), 
    UNIQUE (`name`)
);

CREATE TABLE `user` (
    `active` BOOLEAN NOT NULL, 
    `id` INTEGER NOT NULL AUTO_INCREMENT, 
    `email` VARCHAR(255) NOT NULL, 
    `first_name` VARCHAR(255), 
    `last_name` VARCHAR(255), 
    `company_name` VARCHAR(255), 
    `password_hash` VARCHAR(128), 
    `confirmed_at` DATETIME, 
    `last_login_at` DATETIME, 
    `current_login_at` DATETIME, 
    `last_login_ip` VARCHAR(40), 
    `current_login_ip` VARCHAR(40), 
    `login_count` INTEGER, 
    PRIMARY KEY (`id`), 
    UNIQUE (`email`)
);

CREATE TABLE `formula_argument` (
    `formula_id` INTEGER NOT NULL, 
    `name` VARCHAR(60) NOT NULL, 
    `domain_id` INTEGER, 
    `id` INTEGER NOT NULL AUTO_INCREMENT, 
    PRIMARY KEY (`id`), 
    FOREIGN KEY(`domain_id`) REFERENCES `parameter_domain` (`id`), 
    FOREIGN KEY(`formula_id`) REFERENCES `formula` (`id`), 
    UNIQUE (`formula_id`, `name`)
);

CREATE TABLE `parameter_definition` (
    `variable_name` VARCHAR(150) NOT NULL, 
    `full_name` VARCHAR(120) NOT NULL, 
    `description` VARCHAR(240), 
    `domain_id` INTEGER NOT NULL, 
    `default_value` DECIMAL(60,15), 
    `default_unit` VARCHAR(150), 
    `default_formula_id` INTEGER, 
    `id` INTEGER NOT NULL AUTO_INCREMENT, 
    PRIMARY KEY (`id`), 
    FOREIGN KEY(`default_formula_id`) REFERENCES `formula` (`id`), 
    FOREIGN KEY(`domain_id`) REFERENCES parameter_domain (`id`)
);

CREATE TABLE `roles_users` (
    `user_id` INTEGER, 
    `role_id` INTEGER, 
    FOREIGN KEY(`role_id`) REFERENCES `role` (`id`), 
    FOREIGN KEY(`user_id`) REFERENCES `user` (`id`)
);

CREATE TABLE `scenario` (
    `created` DATETIME NOT NULL, 
    `updated` DATETIME, 
    `name` VARCHAR(120) NOT NULL, 
    `description` VARCHAR(255), 
    `creator_id` INTEGER NOT NULL, 
    `id` INTEGER NOT NULL AUTO_INCREMENT, 
    PRIMARY KEY (`id`), 
    FOREIGN KEY(`creator_id`) REFERENCES user (`id`)
);

-- CREATE TABLE `team` (
--     `scenario_id` INTEGER NOT NULL, 
--     `member_id` INTEGER NOT NULL, 
--     `id` INTEGER NOT NULL AUTO_INCREMENT, 
--     PRIMARY KEY (`id`), 
--     FOREIGN KEY(`member_id`) REFERENCES user (`id`), 
--     FOREIGN KEY(`scenario_id`) REFERENCES scenario (`id`), 
--     UNIQUE (`scenario_id`, `member_id`)
-- );

CREATE TABLE `custom_parameter` (
    `definition_id` INTEGER NOT NULL, 
    `scenario_id` INTEGER NOT NULL, 
    `requirements` VARCHAR(10000), 
    `value` DECIMAL(60,15), 
    `unit` VARCHAR(150), 
    `formula_id` INTEGER, 
    `id` INTEGER NOT NULL AUTO_INCREMENT, 
    PRIMARY KEY (`id`), 
    FOREIGN KEY(`definition_id`) REFERENCES `parameter_definition` (`id`), 
    FOREIGN KEY(`formula_id`) REFERENCES formula (`id`), 
    FOREIGN KEY(`scenario_id`) REFERENCES scenario (`id`)
);

CREATE TABLE `parcel` (
    `name` VARCHAR(120) NOT NULL,
    `description` VARCHAR(250),
    `scenario_id` INTEGER NOT NULL,
    `vertices` JSON NOT NULL,
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (`id`),
    FOREIGN KEY(`scenario_id`) REFERENCES scenario (`id`),
    UNIQUE (`scenario_id`, `name`)
);

CREATE TABLE `scenario_chemicals` (
    `scenario_id` INTEGER, 
    `chemical_id` INTEGER, 
    FOREIGN KEY(`chemical_id`) REFERENCES chemical (`id`), 
    FOREIGN KEY(`scenario_id`) REFERENCES scenario (`id`), 
    UNIQUE (`scenario_id`, `chemical_id`)
);

CREATE TABLE `volume_element` (
    `name` VARCHAR(120) NOT NULL, 
    `parcel_id` INTEGER NOT NULL, 
    `top` DECIMAL(30,15) NOT NULL, 
    `bottom` DECIMAL(30,15) NOT NULL, 
    `id` INTEGER NOT NULL AUTO_INCREMENT, 
    PRIMARY KEY (`id`), 
    FOREIGN KEY(`parcel_id`) REFERENCES `parcel` (`id`), 
    UNIQUE (`parcel_id`, `name`)
);

CREATE TABLE `compartment` (
    `name` VARCHAR(120) NOT NULL, 
    `volume_element_id` INTEGER NOT NULL, 
    `media_id` INTEGER NOT NULL, 
    `id` INTEGER NOT NULL AUTO_INCREMENT, 
    PRIMARY KEY (`id`), 
    FOREIGN KEY(`media_id`) REFERENCES media (`id`), 
    FOREIGN KEY(`volume_element_id`) REFERENCES `volume_element` (`id`), 
    UNIQUE (`volume_element_id`, `name`)
);

CREATE TABLE `compartment_link` (
    `sender_id` INTEGER NOT NULL, 
    `receiver_id` INTEGER NOT NULL, 
    `id` INTEGER NOT NULL AUTO_INCREMENT, 
    PRIMARY KEY (`id`), 
    FOREIGN KEY(`receiver_id`) REFERENCES `compartment` (`id`), 
    FOREIGN KEY(`sender_id`) REFERENCES `compartment` (`id`), 
    UNIQUE (`sender_id`, `receiver_id`)
);

CREATE TABLE `scenario_load_run_proc` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `load_status` VARCHAR(140),
    `run_status` VARCHAR(140),
    `run_datetime` DATETIME,
    `result_file_nt` VARCHAR(255),
    `result_file_conc` VARCHAR(255),
    `result_nt` MEDIUMTEXT,
    `result_conc` MEDIUMTEXT,
    `scenario_id` INTEGER NOT NULL,
    PRIMARY KEY (`id`), 
    FOREIGN KEY(`scenario_id`) REFERENCES `scenario` (`id`)
);

CREATE TABLE `api_key` (
    `active` BOOLEAN NOT NULL, 
    `value` VARCHAR(255) NOT NULL, 
    `user_id` INTEGER NOT NULL, 
    `id` INTEGER NOT NULL AUTO_INCREMENT, 
    PRIMARY KEY (`id`), 
    FOREIGN KEY(`user_id`) REFERENCES `user` (`id`)
    UNIQUE (`value`)
);

INSERT INTO `alembic_version` (`version_num`) VALUES ('12f3b3bc93f9');

