import React from 'react';
import {
  CheckCircle,
  AlertTriangle,
  Clock,
  Shield,
  Edit,
  Globe,
  Mail
} from 'lucide-react';
import { NewsSource } from '@/pages/admin/SourcesAdminPage';

interface SourcesTableProps {
  sources: NewsSource[];
  onValidate: (sourceId: number) => void;
  onEdit: (source: NewsSource) => void;
  showComplianceColumns?: boolean;
  highlightNonCompliant?: boolean;
}

export const SourcesTable: React.FC<SourcesTableProps> = ({
  sources,
  onValidate,
  onEdit,
  showComplianceColumns = true,
  highlightNonCompliant = true
}) => {
  const getValidationStatusBadge = (status: string) => {
    switch (status) {
      case 'validated':
        return <div className="admin-compliance-indicator validated">
          <CheckCircle className="h-3 w-3" />
          Validado
        </div>;
      case 'pending':
        return <div className="admin-compliance-indicator pending">
          <Clock className="h-3 w-3" />
          Pendiente
        </div>;
      case 'failed':
        return <div className="admin-compliance-indicator failed">
          <AlertTriangle className="h-3 w-3" />
          Fallido
        </div>;
      default:
        return <div className="admin-compliance-indicator pending">{status}</div>;
    }
  };

  const getComplianceScore = (score?: number) => {
    if (!score) return 'N/A';
    const percentage = Math.round(score * 100);
    const colorClass = score >= 0.8 ? 'admin-stat-green' : score >= 0.6 ? 'admin-stat-yellow' : 'admin-stat-red';
    return <span className={`admin-stat-value ${colorClass}`} style={{ fontSize: '0.875rem' }}>{percentage}%</span>;
  };

  const getComplianceIndicators = (source: NewsSource) => {
    const indicators = [];

    if (source.robots_txt_url) {
      indicators.push(
        <div key="robots" style={{ display: 'flex', alignItems: 'center', gap: 'var(--admin-spacing-xs)', fontSize: '0.75rem', color: 'var(--admin-accent)' }}>
          <Shield className="h-3 w-3" />
          Robots.txt
        </div>
      );
    }

    if (source.terms_of_service_url) {
      indicators.push(
        <div key="tos" style={{ display: 'flex', alignItems: 'center', gap: 'var(--admin-spacing-xs)', fontSize: '0.75rem', color: 'var(--admin-primary)' }}>
          <Globe className="h-3 w-3" />
          Términos de Servicio
        </div>
      );
    }

    if (source.legal_contact_email) {
      indicators.push(
        <div key="contact" style={{ display: 'flex', alignItems: 'center', gap: 'var(--admin-spacing-xs)', fontSize: '0.75rem', color: '#9333ea' }}>
          <Mail className="h-3 w-3" />
          Contacto
        </div>
      );
    }

    if (source.fair_use_basis) {
      indicators.push(
        <div key="fair-use" style={{ display: 'flex', alignItems: 'center', gap: 'var(--admin-spacing-xs)', fontSize: '0.75rem', color: '#4f46e5' }}>
          <CheckCircle className="h-3 w-3" />
          Uso Justo
        </div>
      );
    }

    return indicators;
  };

  const isNonCompliant = (source: NewsSource) => {
    return source.validation_status === 'failed' ||
           source.validation_status === 'pending' ||
           (source.compliance_score && source.compliance_score < 0.8);
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return 'Nunca';
    return new Date(dateString).toLocaleDateString();
  };

  return (
    <div style={{ overflowX: 'auto' }}>
      <table className="admin-table">
        <thead>
          <tr>
            <th>Fuente</th>
            <th>URL</th>
            <th>País</th>
            <th>Idioma</th>
            {showComplianceColumns && (
              <>
                <th>Estado de Validación</th>
                <th>Puntuación de Cumplimiento</th>
                <th>Características de Cumplimiento</th>
                <th>Última Validación</th>
              </>
            )}
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {sources.map((source) => (
            <tr
              key={source.id}
              style={{
                ...(highlightNonCompliant && isNonCompliant(source)
                  ? { backgroundColor: '#fef2f2', borderColor: '#fecaca' }
                  : {})
              }}
            >
              <td style={{ fontWeight: '500' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--admin-spacing-sm)' }}>
                  <div>
                    <div style={{ fontWeight: '500', color: 'var(--admin-text-primary)' }}>{source.name}</div>
                    <div style={{ fontSize: '0.875rem', color: 'var(--admin-text-secondary)' }}>ID: {source.id}</div>
                  </div>
                </div>
              </td>

              <td>
                <a
                  href={source.base_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ color: 'var(--admin-primary)', textDecoration: 'none', fontSize: '0.875rem' }}
                  onMouseOver={(e) => (e.target as HTMLElement).style.textDecoration = 'underline'}
                  onMouseOut={(e) => (e.target as HTMLElement).style.textDecoration = 'none'}
                >
                  {source.base_url.length > 30
                    ? `${source.base_url.substring(0, 30)}...`
                    : source.base_url
                  }
                </a>
              </td>

              <td>{source.country}</td>

              <td>
                <div className="admin-compliance-indicator pending">
                  {source.language.toUpperCase()}
                </div>
              </td>

              {showComplianceColumns && (
                <>
                  <td>
                    {getValidationStatusBadge(source.validation_status)}
                    {source.validation_error && (
                      <div style={{ fontSize: '0.75rem', color: 'var(--admin-danger)', marginTop: 'var(--admin-spacing-xs)' }}>
                        {source.validation_error.substring(0, 50)}...
                      </div>
                    )}
                  </td>

                  <td>
                    {getComplianceScore(source.compliance_score)}
                  </td>

                  <td>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: 'var(--admin-spacing-xs)' }}>
                      {getComplianceIndicators(source)}
                    </div>
                  </td>

                  <td style={{ fontSize: '0.875rem', color: 'var(--admin-text-secondary)' }}>
                    {formatDate(source.last_validation_at)}
                  </td>
                </>
              )}

              <td>
                <div className={`admin-compliance-indicator ${source.is_active ? 'validated' : 'pending'}`}>
                  {source.is_active ? 'Activo' : 'Inactivo'}
                </div>
              </td>

              <td>
                <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--admin-spacing-sm)' }}>
                  <button
                    onClick={() => onEdit(source)}
                    className="admin-btn admin-btn-ghost"
                    style={{ fontSize: '0.875rem', padding: 'var(--admin-spacing-xs) var(--admin-spacing-sm)' }}
                  >
                    <Edit className="h-3 w-3" />
                    Editar
                  </button>

                  <button
                    onClick={() => onValidate(source.id)}
                    disabled={!source.is_active}
                    className="admin-btn admin-btn-ghost"
                    style={{
                      fontSize: '0.875rem',
                      padding: 'var(--admin-spacing-xs) var(--admin-spacing-sm)',
                      opacity: !source.is_active ? 0.5 : 1
                    }}
                  >
                    <Shield className="h-3 w-3" />
                    Validar
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {sources.length === 0 && (
        <div style={{ textAlign: 'center', padding: 'var(--admin-spacing-2xl)', color: 'var(--admin-text-secondary)' }}>
          No se encontraron fuentes de noticias. Agregue su primera fuente para comenzar.
        </div>
      )}
    </div>
  );
};
