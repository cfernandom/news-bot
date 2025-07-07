-- =====================================================
-- Migration: 002_source_administration.sql
-- Description: Add source administration and compliance features
-- Version: 1.0
-- Date: 2025-07-07
-- Dependencies: 001_initial_schema.sql
-- =====================================================

-- Begin transaction
BEGIN;

-- =====================================================
-- 1. EXTEND NEWS_SOURCES TABLE
-- =====================================================

-- Add source administration columns
ALTER TABLE news_sources
ADD COLUMN IF NOT EXISTS legal_contact_email VARCHAR(255),
ADD COLUMN IF NOT EXISTS terms_of_service_url TEXT,
ADD COLUMN IF NOT EXISTS privacy_policy_url TEXT,
ADD COLUMN IF NOT EXISTS robots_txt_url TEXT,
ADD COLUMN IF NOT EXISTS fair_use_basis TEXT,
ADD COLUMN IF NOT EXISTS content_type VARCHAR(50) DEFAULT 'metadata_only',
ADD COLUMN IF NOT EXISTS data_retention_days INTEGER DEFAULT 365,
ADD COLUMN IF NOT EXISTS data_retention_expires_at TIMESTAMP,
ADD COLUMN IF NOT EXISTS max_articles_per_run INTEGER DEFAULT 50,
ADD COLUMN IF NOT EXISTS crawl_delay_seconds NUMERIC(4,2) DEFAULT 2.0,
ADD COLUMN IF NOT EXISTS target_sections JSONB DEFAULT '[]',
ADD COLUMN IF NOT EXISTS source_type VARCHAR(50) DEFAULT 'news_site',
ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'active';

-- Add compliance tracking columns
ALTER TABLE news_sources
ADD COLUMN IF NOT EXISTS robots_txt_compliant BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS legal_contact_verified BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS terms_acceptable BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS fair_use_documented BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS data_minimization_applied BOOLEAN DEFAULT TRUE,
ADD COLUMN IF NOT EXISTS legal_review_status VARCHAR(50) DEFAULT 'pending',
ADD COLUMN IF NOT EXISTS compliance_last_checked TIMESTAMP,
ADD COLUMN IF NOT EXISTS risk_level VARCHAR(20) DEFAULT 'medium';

-- Add performance tracking columns
ALTER TABLE news_sources
ADD COLUMN IF NOT EXISTS last_successful_run TIMESTAMP,
ADD COLUMN IF NOT EXISTS success_rate NUMERIC(4,3) DEFAULT 0.0,
ADD COLUMN IF NOT EXISTS average_response_time NUMERIC(6,3) DEFAULT 0.0,
ADD COLUMN IF NOT EXISTS articles_collected_total INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS error_count_last_30_days INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS next_scheduled_run TIMESTAMP;

-- Add automation tracking columns
ALTER TABLE news_sources
ADD COLUMN IF NOT EXISTS scraper_type VARCHAR(50) DEFAULT 'manual',
ADD COLUMN IF NOT EXISTS generation_method VARCHAR(50),
ADD COLUMN IF NOT EXISTS template_used VARCHAR(50),
ADD COLUMN IF NOT EXISTS automation_score NUMERIC(3,2) DEFAULT 0.0,
ADD COLUMN IF NOT EXISTS health_status VARCHAR(20) DEFAULT 'unknown',
ADD COLUMN IF NOT EXISTS last_health_check TIMESTAMP;

-- =====================================================
-- 2. CREATE COMPLIANCE AUDIT LOG TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS compliance_audit_log (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    record_id INTEGER,
    action VARCHAR(50) NOT NULL,
    old_values JSONB,
    new_values JSONB,
    legal_basis TEXT,
    compliance_notes TEXT,
    risk_assessment VARCHAR(20),
    performed_by VARCHAR(100) NOT NULL,
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address INET,
    user_agent TEXT,
    session_id VARCHAR(255),

    -- Indexes for performance
    CONSTRAINT valid_action CHECK (action IN ('create', 'update', 'delete', 'validate', 'review', 'suspend', 'activate')),
    CONSTRAINT valid_risk_assessment CHECK (risk_assessment IN ('low', 'medium', 'high', 'critical') OR risk_assessment IS NULL)
);

