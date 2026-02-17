-- SQL script to create the contract_templates table --
CREATE TABLE contract_templates (
    id INT PRIMARY KEY AUTO_INCREMENT,
    template_name VARCHAR(255) NOT NULL,
    template_type VARCHAR(100) NOT NULL,
    file_path VARCHAR(500) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample contract templates into the contract_templates table --
INSERT INTO contract_templates (template_name, template_type, file_path) 
VALUES ('Master Service Agreement Template', 'MSA', 'sample_templates/Master-Service-Agreement-Template.docx');

INSERT INTO contract_templates (template_name, template_type, file_path) 
VALUES ('Non-Disclosure Agreement Template', 'NDA', 'sample_templates/Non-Disclosure-Agreement-Template.docx');

INSERT INTO contract_templates (template_name, template_type, file_path) 
VALUES ('Service Agreement Template', 'SERVICE_AGREEMENT', 'sample_templates/Service-Agreement-Template.docx');

INSERT INTO contract_templates (template_name, template_type, file_path) 
VALUES ('Termination Agreement Template', 'TERMINATION', 'sample_templates/Termination-Agreement-Template.docx');

INSERT INTO contract_templates (template_name, template_type, file_path) 
VALUES ('Statement Of Work Template', 'SOW', 'sample_templates/Statement-Of-Work-Template.docx');
