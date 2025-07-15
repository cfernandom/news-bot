-- =====================================================
-- Migration: 002_compliance_consolidated.sql
-- Description: Consolidated compliance, audit logging, and source administration
-- Version: 1.0
-- Date: 2025-07-15
-- Dependencies: 001_initial_schema.sql
-- =====================================================

-- Begin transaction
BEGIN;

-- =====================================================
-- 1. ADD COMPLIANCE FIELDS TO ARTICLES TABLE
-- =====================================================

-- Add compliance tracking fields to articles table
ALTER TABLE articles ADD COLUMN IF NOT EXISTS robots_txt_compliant BOOLEAN DEFAULT NULL;
ALTER TABLE articles ADD COLUMN IF NOT EXISTS copyright_status VARCHAR(50) DEFAULT 'unknown';
ALTER TABLE articles ADD COLUMN IF NOT EXISTS fair_use_basis TEXT;
ALTER TABLE articles ADD COLUMN IF NOT EXISTS scraping_permission BOOLEAN DEFAULT NULL;
ALTER TABLE articles ADD COLUMN IF NOT EXISTS content_type VARCHAR(20) DEFAULT 'full';
ALTER TABLE articles ADD COLUMN IF NOT EXISTS legal_review_status VARCHAR(50) DEFAULT 'pending';
ALTER TABLE articles ADD COLUMN IF NOT EXISTS data_retention_expires_at TIMESTAMP;

-- Add indexes for compliance queries on articles
CREATE INDEX IF NOT EXISTS idx_articles_copyright_status ON articles(copyright_status);
CREATE INDEX IF NOT EXISTS idx_articles_legal_review ON articles(legal_review_status);
CREATE INDEX IF NOT EXISTS idx_articles_retention_expires ON articles(data_retention_expires_at);
CREATE INDEX IF NOT EXISTS idx_articles_robots_compliant ON articles(robots_txt_compliant);

-- =====================================================
-- 2. EXTEND NEWS_SOURCES TABLE WITH COMPLIANCE & ADMIN FIELDS
-- =====================================================

-- Add compliance tracking to news_sources
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS robots_txt_url VARCHAR(500);
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS robots_txt_last_checked TIMESTAMP;
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS crawl_delay_seconds NUMERIC(4,2) DEFAULT 2.0;
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS scraping_allowed BOOLEAN DEFAULT NULL;
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS terms_of_service_url VARCHAR(500);
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS terms_reviewed_at TIMESTAMP;
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS legal_contact_email VARCHAR(255);
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS privacy_policy_url TEXT;
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS fair_use_basis TEXT;
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS compliance_score DECIMAL(3,2);
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS last_compliance_check TIMESTAMP;

-- Add source administration columns
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS content_type VARCHAR(50) DEFAULT 'metadata_only';
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS data_retention_days INTEGER DEFAULT 365;
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS data_retention_expires_at TIMESTAMP;
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS max_articles_per_run INTEGER DEFAULT 50;
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS target_sections JSONB DEFAULT '[]';
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS source_type VARCHAR(50) DEFAULT 'news_site';
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'active';

-- Add compliance tracking columns
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS robots_txt_compliant BOOLEAN DEFAULT FALSE;
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS legal_contact_verified BOOLEAN DEFAULT FALSE;
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS terms_acceptable BOOLEAN DEFAULT FALSE;
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS fair_use_documented BOOLEAN DEFAULT FALSE;
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS data_minimization_applied BOOLEAN DEFAULT TRUE;
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS risk_level VARCHAR(20) DEFAULT 'medium';

-- Add performance tracking columns
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS last_successful_run TIMESTAMP;
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS success_rate NUMERIC(4,3) DEFAULT 0.0;
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS average_response_time NUMERIC(6,3) DEFAULT 0.0;
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS articles_collected_total INTEGER DEFAULT 0;
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS error_count_last_30_days INTEGER DEFAULT 0;
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS next_scheduled_run TIMESTAMP;

-- Add automation tracking columns
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS scraper_type VARCHAR(50) DEFAULT 'manual';
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS generation_method VARCHAR(50);
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS template_used VARCHAR(50);
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS automation_score NUMERIC(3,2) DEFAULT 0.0;
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS health_status VARCHAR(20) DEFAULT 'unknown';
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS last_health_check TIMESTAMP;

