-- ===========================================================
-- DUMMY DATA INSERTS
-- ===========================================================

INSERT INTO organizations (name, domain)
VALUES ('ABC Corp', 'abc.com'),
       ('XYZ Legal', 'xyzlegal.com');

INSERT INTO users (organization_id, name, email, password_hash)
VALUES 
(1, 'Admin User', 'admin@abc.com', '123456'),
(1, 'Legal User', 'legal@abc.com', '123456'),
(2, 'Client User', 'client@xyzlegal.com', '123456');

INSERT INTO roles (name, description)
VALUES 
('ADMIN','Full access'),
('LEGAL','Legal team'),
('CLIENT','Client access'),
('REVIEWER','Review access');

INSERT INTO user_roles (user_id, role_id)
VALUES 
(1,1),
(2,2),
(3,3);

INSERT INTO permissions (name)
VALUES 
('CREATE_CONTRACT'),
('EDIT_CONTRACT'),
('VIEW_CONTRACT'),
('APPROVE_CONTRACT');

INSERT INTO contracts (organization_id, title, contract_type, jurisdiction, created_by, risk_score)
VALUES 
(1, 'NDA Agreement', 'NDA', 'India', 1, 3.50);

INSERT INTO contract_versions (contract_id, version_number, file_url, edited_by, change_summary)
VALUES 
(1, 1, 'https://storage.com/nda_v1.pdf', 1, 'Initial draft');

INSERT INTO red_flags (contract_id, clause_reference, issue_description, severity)
VALUES 
(1, 'Clause 4.2', 'Unlimited liability clause detected', 'HIGH');

INSERT INTO human_reviews (contract_id, reviewer_id, comments, rating)
VALUES 
(1, 2, 'Needs liability cap adjustment', 4);

INSERT INTO audit_logs (organization_id, user_id, action_type, entity_type, entity_id, ip_address)
VALUES 
(1, 1, 'CREATE', 'CONTRACT', 1, '127.0.0.1');
