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
          Resumen de Cumplimiento
        </h3>
        <p style={{ fontSize: '0.875rem', color: 'var(--admin-text-secondary)' }}>
          Estado de cumplimiento en tiempo real de todas las fuentes de noticias
        </p>
      </div>
      <div style={{ display: 'grid', gap: 'var(--admin-spacing-lg)', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))' }}>
        {/* Total Sources */}
        <div className="admin-stat-card">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 'var(--admin-spacing-sm)' }}>
            <div style={{ fontSize: '0.875rem', fontWeight: '500', color: 'var(--admin-text-primary)' }}>Total Fuentes</div>
            <Shield className="h-4 w-4" style={{ color: 'var(--admin-text-muted)' }} />
          </div>
          <div className="admin-stat-value admin-stat-blue">{dashboard.total_sources}</div>
          <div className="admin-stat-label">
            Fuentes de noticias activas
          </div>
        </div>

        {/* Compliance Rate */}
        <div className="admin-stat-card">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 'var(--admin-spacing-sm)' }}>
            <div style={{ fontSize: '0.875rem', fontWeight: '500', color: 'var(--admin-text-primary)' }}>Tasa de Cumplimiento</div>
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
              {dashboard.compliant_sources}/{dashboard.total_sources} conformes
            </div>
          </div>
        </div>

        {/* Compliant Sources */}
        <div className="admin-stat-card">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 'var(--admin-spacing-sm)' }}>
            <div style={{ fontSize: '0.875rem', fontWeight: '500', color: 'var(--admin-text-primary)' }}>Fuentes Conformas</div>
            <CheckCircle className="h-4 w-4" style={{ color: 'var(--admin-accent)' }} />
          </div>
          <div className="admin-stat-value admin-stat-green">
            {dashboard.compliant_sources}
          </div>
          <div className="admin-stat-label">
            Fuentes totalmente validadas
          </div>
        </div>

        {/* Attention Required */}
        <div className="admin-stat-card">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 'var(--admin-spacing-sm)' }}>
            <div style={{ fontSize: '0.875rem', fontWeight: '500', color: 'var(--admin-text-primary)' }}>Atención Requerida</div>
            <AlertCircle className="h-4 w-4" style={{ color: 'var(--admin-warning)' }} />
          </div>
          <div className="admin-stat-value admin-stat-yellow">
            {dashboard.sources_needing_attention}
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--admin-spacing-xs)', marginTop: 'var(--admin-spacing-xs)' }}>
            {dashboard.pending_review > 0 && (
              <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--admin-spacing-xs)', fontSize: '0.75rem', color: 'var(--admin-text-secondary)' }}>
                <Clock className="h-3 w-3" />
                {dashboard.pending_review} pendientes de revisión
              </div>
            )}
            {dashboard.failed_validation > 0 && (
              <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--admin-spacing-xs)', fontSize: '0.75rem', color: 'var(--admin-danger)' }}>
                <AlertTriangle className="h-3 w-3" />
                {dashboard.failed_validation} validaciones fallidas
              </div>
            )}
          </div>
        </div>

        {/* Status Summary Card */}
        <div className="admin-compliance-card" style={{ gridColumn: '1 / -1' }}>
          <div className="admin-compliance-header">
            <div className="admin-compliance-title">
              <Shield className="h-5 w-5" style={{ color: 'var(--admin-primary)' }} />
              <span>Resumen del Estado de Cumplimiento</span>
            </div>
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', gap: 'var(--admin-spacing-lg)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--admin-spacing-sm)' }}>
              <CheckCircle className="h-4 w-4" style={{ color: 'var(--admin-accent)' }} />
              <span style={{ fontSize: '0.875rem', fontWeight: '500', color: 'var(--admin-text-primary)' }}>
                {dashboard.compliant_sources} Validadas
              </span>
            </div>

            {dashboard.pending_review > 0 && (
              <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--admin-spacing-sm)' }}>
                <Clock className="h-4 w-4" style={{ color: 'var(--admin-warning)' }} />
                <span style={{ fontSize: '0.875rem', fontWeight: '500', color: 'var(--admin-text-primary)' }}>
                  {dashboard.pending_review} Pendientes de Revisión
                </span>
              </div>
            )}

            {dashboard.failed_validation > 0 && (
              <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--admin-spacing-sm)' }}>
                <AlertTriangle className="h-4 w-4" style={{ color: 'var(--admin-danger)' }} />
                <span style={{ fontSize: '0.875rem', fontWeight: '500', color: 'var(--admin-text-primary)' }}>
                  {dashboard.failed_validation} Validaciones Fallidas
                </span>
              </div>
            )}

            <div style={{ marginLeft: 'auto', fontSize: '0.75rem', color: 'var(--admin-text-muted)' }}>
              Última actualización: {formatDateTime(dashboard.dashboard_updated_at)}
            </div>
          </div>

          {/* Legal Compliance Notice */}
          <div className="admin-alert admin-alert-info" style={{ marginTop: 'var(--admin-spacing-lg)' }}>
            <Shield className="h-4 w-4" style={{ marginTop: '0.125rem' }} />
            <div style={{ fontSize: '0.75rem' }}>
              <strong>Marco de Cumplimiento Legal:</strong> Todas las fuentes mantienen el cumplimiento con
              la Ley Colombiana 1581/2012, los estándares GDPR y la doctrina de uso justo académico.
              La tasa de cumplimiento debe permanecer al 100% para protección legal.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