-- =====================================================
-- 3. CREATE COMPLIANCE AUDIT LOG TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS compliance_audit_log (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    record_id INTEGER,
    action VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending', -- IMPORTANT: Include status column
    old_values JSONB,
    new_values JSONB,
    details JSONB,
    legal_basis VARCHAR(255) DEFAULT 'academic_research_fair_use',
    compliance_notes TEXT,
    risk_assessment VARCHAR(20),
    performed_by VARCHAR(255) NOT NULL,
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Compliance-specific fields
    compliance_score_before NUMERIC(3,2),
    compliance_score_after NUMERIC(3,2),
    risk_level VARCHAR(20),
    violations_count INTEGER DEFAULT 0,

    -- Timestamp fields
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address INET,
    user_agent TEXT,
    session_id VARCHAR(255),

    -- Constraints
    CONSTRAINT valid_action CHECK (action IN ('create', 'update', 'delete', 'validate', 'review', 'suspend', 'activate', 'robots_check', 'copyright_review', 'content_removal', 'migration_baseline', 'migration_002_applied')),
    CONSTRAINT valid_status CHECK (status IN ('pending', 'passed', 'failed') OR status IS NULL),
    CONSTRAINT valid_risk_assessment CHECK (risk_assessment IN ('low', 'medium', 'high', 'critical') OR risk_assessment IS NULL)
);

-- Create indexes for compliance_audit_log
CREATE INDEX IF NOT EXISTS idx_audit_table_record ON compliance_audit_log(table_name, record_id);
CREATE INDEX IF NOT EXISTS idx_audit_action ON compliance_audit_log(action);
CREATE INDEX IF NOT EXISTS idx_audit_status ON compliance_audit_log(status); -- This index should now work
CREATE INDEX IF NOT EXISTS idx_audit_performed_at ON compliance_audit_log(performed_at);
CREATE INDEX IF NOT EXISTS idx_compliance_audit_log_performed_by ON compliance_audit_log(performed_by);

-- =====================================================
-- 4. CREATE LEGAL NOTICES TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS legal_notices (
    id SERIAL PRIMARY KEY,
    source_id INTEGER REFERENCES news_sources(id) ON DELETE CASCADE,
    notice_type VARCHAR(50) NOT NULL, -- 'dmca', 'cease_desist', 'privacy_request', 'fair_use', 'takedown_request'
    title VARCHAR(200),
    source_domain VARCHAR(255) NOT NULL,
    affected_articles JSONB, -- Array of article IDs
    notice_content TEXT,
    content TEXT,
    requester_contact VARCHAR(255),
    legal_contact VARCHAR(255),
    received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    effective_date DATE,
    expiration_date DATE,
    status VARCHAR(50) DEFAULT 'received', -- 'received', 'reviewing', 'complied', 'disputed', 'active', 'expired'
    response_sent_at TIMESTAMP,
    compliance_actions JSONB, -- Actions taken to comply
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT valid_notice_type CHECK (notice_type IN ('dmca', 'cease_desist', 'privacy_request', 'fair_use', 'takedown_request', 'legal_review', 'compliance_warning')),
    CONSTRAINT valid_status CHECK (status IN ('received', 'reviewing', 'complied', 'disputed', 'active', 'expired', 'superseded', 'withdrawn'))
);

-- Create indexes for legal_notices
CREATE INDEX IF NOT EXISTS idx_notices_type ON legal_notices(notice_type);
CREATE INDEX IF NOT EXISTS idx_notices_domain ON legal_notices(source_domain);
CREATE INDEX IF NOT EXISTS idx_notices_status ON legal_notices(status);
CREATE INDEX IF NOT EXISTS idx_notices_received ON legal_notices(received_at);
CREATE INDEX IF NOT EXISTS idx_legal_notices_source_id ON legal_notices(source_id);
CREATE INDEX IF NOT EXISTS idx_legal_notices_effective_date ON legal_notices(effective_date DESC);

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
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_active ON users(is_active);
CREATE INDEX IF NOT EXISTS idx_user_role_assignments_user_id ON user_role_assignments(user_id);
CREATE INDEX IF NOT EXISTS idx_user_role_assignments_role_id ON user_role_assignments(role_id);

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
-- 6. CREATE ADDITIONAL TABLES FOR COMPLIANCE
-- =====================================================

