-- Migration 002: Legal Compliance Enhancements
-- Adds compliance tracking fields and modifies content storage for legal compliance
-- Created: 2025-06-29
-- Purpose: Address copyright, privacy, and ethical scraping concerns

-- Add compliance tracking fields to articles table
ALTER TABLE articles ADD COLUMN IF NOT EXISTS robots_txt_compliant BOOLEAN DEFAULT NULL;
ALTER TABLE articles ADD COLUMN IF NOT EXISTS copyright_status VARCHAR(50) DEFAULT 'unknown';
ALTER TABLE articles ADD COLUMN IF NOT EXISTS fair_use_basis TEXT;
ALTER TABLE articles ADD COLUMN IF NOT EXISTS scraping_permission BOOLEAN DEFAULT NULL;
ALTER TABLE articles ADD COLUMN IF NOT EXISTS content_type VARCHAR(20) DEFAULT 'full'; -- 'full', 'summary', 'metadata'
ALTER TABLE articles ADD COLUMN IF NOT EXISTS legal_review_status VARCHAR(50) DEFAULT 'pending';
ALTER TABLE articles ADD COLUMN IF NOT EXISTS data_retention_expires_at TIMESTAMP;

-- Add indexes for compliance queries
CREATE INDEX IF NOT EXISTS idx_articles_copyright_status ON articles(copyright_status);
CREATE INDEX IF NOT EXISTS idx_articles_legal_review ON articles(legal_review_status);
CREATE INDEX IF NOT EXISTS idx_articles_retention_expires ON articles(data_retention_expires_at);
CREATE INDEX IF NOT EXISTS idx_articles_robots_compliant ON articles(robots_txt_compliant);

-- Add compliance tracking to news_sources
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS robots_txt_url VARCHAR(500);
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS robots_txt_last_checked TIMESTAMP;
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS crawl_delay_seconds INTEGER DEFAULT 2;
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS scraping_allowed BOOLEAN DEFAULT NULL;
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS terms_of_service_url VARCHAR(500);
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS terms_reviewed_at TIMESTAMP;
ALTER TABLE news_sources ADD COLUMN IF NOT EXISTS legal_contact_email VARCHAR(255);

-- Create table for compliance audit log
CREATE TABLE IF NOT EXISTS compliance_audit_log (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(50) NOT NULL,
    record_id INTEGER NOT NULL,
    action VARCHAR(50) NOT NULL, -- 'robots_check', 'copyright_review', 'content_removal'
    status VARCHAR(50) NOT NULL, -- 'passed', 'failed', 'pending'
    details JSONB,
    performed_by VARCHAR(100) DEFAULT 'system',
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for compliance_audit_log
CREATE INDEX IF NOT EXISTS idx_audit_table_record ON compliance_audit_log(table_name, record_id);
CREATE INDEX IF NOT EXISTS idx_audit_action ON compliance_audit_log(action);
CREATE INDEX IF NOT EXISTS idx_audit_status ON compliance_audit_log(status);
CREATE INDEX IF NOT EXISTS idx_audit_performed_at ON compliance_audit_log(performed_at);

-- Create table for legal notices and takedown requests
CREATE TABLE IF NOT EXISTS legal_notices (
    id SERIAL PRIMARY KEY,
    notice_type VARCHAR(50) NOT NULL, -- 'dmca', 'cease_desist', 'privacy_request'
    source_domain VARCHAR(255) NOT NULL,
    affected_articles JSONB, -- Array of article IDs
    notice_content TEXT,
    requester_contact VARCHAR(255),
    received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'received', -- 'received', 'reviewing', 'complied', 'disputed'
    response_sent_at TIMESTAMP,
    compliance_actions JSONB, -- Actions taken to comply
    notes TEXT
);

-- Create indexes for legal_notices
CREATE INDEX IF NOT EXISTS idx_notices_type ON legal_notices(notice_type);
CREATE INDEX IF NOT EXISTS idx_notices_domain ON legal_notices(source_domain);
CREATE INDEX IF NOT EXISTS idx_notices_status ON legal_notices(status);
CREATE INDEX IF NOT EXISTS idx_notices_received ON legal_notices(received_at);

-- Create view for compliance dashboard
CREATE OR REPLACE VIEW compliance_dashboard AS
SELECT
    -- Source compliance overview
    COUNT(DISTINCT ns.id) as total_sources,
    COUNT(DISTINCT CASE WHEN ns.scraping_allowed = true THEN ns.id END) as sources_permitted,
    COUNT(DISTINCT CASE WHEN ns.scraping_allowed = false THEN ns.id END) as sources_blocked,
    COUNT(DISTINCT CASE WHEN ns.scraping_allowed IS NULL THEN ns.id END) as sources_unknown,

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

    -- Recent activity
    MAX(cal.performed_at) as last_compliance_check
FROM news_sources ns
LEFT JOIN articles a ON ns.id = a.source_id
LEFT JOIN legal_notices ln ON ns.base_url LIKE '%' || ln.source_domain || '%'
LEFT JOIN compliance_audit_log cal ON cal.table_name = 'articles';

-- Add comments for documentation
COMMENT ON TABLE compliance_audit_log IS 'Tracks all compliance-related actions and checks';
COMMENT ON TABLE legal_notices IS 'Stores legal notices, takedown requests, and compliance actions';
COMMENT ON VIEW compliance_dashboard IS 'Provides overview of legal compliance status across the system';

COMMENT ON COLUMN articles.robots_txt_compliant IS 'Whether scraping this article complied with robots.txt';
COMMENT ON COLUMN articles.copyright_status IS 'Copyright clearance status: unknown, cleared, fair_use, violation';
COMMENT ON COLUMN articles.fair_use_basis IS 'Justification for fair use if applicable';
COMMENT ON COLUMN articles.scraping_permission IS 'Explicit permission obtained for scraping';
COMMENT ON COLUMN articles.content_type IS 'Type of content stored: full, summary, metadata';
COMMENT ON COLUMN articles.legal_review_status IS 'Legal review status: pending, approved, rejected';
COMMENT ON COLUMN articles.data_retention_expires_at IS 'When this data should be deleted per retention policy';

-- Insert default compliance settings for existing sources
UPDATE news_sources
SET
    crawl_delay_seconds = 2,
    robots_txt_url = base_url || '/robots.txt'
WHERE robots_txt_url IS NULL;

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

-- Log this migration
INSERT INTO compliance_audit_log (table_name, record_id, action, status, details, performed_by)
VALUES ('schema', 0, 'migration_002_applied', 'passed',
        '{"migration": "002_legal_compliance", "fields_added": 14, "tables_created": 2}',
        'migration_system');
