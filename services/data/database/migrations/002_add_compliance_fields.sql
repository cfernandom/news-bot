-- Migration: Add compliance fields and audit logging
-- Version: 002
-- Date: 2025-07-04
-- Description: Add fair_use_basis, compliance_score, and audit logging for news source administration

-- Add new compliance fields to news_sources table
ALTER TABLE news_sources
ADD COLUMN fair_use_basis TEXT,
ADD COLUMN compliance_score DECIMAL(3,2),
ADD COLUMN last_compliance_check TIMESTAMP;

-- Create compliance_audit_log table
CREATE TABLE compliance_audit_log (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    record_id INTEGER NOT NULL,
    action VARCHAR(50) NOT NULL,
    old_values JSONB,
    new_values JSONB,
    legal_basis VARCHAR(255) DEFAULT 'academic_research_fair_use',
    performed_by VARCHAR(255) NOT NULL,
    performed_at TIMESTAMP NOT NULL DEFAULT NOW(),

    -- Compliance-specific fields
    compliance_score_before DECIMAL(3,2),
    compliance_score_after DECIMAL(3,2),
    risk_level VARCHAR(20),
    violations_count INTEGER DEFAULT 0,

    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX idx_compliance_audit_table_record ON compliance_audit_log(table_name, record_id);
CREATE INDEX idx_compliance_audit_performed_at ON compliance_audit_log(performed_at);
CREATE INDEX idx_compliance_audit_action ON compliance_audit_log(action);
CREATE INDEX idx_news_sources_compliance_score ON news_sources(compliance_score);
CREATE INDEX idx_news_sources_last_compliance_check ON news_sources(last_compliance_check);

-- Update existing sources with default compliance data for backwards compatibility
UPDATE news_sources
SET
    fair_use_basis = 'Academic research under Colombian Law 1581/2012 and fair use doctrine',
    compliance_score = 0.80,
    last_compliance_check = NOW()
WHERE fair_use_basis IS NULL;

-- Insert initial audit log entries for existing sources
INSERT INTO compliance_audit_log (
    table_name, record_id, action, new_values, legal_basis, performed_by, performed_at
)
SELECT
    'news_sources',
    id,
    'migration_baseline',
    json_build_object(
        'name', name,
        'base_url', base_url,
        'compliance_score', 0.80,
        'migration_note', 'Baseline compliance established during news source administration implementation'
    ),
    'academic_research_fair_use',
    'system_migration',
    NOW()
FROM news_sources;

-- Add comment to track migration
COMMENT ON TABLE compliance_audit_log IS 'Audit trail for compliance-related actions on news sources. Part of legal compliance framework.';
COMMENT ON COLUMN news_sources.fair_use_basis IS 'Legal basis for fair use of content from this source';
COMMENT ON COLUMN news_sources.compliance_score IS 'Overall compliance score (0.00-1.00) based on legal requirements';
COMMENT ON COLUMN news_sources.last_compliance_check IS 'Timestamp of last automated compliance validation';
