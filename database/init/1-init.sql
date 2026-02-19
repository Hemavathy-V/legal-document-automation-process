INSERT INTO look_up (lookup_type, lookup_value) VALUES

-- Contract Types
('contract_type', 'MSA'),
('contract_type', 'SOW'),
('contract_type', 'Service Agreement'),
('contract_type', 'Termination Agreement'),
('contract_type', 'NDA'),

-- Jurisdictions
('jurisdiction', 'India'),
('jurisdiction', 'Global'),
('jurisdiction', 'United States'),
('jurisdiction', 'United Kingdom'),
('jurisdiction', 'United Kingdom-Walves'),
('jurisdiction', 'United Kingdom-England'),

-- Contract Status
('status', 'Review'),
('status', 'Under-Review'),
('status', 'Rejected'),
('status', 'Draft'),

-- User Roles
('user_role', 'Lawyer'),
('user_role', 'Admin'),
('user_role', 'Client'),
('user_role', 'Assistant Lawyer');

INSERT INTO users (user_name, role_id, email) VALUES
('Arun Kumar', 16, 'arun.kumar@company.com'),
('Meena Sharma', 17, 'meena.sharma@company.com'),
('Ravi Patel', 18, 'ravi.patel@client.com'),
('Sanjay Rao', 19, 'sanjay.rao@company.com'),
('Anita Verma', 17, 'anita.verma@company.com');

INSERT INTO contracts 
(contract_type_id, jurisdiction_id, status_id, created_by) 
VALUES
(1, 6, 11, 1),   -- MSA, India, Draft, Arun
(5, 8, 12, 2),   -- NDA, United States, Review, Meena
(2, 7, 13, 4),   -- SOW, Global, Under-Review, Sanjay
(3, 6, 11, 5),   -- Service Agreement, India, Draft, Anita
(4, 9, 14, 1);   -- Termination Agreement, UK, Rejected, Arun