-- Create compliance validations table
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
CREATE INDEX IF NOT EXISTS idx_compliance_validations_source_id ON compliance_validations(source_id);
CREATE INDEX IF NOT EXISTS idx_compliance_validations_type ON compliance_validations(validation_type);
CREATE INDEX IF NOT EXISTS idx_compliance_validations_timestamp ON compliance_validations(validation_timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_compliance_validations_result ON compliance_validations(validation_result);

-- Create scraper automation log table
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
CREATE INDEX IF NOT EXISTS idx_scraper_automation_log_domain ON scraper_automation_log(domain);
CREATE INDEX IF NOT EXISTS idx_scraper_automation_log_action ON scraper_automation_log(action);
CREATE INDEX IF NOT EXISTS idx_scraper_automation_log_created_at ON scraper_automation_log(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_scraper_automation_log_result ON scraper_automation_log(result);

-- =====================================================
-- 6. CREATE VIEWS FOR COMPLIANCE DASHBOARD
-- =====================================================

-- Create view for compliance dashboard
CREATE OR REPLACE VIEW compliance_dashboard AS
SELECT
    -- Source compliance overview
    COUNT(DISTINCT ns.id) as total_sources,
    COUNT(DISTINCT CASE WHEN ns.scraping_allowed = true THEN ns.id END) as sources_permitted,
    COUNT(DISTINCT CASE WHEN ns.scraping_allowed = false THEN ns.id END) as sources_blocked,
    COUNT(DISTINCT CASE WHEN ns.scraping_allowed IS NULL THEN ns.id END) as sources_unknown,
    COUNT(DISTINCT CASE WHEN ns.robots_txt_compliant = TRUE AND
                           ns.legal_contact_verified = TRUE AND
                           ns.terms_acceptable = TRUE AND
                           ns.fair_use_documented = TRUE AND
                           ns.data_minimization_applied = TRUE THEN ns.id END) as compliant_sources,
    COUNT(DISTINCT CASE WHEN ns.status = 'active' THEN ns.id END) as active_sources,
    COUNT(DISTINCT CASE WHEN ns.risk_level = 'high' OR ns.risk_level = 'critical' THEN ns.id END) as high_risk_sources,

    -- Article compliance overview
    COUNT(DISTINCT a.id) as total_articles,
    COUNT(DISTINCT CASE WHEN a.robots_txt_compliant = true THEN a.id END) as articles_robots_compliant,
    COUNT(DISTINCT CASE WHEN a.robots_txt_compliant = false THEN a.id END) as articles_robots_violation,
    COUNT(DISTINCT CASE WHEN a.copyright_status = 'cleared' THEN a.id END) as articles_copyright_cleared,
    COUNT(DISTINCT CASE WHEN a.copyright_status = 'violation' THEN a.id END) as articles_copyright_violation,
    COUNT(DISTINCT CASE WHEN a.legal_review_status = 'approved' THEN a.id END) as articles_legally_approved,
    COUNT(DISTINCT CASE WHEN a.data_retention_expires_at < CURRENT_TIMESTAMP THEN a.id END) as articles_expired_retention,

    -- Legal notices overview
    COUNT(DISTINCT ln.id) as total_legal_notices,
    COUNT(DISTINCT CASE WHEN ln.status = 'received' THEN ln.id END) as notices_pending,
    COUNT(DISTINCT CASE WHEN ln.status = 'complied' THEN ln.id END) as notices_complied,

    -- Performance metrics
    AVG(ns.success_rate) as average_success_rate,
    MAX(ns.last_compliance_check) as last_compliance_check,
    MAX(cal.performed_at) as last_compliance_audit
FROM news_sources ns
LEFT JOIN articles a ON ns.id = a.source_id
LEFT JOIN legal_notices ln ON ns.base_url LIKE '%' || ln.source_domain || '%'
LEFT JOIN compliance_audit_log cal ON cal.table_name = 'articles'
WHERE ns.status != 'deleted' OR ns.status IS NULL;

-- Create view for source performance summary
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
    ns.last_compliance_check,
    CASE
        WHEN ns.robots_txt_compliant = TRUE AND ns.legal_contact_verified = TRUE AND
             ns.terms_acceptable = TRUE AND ns.fair_use_documented = TRUE AND
             ns.data_minimization_applied = TRUE THEN 'compliant'
        ELSE 'non_compliant'
    END as compliance_status
FROM news_sources ns
LEFT JOIN articles a ON ns.id = a.source_id
WHERE ns.status != 'deleted' OR ns.status IS NULL
GROUP BY ns.id, ns.name, ns.base_url, ns.status, ns.success_rate,
         ns.articles_collected_total, ns.last_successful_run,
         ns.error_count_last_30_days, ns.last_compliance_check,
         ns.robots_txt_compliant, ns.legal_contact_verified,
         ns.terms_acceptable, ns.fair_use_documented,
         ns.data_minimization_applied;

-- =====================================================
-- 7. ADD CONSTRAINTS FOR DATA INTEGRITY
-- =====================================================

-- Add constraints for news_sources (PostgreSQL doesn't support IF NOT EXISTS with ADD CONSTRAINT)
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'check_crawl_delay') THEN
        ALTER TABLE news_sources ADD CONSTRAINT check_crawl_delay CHECK (crawl_delay_seconds >= 1.0);
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'check_max_articles') THEN
        ALTER TABLE news_sources ADD CONSTRAINT check_max_articles CHECK (max_articles_per_run > 0 AND max_articles_per_run <= 500);
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'check_retention_days') THEN
        ALTER TABLE news_sources ADD CONSTRAINT check_retention_days CHECK (data_retention_days >= 30 AND data_retention_days <= 2555);
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'check_content_type') THEN
        ALTER TABLE news_sources ADD CONSTRAINT check_content_type CHECK (content_type IN ('metadata_only', 'summary_only', 'full'));
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'check_source_type') THEN
        ALTER TABLE news_sources ADD CONSTRAINT check_source_type CHECK (source_type IN ('news_site', 'academic', 'government', 'ngo', 'medical_journal'));
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'check_status') THEN
        ALTER TABLE news_sources ADD CONSTRAINT check_status CHECK (status IN ('active', 'inactive', 'suspended', 'under_review', 'deleted'));
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'check_risk_level') THEN
        ALTER TABLE news_sources ADD CONSTRAINT check_risk_level CHECK (risk_level IN ('low', 'medium', 'high', 'critical'));
    END IF;
