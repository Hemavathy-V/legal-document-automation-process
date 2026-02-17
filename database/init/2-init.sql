-- ===========================================================
-- VIEWS
-- ===========================================================

CREATE VIEW view_contract_summary AS
SELECT 
    c.id,
    c.title,
    c.contract_type,
    c.status,
    c.risk_score,
    o.name AS organization_name
FROM contracts c
JOIN organizations o ON c.organization_id = o.id
WHERE c.is_deleted = FALSE;

CREATE VIEW view_red_flag_summary AS
SELECT 
    r.id,
    c.title,
    r.clause_reference,
    r.severity,
    r.resolved
FROM red_flags r
JOIN contracts c ON r.contract_id = c.id;