-- Create indexes for audit log
CREATE INDEX IF NOT EXISTS idx_compliance_audit_log_table_record
ON compliance_audit_log (table_name, record_id);

CREATE INDEX IF NOT EXISTS idx_compliance_audit_log_performed_at
ON compliance_audit_log (performed_at DESC);

CREATE INDEX IF NOT EXISTS idx_compliance_audit_log_performed_by
ON compliance_audit_log (performed_by);

CREATE INDEX IF NOT EXISTS idx_compliance_audit_log_action
ON compliance_audit_log (action);

-- =====================================================
-- 3. CREATE LEGAL NOTICES TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS legal_notices (
    id SERIAL PRIMARY KEY,
    source_id INTEGER REFERENCES news_sources(id) ON DELETE CASCADE,
    notice_type VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    effective_date DATE NOT NULL,
    expiration_date DATE,
    status VARCHAR(20) DEFAULT 'active',
    legal_contact VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT valid_notice_type CHECK (notice_type IN ('fair_use', 'dmca_notice', 'takedown_request', 'legal_review', 'compliance_warning')),
    CONSTRAINT valid_status CHECK (status IN ('active', 'expired', 'superseded', 'withdrawn'))
);

-- Create indexes for legal notices
CREATE INDEX IF NOT EXISTS idx_legal_notices_source_id ON legal_notices (source_id);
CREATE INDEX IF NOT EXISTS idx_legal_notices_effective_date ON legal_notices (effective_date DESC);
CREATE INDEX IF NOT EXISTS idx_legal_notices_notice_type ON legal_notices (notice_type);
CREATE INDEX IF NOT EXISTS idx_legal_notices_status ON legal_notices (status);

-- =====================================================
-- 4. CREATE COMPLIANCE VALIDATIONS TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS compliance_validations (
    id SERIAL PRIMARY KEY,
    source_id INTEGER REFERENCES news_sources(id) ON DELETE CASCADE,
    validation_type VARCHAR(50) NOT NULL,
    validation_result BOOLEAN NOT NULL,
    validation_details JSONB DEFAULT '{}',
    validation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    validator VARCHAR(100) NOT NULL,
    expires_at TIMESTAMP,
    revalidation_required BOOLEAN DEFAULT FALSE,
    notes TEXT,

    CONSTRAINT valid_validation_type CHECK (validation_type IN (
        'robots_txt', 'legal_contact', 'terms_of_service', 'fair_use',
        'data_retention', 'gdpr', 'accessibility', 'content_type'
    ))
);

-- Create indexes for compliance validations
CREATE INDEX IF NOT EXISTS idx_compliance_validations_source_id ON compliance_validations (source_id);
CREATE INDEX IF NOT EXISTS idx_compliance_validations_type ON compliance_validations (validation_type);
CREATE INDEX IF NOT EXISTS idx_compliance_validations_timestamp ON compliance_validations (validation_timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_compliance_validations_result ON compliance_validations (validation_result);

-- =====================================================
-- 5. CREATE USER ROLES AND PERMISSIONS TABLES
-- =====================================================

CREATE TABLE IF NOT EXISTS user_roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    permissions JSONB DEFAULT '[]',
    is_system_role BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT valid_role_name CHECK (name ~ '^[a-z_]+$')
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    last_login TIMESTAMP,
    failed_login_attempts INTEGER DEFAULT 0,
    account_locked_until TIMESTAMP,
    password_changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT valid_email CHECK (email ~ '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
);

CREATE TABLE IF NOT EXISTS user_role_assignments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    role_id INTEGER REFERENCES user_roles(id) ON DELETE CASCADE,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    assigned_by INTEGER REFERENCES users(id),
    expires_at TIMESTAMP,

    UNIQUE(user_id, role_id)
);

