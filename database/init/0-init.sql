CREATE DATABASE IF NOT EXISTS contract_management
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE contract_management;

CREATE TABLE look_up (
    lookup_id INT AUTO_INCREMENT PRIMARY KEY,

    lookup_type VARCHAR(30) NOT NULL,   -- contract_type, jurisdiction, status, user_role
    lookup_value VARCHAR(30) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (lookup_type, lookup_value)
);

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(30) NOT NULL,
    role_id INT NOT NULL,
    email VARCHAR(30) UNIQUE NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (role_id)
        REFERENCES look_up(lookup_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE contracts (
    contract_id INT AUTO_INCREMENT PRIMARY KEY,

    contract_type_id INT NOT NULL,
    jurisdiction_id INT NOT NULL,
    status_id INT NOT NULL,

    created_by INT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (contract_type_id)
        REFERENCES look_up(lookup_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    FOREIGN KEY (jurisdiction_id)
        REFERENCES look_up(lookup_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    FOREIGN KEY (status_id)
        REFERENCES look_up(lookup_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    FOREIGN KEY (created_by)
        REFERENCES users(user_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