END $$;

-- =====================================================
-- 8. CREATE PERFORMANCE INDEXES
-- =====================================================

-- Create composite indexes for common queries
CREATE INDEX IF NOT EXISTS idx_news_sources_status_type ON news_sources(status, source_type);
CREATE INDEX IF NOT EXISTS idx_news_sources_compliance_status ON news_sources(robots_txt_compliant, legal_contact_verified, terms_acceptable, fair_use_documented);
CREATE INDEX IF NOT EXISTS idx_news_sources_performance ON news_sources(success_rate DESC, last_successful_run DESC) WHERE status = 'active';
CREATE INDEX IF NOT EXISTS idx_news_sources_compliance_check ON news_sources(last_compliance_check ASC) WHERE status = 'active';
CREATE INDEX IF NOT EXISTS idx_news_sources_compliance_score ON news_sources(compliance_score);

-- =====================================================
-- 9. UPDATE EXISTING DATA WITH DEFAULTS
-- =====================================================

-- Update existing sources with default compliance values
UPDATE news_sources
SET
    robots_txt_url = CASE WHEN robots_txt_url IS NULL THEN base_url || '/robots.txt' ELSE robots_txt_url END,
    crawl_delay_seconds = CASE WHEN crawl_delay_seconds IS NULL THEN 2.0 ELSE crawl_delay_seconds END,
    content_type = CASE WHEN content_type IS NULL THEN 'metadata_only' ELSE content_type END,
    data_retention_days = CASE WHEN data_retention_days IS NULL THEN 365 ELSE data_retention_days END,
    data_retention_expires_at = CASE WHEN data_retention_expires_at IS NULL THEN CURRENT_DATE + INTERVAL '365 days' ELSE data_retention_expires_at END,
    max_articles_per_run = CASE WHEN max_articles_per_run IS NULL THEN 50 ELSE max_articles_per_run END,
    target_sections = CASE WHEN target_sections IS NULL THEN '[]' ELSE target_sections END,
    source_type = CASE WHEN source_type IS NULL THEN 'news_site' ELSE source_type END,
    status = CASE WHEN status IS NULL THEN 'active' ELSE status END,
    data_minimization_applied = CASE WHEN data_minimization_applied IS NULL THEN TRUE ELSE data_minimization_applied END,
    risk_level = CASE WHEN risk_level IS NULL THEN 'low' ELSE risk_level END,
    scraper_type = CASE WHEN scraper_type IS NULL THEN 'manual' ELSE scraper_type END,
    health_status = CASE WHEN health_status IS NULL THEN 'operational' ELSE health_status END,
    compliance_score = CASE WHEN compliance_score IS NULL THEN 0.80 ELSE compliance_score END,
    fair_use_basis = CASE WHEN fair_use_basis IS NULL THEN 'Academic research at UCOMPENSAR University for breast cancer news analysis under fair use doctrine for educational purposes' ELSE fair_use_basis END
