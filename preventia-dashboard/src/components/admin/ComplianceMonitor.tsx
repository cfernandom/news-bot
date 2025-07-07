import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';
import {
  RefreshCw,
  AlertCircle,
  CheckCircle,
  Clock,
  TrendingUp,
  Activity,
  Shield,
  Globe
} from 'lucide-react';
import { NewsSource } from '@/pages/admin/SourcesAdminPage';
import { ComplianceStatusIndicator } from './ComplianceStatusIndicator';

interface ComplianceMonitorProps {
  sources: NewsSource[];
  onRefresh?: () => void;
  refreshInterval?: number; // in seconds
}

interface ComplianceStats {
  total: number;
  compliant: number;
  pending: number;
  failed: number;
  lastUpdated: Date;
}

export const ComplianceMonitor: React.FC<ComplianceMonitorProps> = ({
  sources,
  onRefresh,
  refreshInterval = 30
}) => {
  const [stats, setStats] = useState<ComplianceStats>({
    total: 0,
    compliant: 0,
    pending: 0,
    failed: 0,
    lastUpdated: new Date()
  });
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [nextRefresh, setNextRefresh] = useState(refreshInterval);

  // Calculate compliance statistics
  const calculateStats = (): ComplianceStats => {
    const total = sources.length;
    const compliant = sources.filter(s => s.validation_status === 'validated').length;
    const pending = sources.filter(s => s.validation_status === 'pending').length;
    const failed = sources.filter(s => s.validation_status === 'failed').length;

    return {
      total,
      compliant,
      pending,
      failed,
      lastUpdated: new Date()
    };
  };

  // Update stats when sources change
  useEffect(() => {
    setStats(calculateStats());
  }, [sources]);

  // Auto-refresh countdown
  useEffect(() => {
    if (refreshInterval <= 0) return;

    const interval = setInterval(() => {
      setNextRefresh(prev => {
        if (prev <= 1) {
          handleRefresh();
          return refreshInterval;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [refreshInterval]);

  const handleRefresh = async () => {
    setIsRefreshing(true);
    try {
      await onRefresh?.();
      setStats(calculateStats());
    } catch (error) {
      console.error('Failed to refresh compliance data:', error);
    } finally {
      setIsRefreshing(false);
    }
  };

  const getComplianceRate = () => {
    if (stats.total === 0) return 0;
    return Math.round((stats.compliant / stats.total) * 100);
  };

  const getStatusColor = (rate: number) => {
    if (rate >= 80) return 'text-green-600';
    if (rate >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getRecentlyUpdated = () => {
    const recent = sources.filter(source => {
      if (!source.last_validation_at) return false;
      const lastValidated = new Date(source.last_validation_at);
      const hourAgo = new Date(Date.now() - 60 * 60 * 1000);
      return lastValidated > hourAgo;
    });
    return recent;
  };

  const getStaleValidations = () => {
    const stale = sources.filter(source => {
      if (!source.last_validation_at) return true;
      const lastValidated = new Date(source.last_validation_at);
      const dayAgo = new Date(Date.now() - 24 * 60 * 60 * 1000);
      return lastValidated < dayAgo;
    });
    return stale;
  };

  const recentlyUpdated = getRecentlyUpdated();
  const staleValidations = getStaleValidations();
  const complianceRate = getComplianceRate();

  return (
    <div className="admin-space-y-4">
      {/* Header with refresh controls */}
      <div className="admin-compliance-header">
        <div className="admin-compliance-title">
          <Activity className="h-5 w-5" style={{ color: 'var(--admin-primary)' }} />
          <span>Monitor de Cumplimiento</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--admin-spacing-sm)' }}>
          <span style={{ fontSize: '0.875rem', color: 'var(--admin-text-secondary)' }}>
            Próxima actualización: {nextRefresh}s
          </span>
          <button
            onClick={handleRefresh}
            disabled={isRefreshing}
            className="admin-btn admin-btn-secondary"
            style={{ fontSize: '0.875rem', padding: 'var(--admin-spacing-sm) var(--admin-spacing-md)' }}
          >
            <RefreshCw className={`h-4 w-4 ${isRefreshing ? 'animate-spin' : ''}`} />
            Actualizar
          </button>
        </div>
      </div>

      {/* Overall compliance status */}
      <div className="admin-compliance-card">
        <div className="admin-compliance-header">
          <div className="admin-compliance-title">
            <Shield className="h-4 w-4" style={{ color: 'var(--admin-primary)' }} />
            <span>Estado General de Cumplimiento</span>
          </div>
        </div>
        <div className="admin-compliance-stats">
          <div className="admin-stat-card">
            <div className="admin-stat-value admin-stat-blue">{stats.total}</div>
            <div className="admin-stat-label">Total Fuentes</div>
          </div>
          <div className="admin-stat-card">
            <div className="admin-stat-value admin-stat-green">{stats.compliant}</div>
            <div className="admin-stat-label">Conformes</div>
          </div>
          <div className="admin-stat-card">
            <div className="admin-stat-value admin-stat-yellow">{stats.pending}</div>
            <div className="admin-stat-label">Pendientes</div>
          </div>
          <div className="admin-stat-card">
            <div className="admin-stat-value admin-stat-red">{stats.failed}</div>
            <div className="admin-stat-label">Fallidas</div>
          </div>
        </div>

        <div style={{ marginTop: 'var(--admin-spacing-lg)', paddingTop: 'var(--admin-spacing-lg)', borderTop: '1px solid var(--admin-border)' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <span style={{ fontSize: '0.875rem', fontWeight: '500', color: 'var(--admin-text-primary)' }}>Tasa de Cumplimiento</span>
            <span className={`admin-stat-value ${
              complianceRate >= 80 ? 'admin-stat-green' :
              complianceRate >= 60 ? 'admin-stat-yellow' : 'admin-stat-red'
            }`} style={{ fontSize: '1.125rem' }}>
              {complianceRate}%
            </span>
          </div>
          <div className="admin-progress-bar">
            <div
              className={`admin-progress-fill ${
                complianceRate >= 80 ? '' :
                complianceRate >= 60 ? 'warning' : 'danger'
              }`}
              style={{ width: `${complianceRate}%` }}
            />
          </div>
        </div>
      </div>

      {/* Active alerts */}
      {(stats.failed > 0 || staleValidations.length > 0) && (
        <div className="admin-space-y-4">
          {stats.failed > 0 && (
            <div className="admin-alert admin-alert-danger">
              <AlertCircle className="h-4 w-4" />
              <div>
                <strong>{stats.failed} fuente{stats.failed > 1 ? 's' : ''}</strong> fallaron la validación de cumplimiento.
                Revise y solucione los problemas inmediatamente.
              </div>
            </div>
          )}

          {staleValidations.length > 0 && (
            <div className="admin-alert admin-alert-warning">
              <Clock className="h-4 w-4" />
              <div>
                <strong>{staleValidations.length} fuente{staleValidations.length > 1 ? 's' : ''}</strong> necesitan
                actualización de validación (más de 24 horas).
              </div>
            </div>
          )}
        </div>
      )}

      {/* Recent activity */}
      <div className="admin-compliance-card">
        <div className="admin-compliance-header">
          <div className="admin-compliance-title">
            <TrendingUp className="h-4 w-4" style={{ color: 'var(--admin-primary)' }} />
            <span>Actividad Reciente</span>
          </div>
        </div>
        <div className="admin-space-y-6">
          {recentlyUpdated.length > 0 ? (
            recentlyUpdated.slice(0, 5).map((source, index) => (
              <div key={index} style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: 'var(--admin-spacing-sm)',
                backgroundColor: 'var(--admin-secondary)',
                borderRadius: 'var(--admin-radius)'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--admin-spacing-md)' }}>
                  <Globe className="h-4 w-4" style={{ color: 'var(--admin-primary)' }} />
                  <div>
                    <div style={{ fontWeight: '500', fontSize: '0.875rem', color: 'var(--admin-text-primary)' }}>{source.name}</div>
                    <div style={{ fontSize: '0.75rem', color: 'var(--admin-text-secondary)' }}>
                      {source.last_validation_at &&
                        new Date(source.last_validation_at).toLocaleString()}
                    </div>
                  </div>
                </div>
                <ComplianceStatusIndicator source={source} size="sm" />
              </div>
            ))
          ) : (
            <div style={{ textAlign: 'center', padding: 'var(--admin-spacing-xl)', color: 'var(--admin-text-secondary)' }}>
              <Clock className="h-8 w-8" style={{ margin: '0 auto var(--admin-spacing-sm) auto', opacity: '0.5' }} />
              <p>No hay actividad de validación reciente</p>
            </div>
          )}
        </div>
      </div>

      {/* Last updated timestamp */}
      <div style={{ textAlign: 'center', fontSize: '0.75rem', color: 'var(--admin-text-muted)' }}>
        Última actualización: {stats.lastUpdated.toLocaleString()}
      </div>
    </div>
  );
};

export default ComplianceMonitor;
