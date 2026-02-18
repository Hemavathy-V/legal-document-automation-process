/* ===========================================================
   CONTRACT AUTOMATION DATABASE - FULL SETUP
   Multi-Tenant | RBAC | Versioning | Audit | Cloud Ready
=========================================================== */

DROP DATABASE IF EXISTS contract_automation;

CREATE DATABASE contract_automation
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE contract_automation;

-- ===========================================================
-- ORGANIZATIONS
-- ===========================================================

CREATE TABLE organizations (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    domain VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMP NULL
) ENGINE=InnoDB;

-- ===========================================================
-- USERS
-- ===========================================================

CREATE TABLE users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    organization_id BIGINT NOT NULL,
    name VARCHAR(30) NOT NULL,
    email VARCHAR(30) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    status ENUM('ACTIVE','INACTIVE') DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMP NULL,
    
    FOREIGN KEY (organization_id) REFERENCES organizations(id)
    ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE INDEX idx_users_org ON users(organization_id);

-- ===========================================================
-- ROLES
-- ===========================================================

CREATE TABLE roles (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ===========================================================
-- USER ROLES
-- ===========================================================

CREATE TABLE user_roles (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    role_id BIGINT NOT NULL,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ===========================================================
-- PERMISSIONS
-- ===========================================================

CREATE TABLE permissions (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- ===========================================================
-- ROLE PERMISSIONS
-- ===========================================================

CREATE TABLE role_permissions (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    role_id BIGINT NOT NULL,
    permission_id BIGINT NOT NULL,
    
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ===========================================================
-- CONTRACTS
-- ===========================================================

CREATE TABLE contracts (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    organization_id BIGINT NOT NULL,
    title VARCHAR(20) NOT NULL,
    contract_type VARCHAR(30),
    jurisdiction VARCHAR(150),
    status ENUM('DRAFT','UNDER_REVIEW','APPROVED','REJECTED','EXECUTED','EXPIRED') DEFAULT 'DRAFT',
    risk_score DECIMAL(5,2) DEFAULT 0.00,
    effective_date DATE,
    expiration_date DATE,
    current_version_id BIGINT NULL,
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMP NULL,
    
    FOREIGN KEY (organization_id) REFERENCES organizations(id),
    FOREIGN KEY (created_by) REFERENCES users(id)
) ENGINE=InnoDB;

CREATE INDEX idx_contract_org ON contracts(organization_id);

-- ===========================================================
-- CONTRACT VERSIONS
-- ===========================================================

CREATE TABLE contract_versions (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    contract_id BIGINT NOT NULL,
    version_number INT NOT NULL,
    file_url TEXT NOT NULL,
    edited_by BIGINT NOT NULL,
    change_summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE,
    
    FOREIGN KEY (contract_id) REFERENCES contracts(id) ON DELETE CASCADE,
    FOREIGN KEY (edited_by) REFERENCES users(id)
) ENGINE=InnoDB;

-- ===========================================================
-- CONTRACT STATUS HISTORY
-- ===========================================================

CREATE TABLE contract_status_history (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    contract_id BIGINT NOT NULL,
    old_status VARCHAR(30),
    new_status VARCHAR(30),
    changed_by BIGINT NOT NULL,
    comments TEXT,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (contract_id) REFERENCES contracts(id) ON DELETE CASCADE,
    FOREIGN KEY (changed_by) REFERENCES users(id)
) ENGINE=InnoDB;

-- ===========================================================
-- RED FLAGS
-- ===========================================================

CREATE TABLE red_flags (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    contract_id BIGINT NOT NULL,
    clause_reference TEXT,
    issue_description TEXT,
    severity ENUM('LOW','MEDIUM','HIGH') DEFAULT 'MEDIUM',
    generated_by_llm BOOLEAN DEFAULT TRUE,
    resolved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (contract_id) REFERENCES contracts(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ===========================================================
-- HUMAN REVIEWS
-- ===========================================================

CREATE TABLE human_reviews (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    contract_id BIGINT NOT NULL,
    reviewer_id BIGINT NOT NULL,
    comments TEXT,
    rating INT,
    reviewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (contract_id) REFERENCES contracts(id) ON DELETE CASCADE,
    FOREIGN KEY (reviewer_id) REFERENCES users(id)
) ENGINE=InnoDB;

-- ===========================================================
-- AUDIT LOGS
-- ===========================================================

CREATE TABLE audit_logs (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    organization_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    action_type VARCHAR(150),
    entity_type VARCHAR(150),
    entity_id BIGINT,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (organization_id) REFERENCES organizations(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB;

-- =============================================
-- CLAUSE LIBRARY TABLE
-- =============================================
USE contract_automation;
CREATE TABLE IF NOT EXISTS clauses (
    clause_id INT PRIMARY KEY AUTO_INCREMENT,
    clause_title VARCHAR(30) NOT NULL,
    clause_category VARCHAR(100) NOT NULL,
    contract_type VARCHAR(30) NOT NULL,
    jurisdiction VARCHAR(100),
    risk_level VARCHAR(50),
    clause_text TEXT NOT NULL,
    version INT DEFAULT 1,
    is_active BOOLEAN DEFAULT TRUE,
    created_by VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- =============================================
-- INDEXES (FOR FAST RETRIEVAL)
-- =============================================

CREATE INDEX idx_clause_category ON clauses(clause_category);
CREATE INDEX idx_contract_type ON clauses(contract_type);
CREATE INDEX idx_jurisdiction ON clauses(jurisdiction);
CREATE INDEX idx_risk_level ON clauses(risk_level);
