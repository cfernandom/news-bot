import React from 'react';
import {
  Shield,
  CheckCircle,
  AlertTriangle,
  Clock,
  TrendingUp,
  AlertCircle
} from 'lucide-react';

interface ComplianceDashboard {
  total_sources: number;
  compliant_sources: number;
  pending_review: number;
  failed_validation: number;
  compliance_rate: number;
  sources_needing_attention: number;
  dashboard_updated_at: string;
}

interface ComplianceStatusHeaderProps {
  dashboard: ComplianceDashboard;
}

export const ComplianceStatusHeader: React.FC<ComplianceStatusHeaderProps> = ({
  dashboard
}) => {

  const formatDateTime = (dateString: string) => {
    return new Date(dateString).toLocaleString();
  };

  return (
    <div className="admin-card">
      <div className="admin-card-header">
        <h3 style={{ fontSize: '1.25rem', fontWeight: '600', color: 'var(--admin-text-primary)', marginBottom: '0.5rem' }}>
          Compliance Overview
        </h3>
        <p style={{ fontSize: '0.875rem', color: 'var(--admin-text-secondary)' }}>
          Real-time compliance status across all news sources
        </p>
      </div>
      <div style={{ display: 'grid', gap: 'var(--admin-spacing-lg)', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))' }}>
        {/* Total Sources */}
        <div className="admin-stat-card">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 'var(--admin-spacing-sm)' }}>
            <div style={{ fontSize: '0.875rem', fontWeight: '500', color: 'var(--admin-text-primary)' }}>Total Sources</div>
            <Shield className="h-4 w-4" style={{ color: 'var(--admin-text-muted)' }} />
          </div>
          <div className="admin-stat-value admin-stat-blue">{dashboard.total_sources}</div>
          <div className="admin-stat-label">
            Active news sources
          </div>
        </div>

        {/* Compliance Rate */}
        <div className="admin-stat-card">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 'var(--admin-spacing-sm)' }}>
            <div style={{ fontSize: '0.875rem', fontWeight: '500', color: 'var(--admin-text-primary)' }}>Compliance Rate</div>
            <TrendingUp className="h-4 w-4" style={{ color: 'var(--admin-text-muted)' }} />
          </div>
          <div className={`admin-stat-value ${
            dashboard.compliance_rate >= 90 ? 'admin-stat-green' :
            dashboard.compliance_rate >= 75 ? 'admin-stat-yellow' : 'admin-stat-red'
          }`}>
            {dashboard.compliance_rate.toFixed(1)}%
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--admin-spacing-sm)', marginTop: 'var(--admin-spacing-xs)' }}>
            <div className={`admin-compliance-indicator ${
              dashboard.compliance_rate >= 90 ? 'validated' :
              dashboard.compliance_rate >= 75 ? 'pending' : 'failed'
            }`}>
              {dashboard.compliant_sources}/{dashboard.total_sources} compliant
            </div>
          </div>
        </div>

        {/* Compliant Sources */}
        <div className="admin-stat-card">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 'var(--admin-spacing-sm)' }}>
            <div style={{ fontSize: '0.875rem', fontWeight: '500', color: 'var(--admin-text-primary)' }}>Compliant Sources</div>
            <CheckCircle className="h-4 w-4" style={{ color: 'var(--admin-accent)' }} />
          </div>
          <div className="admin-stat-value admin-stat-green">
            {dashboard.compliant_sources}
          </div>
          <div className="admin-stat-label">
            Fully validated sources
          </div>
        </div>

        {/* Attention Required */}
        <div className="admin-stat-card">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 'var(--admin-spacing-sm)' }}>
            <div style={{ fontSize: '0.875rem', fontWeight: '500', color: 'var(--admin-text-primary)' }}>Attention Required</div>
            <AlertCircle className="h-4 w-4" style={{ color: 'var(--admin-warning)' }} />
          </div>
          <div className="admin-stat-value admin-stat-yellow">
            {dashboard.sources_needing_attention}
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--admin-spacing-xs)', marginTop: 'var(--admin-spacing-xs)' }}>
            {dashboard.pending_review > 0 && (
              <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--admin-spacing-xs)', fontSize: '0.75rem', color: 'var(--admin-text-secondary)' }}>
                <Clock className="h-3 w-3" />
                {dashboard.pending_review} pending review
              </div>
            )}
            {dashboard.failed_validation > 0 && (
              <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--admin-spacing-xs)', fontSize: '0.75rem', color: 'var(--admin-danger)' }}>
                <AlertTriangle className="h-3 w-3" />
                {dashboard.failed_validation} failed validation
              </div>
            )}
          </div>
        </div>

        {/* Status Summary Card */}
        <div className="admin-compliance-card" style={{ gridColumn: '1 / -1' }}>
          <div className="admin-compliance-header">
            <div className="admin-compliance-title">
              <Shield className="h-5 w-5" style={{ color: 'var(--admin-primary)' }} />
              <span>Compliance Status Summary</span>
            </div>
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', gap: 'var(--admin-spacing-lg)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--admin-spacing-sm)' }}>
              <CheckCircle className="h-4 w-4" style={{ color: 'var(--admin-accent)' }} />
              <span style={{ fontSize: '0.875rem', fontWeight: '500', color: 'var(--admin-text-primary)' }}>
                {dashboard.compliant_sources} Validated
              </span>
            </div>

            {dashboard.pending_review > 0 && (
              <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--admin-spacing-sm)' }}>
                <Clock className="h-4 w-4" style={{ color: 'var(--admin-warning)' }} />
                <span style={{ fontSize: '0.875rem', fontWeight: '500', color: 'var(--admin-text-primary)' }}>
                  {dashboard.pending_review} Pending Review
                </span>
              </div>
            )}

            {dashboard.failed_validation > 0 && (
              <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--admin-spacing-sm)' }}>
                <AlertTriangle className="h-4 w-4" style={{ color: 'var(--admin-danger)' }} />
                <span style={{ fontSize: '0.875rem', fontWeight: '500', color: 'var(--admin-text-primary)' }}>
                  {dashboard.failed_validation} Failed Validation
                </span>
              </div>
            )}

            <div style={{ marginLeft: 'auto', fontSize: '0.75rem', color: 'var(--admin-text-muted)' }}>
              Last updated: {formatDateTime(dashboard.dashboard_updated_at)}
            </div>
          </div>

          {/* Legal Compliance Notice */}
          <div className="admin-alert admin-alert-info" style={{ marginTop: 'var(--admin-spacing-lg)' }}>
            <Shield className="h-4 w-4" style={{ marginTop: '0.125rem' }} />
            <div style={{ fontSize: '0.75rem' }}>
              <strong>Legal Compliance Framework:</strong> All sources maintain compliance with
              Colombian Law 1581/2012, GDPR standards, and academic fair use doctrine.
              Compliance rate must remain at 100% for legal protection.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