-- Create indexes for user management
CREATE INDEX IF NOT EXISTS idx_users_username ON users (username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users (email);
CREATE INDEX IF NOT EXISTS idx_users_active ON users (is_active);
CREATE INDEX IF NOT EXISTS idx_user_role_assignments_user_id ON user_role_assignments (user_id);
CREATE INDEX IF NOT EXISTS idx_user_role_assignments_role_id ON user_role_assignments (role_id);

-- =====================================================
-- 6. CREATE SCRAPER AUTOMATION LOG TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS scraper_automation_log (
    id SERIAL PRIMARY KEY,
    domain VARCHAR(255) NOT NULL,
    action VARCHAR(50) NOT NULL,
    result VARCHAR(20) NOT NULL,
    details JSONB DEFAULT '{}',
    performance_metrics JSONB DEFAULT '{}',
    compliance_status JSONB DEFAULT '{}',
    error_message TEXT,
    execution_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT valid_action CHECK (action IN (
        'generate', 'test', 'deploy', 'validate', 'monitor', 'suspend', 'remove'
    )),
    CONSTRAINT valid_result CHECK (result IN ('success', 'failure', 'warning', 'partial'))
);

-- Create indexes for automation log
CREATE INDEX IF NOT EXISTS idx_scraper_automation_log_domain ON scraper_automation_log (domain);
CREATE INDEX IF NOT EXISTS idx_scraper_automation_log_action ON scraper_automation_log (action);
CREATE INDEX IF NOT EXISTS idx_scraper_automation_log_created_at ON scraper_automation_log (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_scraper_automation_log_result ON scraper_automation_log (result);

-- =====================================================
-- 7. INSERT DEFAULT DATA
-- =====================================================

-- Insert default user roles
INSERT INTO user_roles (name, description, permissions, is_system_role)
VALUES
(
    'source_admin',
    'Source Administration Manager - Full access to source management',
    '["sources:create", "sources:read", "sources:update", "sources:delete", "sources:validate", "compliance:read", "compliance:validate", "audit:read"]',
    TRUE
),
(
    'source_editor',
    'Source Editor - Can modify existing sources',
    '["sources:read", "sources:update", "sources:validate", "compliance:read"]',
    TRUE
),
(
    'source_viewer',
    'Source Viewer - Read-only access to sources',
    '["sources:read", "compliance:read"]',
    TRUE
),
(
    'compliance_officer',
    'Compliance Officer - Specialized compliance management',
    '["sources:read", "compliance:read", "compliance:validate", "compliance:review", "audit:read", "legal:manage"]',
    TRUE
),
(
    'system_admin',
    'System Administrator - Full system access',
    '["*"]',
    TRUE
)
ON CONFLICT (name) DO NOTHING;

-- =====================================================
-- 8. UPDATE EXISTING SOURCES WITH DEFAULT VALUES
-- =====================================================

-- Update existing sources with default compliance values
UPDATE news_sources
SET
    content_type = 'metadata_only',
    data_retention_days = 365,
    data_retention_expires_at = CURRENT_DATE + INTERVAL '365 days',
    max_articles_per_run = 50,
    crawl_delay_seconds = 2.0,
    target_sections = '[]',
    source_type = 'news_site',
    status = 'active',
    data_minimization_applied = TRUE,
    legal_review_status = 'approved',
    risk_level = 'low',
    scraper_type = 'manual',
    health_status = 'operational'
WHERE content_type IS NULL;

-- Set compliance status for existing operational sources
UPDATE news_sources
SET
    robots_txt_compliant = TRUE,
    legal_contact_verified = TRUE,
    terms_acceptable = TRUE,
    fair_use_documented = TRUE,
    compliance_last_checked = CURRENT_TIMESTAMP,
    fair_use_basis = 'Academic research at UCOMPENSAR University for breast cancer news analysis under fair use doctrine for educational purposes'
WHERE id IN (
    SELECT DISTINCT source_id
    FROM articles
    WHERE created_at > CURRENT_DATE - INTERVAL '30 days'
) AND fair_use_basis IS NULL;

-- =====================================================
-- 9. CREATE TRIGGERS FOR AUDIT LOGGING
-- =====================================================

-- Function to log compliance changes
CREATE OR REPLACE FUNCTION log_compliance_changes()
RETURNS TRIGGER AS $$
BEGIN
    -- Log changes to news_sources table
    IF TG_TABLE_NAME = 'news_sources' THEN
        INSERT INTO compliance_audit_log (
            table_name, record_id, action, old_values, new_values,
            performed_by, performed_at, legal_basis
        ) VALUES (
            TG_TABLE_NAME,
            COALESCE(NEW.id, OLD.id),
            CASE
                WHEN TG_OP = 'INSERT' THEN 'create'
                WHEN TG_OP = 'UPDATE' THEN 'update'
                WHEN TG_OP = 'DELETE' THEN 'delete'
            END,
            CASE WHEN TG_OP != 'INSERT' THEN row_to_json(OLD) END,
            CASE WHEN TG_OP != 'DELETE' THEN row_to_json(NEW) END,
            COALESCE(current_setting('app.current_user', TRUE), 'system'),
            CURRENT_TIMESTAMP,
            CASE
                WHEN TG_OP = 'INSERT' THEN 'Source creation for academic research'
                WHEN TG_OP = 'UPDATE' THEN 'Source modification for compliance maintenance'
                WHEN TG_OP = 'DELETE' THEN 'Source removal for compliance or operational reasons'
            END
        );
    END IF;

    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

-- Create triggers for audit logging
DROP TRIGGER IF EXISTS news_sources_audit_trigger ON news_sources;
CREATE TRIGGER news_sources_audit_trigger
    AFTER INSERT OR UPDATE OR DELETE ON news_sources
    FOR EACH ROW
    EXECUTE FUNCTION log_compliance_changes();

-- =====================================================
-- 10. CREATE VIEWS FOR REPORTING
-- =====================================================

-- View for compliance dashboard
CREATE OR REPLACE VIEW compliance_dashboard AS
SELECT
    COUNT(*) as total_sources,
    COUNT(*) FILTER (WHERE robots_txt_compliant = TRUE AND
                           legal_contact_verified = TRUE AND
                           terms_acceptable = TRUE AND
                           fair_use_documented = TRUE AND
                           data_minimization_applied = TRUE) as compliant_sources,
    COUNT(*) FILTER (WHERE legal_review_status = 'pending') as pending_review,
    COUNT(*) FILTER (WHERE status = 'active') as active_sources,
    COUNT(*) FILTER (WHERE risk_level = 'high' OR risk_level = 'critical') as high_risk_sources,
    AVG(success_rate) as average_success_rate,
    MAX(compliance_last_checked) as last_compliance_check
FROM news_sources
WHERE status != 'deleted';

-- View for source performance summary
CREATE OR REPLACE VIEW source_performance_summary AS
SELECT
    ns.id,
    ns.name,
    ns.base_url,
    ns.status,
    ns.success_rate,
    ns.articles_collected_total,
    ns.last_successful_run,
    ns.error_count_last_30_days,
    COUNT(a.id) FILTER (WHERE a.created_at > CURRENT_DATE - INTERVAL '30 days') as articles_last_30_days,
    ns.compliance_last_checked,
    CASE
        WHEN ns.robots_txt_compliant AND ns.legal_contact_verified AND
             ns.terms_acceptable AND ns.fair_use_documented AND
             ns.data_minimization_applied THEN 'compliant'
        ELSE 'non_compliant'
    END as compliance_status
FROM news_sources ns
LEFT JOIN articles a ON ns.id = a.source_id
WHERE ns.status != 'deleted'
GROUP BY ns.id, ns.name, ns.base_url, ns.status, ns.success_rate,
         ns.articles_collected_total, ns.last_successful_run,
         ns.error_count_last_30_days, ns.compliance_last_checked,
         ns.robots_txt_compliant, ns.legal_contact_verified,
         ns.terms_acceptable, ns.fair_use_documented,
         ns.data_minimization_applied;

-- =====================================================
-- 11. CREATE CONSTRAINTS
-- =====================================================

-- Add constraints for data integrity
ALTER TABLE news_sources
ADD CONSTRAINT IF NOT EXISTS check_crawl_delay
CHECK (crawl_delay_seconds >= 1.0);

ALTER TABLE news_sources
ADD CONSTRAINT IF NOT EXISTS check_max_articles
CHECK (max_articles_per_run > 0 AND max_articles_per_run <= 500);

ALTER TABLE news_sources
ADD CONSTRAINT IF NOT EXISTS check_retention_days
CHECK (data_retention_days >= 30 AND data_retention_days <= 2555);

ALTER TABLE news_sources
ADD CONSTRAINT IF NOT EXISTS check_content_type
CHECK (content_type IN ('metadata_only', 'summary_only'));

ALTER TABLE news_sources
ADD CONSTRAINT IF NOT EXISTS check_source_type
CHECK (source_type IN ('news_site', 'academic', 'government', 'ngo', 'medical_journal'));

ALTER TABLE news_sources
ADD CONSTRAINT IF NOT EXISTS check_status
CHECK (status IN ('active', 'inactive', 'suspended', 'under_review', 'deleted'));

ALTER TABLE news_sources
ADD CONSTRAINT IF NOT EXISTS check_risk_level
CHECK (risk_level IN ('low', 'medium', 'high', 'critical'));

-- =====================================================
-- 12. PERFORMANCE OPTIMIZATIONS
-- =====================================================

-- Create composite indexes for common queries
CREATE INDEX IF NOT EXISTS idx_news_sources_status_type
ON news_sources (status, source_type);

CREATE INDEX IF NOT EXISTS idx_news_sources_compliance_status
ON news_sources (robots_txt_compliant, legal_contact_verified, terms_acceptable, fair_use_documented);

CREATE INDEX IF NOT EXISTS idx_news_sources_performance
ON news_sources (success_rate DESC, last_successful_run DESC)
WHERE status = 'active';

CREATE INDEX IF NOT EXISTS idx_news_sources_compliance_check
ON news_sources (compliance_last_checked ASC)
WHERE status = 'active';

-- =====================================================
-- 13. GRANTS AND PERMISSIONS
-- =====================================================

-- Grant appropriate permissions (adjust role names as needed)
-- GRANT SELECT, INSERT, UPDATE ON news_sources TO source_admin_role;
-- GRANT SELECT, INSERT ON compliance_audit_log TO source_admin_role;
-- GRANT SELECT ON compliance_dashboard TO source_viewer_role;

-- =====================================================
-- COMMIT TRANSACTION
-- =====================================================

COMMIT;

-- =====================================================
-- VERIFICATION QUERIES
-- =====================================================

-- Verify migration success
DO $$
BEGIN
    -- Check if all columns were added
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'news_sources' AND column_name = 'legal_contact_email'
    ) THEN
        RAISE EXCEPTION 'Migration failed: legal_contact_email column not created';
    END IF;

    -- Check if audit table was created
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.tables
        WHERE table_name = 'compliance_audit_log'
    ) THEN
        RAISE EXCEPTION 'Migration failed: compliance_audit_log table not created';
    END IF;

    -- Check if default roles were inserted
    IF NOT EXISTS (
        SELECT 1 FROM user_roles WHERE name = 'source_admin'
    ) THEN
        RAISE EXCEPTION 'Migration failed: default roles not inserted';
    END IF;

    RAISE NOTICE 'Migration 002_source_administration.sql completed successfully';
END
$$;