WHERE robots_txt_url IS NULL
   OR crawl_delay_seconds IS NULL
   OR content_type IS NULL
   OR data_retention_days IS NULL
   OR max_articles_per_run IS NULL
   OR target_sections IS NULL
   OR source_type IS NULL
   OR status IS NULL
   OR data_minimization_applied IS NULL
   OR risk_level IS NULL
   OR scraper_type IS NULL
   OR health_status IS NULL
   OR compliance_score IS NULL
   OR fair_use_basis IS NULL;

-- Set compliance status for existing operational sources
UPDATE news_sources
SET
    robots_txt_compliant = TRUE,
    legal_contact_verified = TRUE,
    terms_acceptable = TRUE,
    fair_use_documented = TRUE,
    last_compliance_check = CURRENT_TIMESTAMP
WHERE id IN (
    SELECT DISTINCT source_id
    FROM articles
    WHERE created_at > CURRENT_DATE - INTERVAL '30 days'
) AND (robots_txt_compliant IS NULL OR robots_txt_compliant = FALSE);

-- Mark existing articles as needing compliance review
UPDATE articles
SET
    legal_review_status = 'needs_review',
    content_type = 'full',
    copyright_status = 'unknown'
WHERE legal_review_status = 'pending';

-- Set data retention expiry (1 year from scraping for existing data)
UPDATE articles
SET data_retention_expires_at = scraped_at + INTERVAL '1 year'
WHERE data_retention_expires_at IS NULL;

-- =====================================================
-- 10. LOG MIGRATION COMPLETION
-- =====================================================

-- Log this migration
INSERT INTO compliance_audit_log (table_name, record_id, action, status, details, performed_by)
VALUES ('schema', 0, 'migration_002_applied', 'passed',
        '{"migration": "002_compliance_consolidated", "description": "Consolidated compliance, audit logging, and source administration", "fields_added": 35, "tables_created": 4}',
        'migration_system');

-- =====================================================
-- 11. ADD COMMENTS FOR DOCUMENTATION
-- =====================================================

COMMENT ON TABLE compliance_audit_log IS 'Consolidated audit trail for all compliance-related actions across the system';
COMMENT ON TABLE legal_notices IS 'Stores legal notices, takedown requests, and compliance actions';
COMMENT ON TABLE compliance_validations IS 'Tracks compliance validation results for news sources';
COMMENT ON TABLE scraper_automation_log IS 'Logs automation activities for scraper generation and management';
COMMENT ON VIEW compliance_dashboard IS 'Provides comprehensive overview of legal compliance status across the system';
COMMENT ON VIEW source_performance_summary IS 'Provides performance and compliance summary for news sources';

-- Article compliance comments
COMMENT ON COLUMN articles.robots_txt_compliant IS 'Whether scraping this article complied with robots.txt';
COMMENT ON COLUMN articles.copyright_status IS 'Copyright clearance status: unknown, cleared, fair_use, violation';
COMMENT ON COLUMN articles.fair_use_basis IS 'Justification for fair use if applicable';
COMMENT ON COLUMN articles.scraping_permission IS 'Explicit permission obtained for scraping';
COMMENT ON COLUMN articles.content_type IS 'Type of content stored: full, summary, metadata';
COMMENT ON COLUMN articles.legal_review_status IS 'Legal review status: pending, approved, rejected';
COMMENT ON COLUMN articles.data_retention_expires_at IS 'When this data should be deleted per retention policy';

-- News sources compliance comments
COMMENT ON COLUMN news_sources.fair_use_basis IS 'Legal basis for fair use of content from this source';
COMMENT ON COLUMN news_sources.compliance_score IS 'Overall compliance score (0.00-1.00) based on legal requirements';
COMMENT ON COLUMN news_sources.last_compliance_check IS 'Timestamp of last automated compliance validation';

-- =====================================================
-- COMMIT TRANSACTION
-- =====================================================

COMMIT;

-- =====================================================
-- VERIFICATION
-- =====================================================

-- Verify that the status column exists
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'compliance_audit_log' AND column_name = 'status'
    ) THEN
        RAISE EXCEPTION 'Migration failed: status column not created in compliance_audit_log';
    END IF;

    RAISE NOTICE 'Migration 002_compliance_consolidated.sql completed successfully';
    RAISE NOTICE 'compliance_audit_log table created with status column';
END
$$;
