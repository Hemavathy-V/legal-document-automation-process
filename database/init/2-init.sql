-- Contract templates table and seed data
-- Run after 0-init.sql (schema) and 1-init.sql (lookup + user seed data)

USE contract_management1;

CREATE TABLE contract_templates (
    id           INT PRIMARY KEY AUTO_INCREMENT,
    template_name VARCHAR(255) NOT NULL,
    template_type VARCHAR(100) NOT NULL,
    file_path    VARCHAR(500) NOT NULL UNIQUE,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO contract_templates (template_name, template_type, file_path) VALUES
('Master Service Agreement Template', 'MSA',                 'sample_templates/Master-Service-Agreement-Template.docx'),
('Non-Disclosure Agreement Template', 'NDA',                 'sample_templates/Non-Disclosure-Agreement-Template.docx'),
('Service Agreement Template',        'SERVICE_AGREEMENT',   'sample_templates/Service-Agreement-Template.docx'),
('Termination Agreement Template',    'TERMINATION',         'sample_templates/Termination-Agreement-Template.docx'),
('Statement Of Work Template',        'SOW',                 'sample_templates/Statement-Of-Work-Template.docx');
