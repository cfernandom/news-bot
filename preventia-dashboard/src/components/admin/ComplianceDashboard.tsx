import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';
import {
  Shield,
  TrendingUp,
  AlertTriangle,
  CheckCircle,
  Clock,
  Globe,
  FileText,
  Activity,
  BarChart3,
  Zap
} from 'lucide-react';
import { NewsSource } from '@/pages/admin/SourcesAdminPage';

interface ComplianceDashboardProps {
  sources: NewsSource[];
}

interface ComplianceWidget {
  id: string;
  title: string;
  value: string | number;
  change?: number;
  icon: React.ReactNode;
  color: 'green' | 'yellow' | 'red' | 'blue' | 'purple';
  description?: string;
}

export const ComplianceDashboard: React.FC<ComplianceDashboardProps> = ({ sources }) => {
  const [widgets, setWidgets] = useState<ComplianceWidget[]>([]);

  useEffect(() => {
    const calculateWidgets = (): ComplianceWidget[] => {
      const total = sources.length;
      const compliant = sources.filter(s => s.validation_status === 'validated').length;
      const pending = sources.filter(s => s.validation_status === 'pending').length;
      const failed = sources.filter(s => s.validation_status === 'failed').length;

      // Calculate compliance rate
      const complianceRate = total > 0 ? Math.round((compliant / total) * 100) : 0;

      // Calculate average compliance score
      const sourcesWithScore = sources.filter(s => s.compliance_score);
      const avgScore = sourcesWithScore.length > 0
        ? Math.round(sourcesWithScore.reduce((sum, s) => sum + (s.compliance_score || 0), 0) / sourcesWithScore.length * 100)
        : 0;

      // Count sources with specific compliance features
      const withRobotsTxt = sources.filter(s => s.robots_txt_url).length;
      const withTermsOfService = sources.filter(s => s.terms_of_service_url).length;
      const withLegalContact = sources.filter(s => s.legal_contact_email).length;
      const withFairUse = sources.filter(s => s.fair_use_basis).length;

      // Recent validations (last 7 days)
      const sevenDaysAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
      const recentValidations = sources.filter(s =>
        s.last_validation_at && new Date(s.last_validation_at) > sevenDaysAgo
      ).length;

      return [
        {
          id: 'compliance-rate',
          title: 'Compliance Rate',
          value: `${complianceRate}%`,
          icon: <Shield className="h-5 w-5" />,
          color: complianceRate >= 80 ? 'green' : complianceRate >= 60 ? 'yellow' : 'red',
          description: `${compliant} of ${total} sources fully compliant`
        },
        {
          id: 'avg-score',
          title: 'Average Score',
          value: `${avgScore}%`,
          icon: <BarChart3 className="h-5 w-5" />,
          color: avgScore >= 80 ? 'green' : avgScore >= 60 ? 'yellow' : 'red',
          description: `Based on ${sourcesWithScore.length} evaluated sources`
        },
        {
          id: 'pending-review',
          title: 'Pending Review',
          value: pending,
          icon: <Clock className="h-5 w-5" />,
          color: pending > 0 ? 'yellow' : 'green',
          description: `${pending} sources awaiting validation`
        },
        {
          id: 'failed-validation',
          title: 'Failed Validation',
          value: failed,
          icon: <AlertTriangle className="h-5 w-5" />,
          color: failed > 0 ? 'red' : 'green',
          description: `${failed} sources with compliance issues`
        },
        {
          id: 'robots-txt',
          title: 'Robots.txt',
          value: `${withRobotsTxt}/${total}`,
          icon: <Shield className="h-5 w-5" />,
          color: withRobotsTxt === total ? 'green' : 'yellow',
          description: 'Sources with robots.txt configured'
        },
        {
          id: 'terms-service',
          title: 'Terms of Service',
          value: `${withTermsOfService}/${total}`,
          icon: <FileText className="h-5 w-5" />,
          color: withTermsOfService === total ? 'green' : 'yellow',
          description: 'Sources with ToS documentation'
        },
        {
          id: 'legal-contact',
          title: 'Legal Contact',
          value: `${withLegalContact}/${total}`,
          icon: <Globe className="h-5 w-5" />,
          color: withLegalContact === total ? 'green' : 'yellow',
          description: 'Sources with legal contact info'
        },
        {
          id: 'fair-use',
          title: 'Fair Use Basis',
          value: `${withFairUse}/${total}`,
          icon: <CheckCircle className="h-5 w-5" />,
          color: withFairUse === total ? 'green' : 'yellow',
          description: 'Sources with fair use documentation'
        },
        {
          id: 'recent-validations',
          title: 'Recent Validations',
          value: recentValidations,
          icon: <Activity className="h-5 w-5" />,
          color: recentValidations > 0 ? 'green' : 'yellow',
          description: 'Validations in the last 7 days'
        }
      ];
    };

    setWidgets(calculateWidgets());
  }, [sources]);

  const getWidgetColorClasses = (color: string) => {
    switch (color) {
      case 'green':
        return {
          bg: 'admin-alert-success',
          text: 'admin-stat-green',
          icon: 'admin-stat-green',
          border: ''
        };
      case 'yellow':
        return {
          bg: 'admin-alert-warning',
          text: 'admin-stat-yellow',
          icon: 'admin-stat-yellow',
          border: ''
        };
      case 'red':
        return {
          bg: 'admin-alert-danger',
          text: 'admin-stat-red',
          icon: 'admin-stat-red',
          border: ''
        };
      case 'blue':
        return {
          bg: 'admin-alert-info',
          text: 'admin-stat-blue',
          icon: 'admin-stat-blue',
          border: ''
        };
      case 'purple':
        return {
          bg: 'admin-alert-info', // No direct purple in admin-theme, using info as fallback
          text: 'admin-stat-blue',
          icon: 'admin-stat-blue',
          border: ''
        };
      default:
        return {
          bg: 'admin-secondary',
          text: 'admin-text-primary',
          icon: 'admin-text-secondary',
          border: 'admin-border'
        };
    }
  };

  const getCriticalIssues = () => {
    const issues = [];

    const failed = sources.filter(s => s.validation_status === 'failed');
    if (failed.length > 0) {
      issues.push({
        severity: 'high',
        title: 'Failed Validations',
        description: `${failed.length} sources failed compliance validation`,
        sources: failed.map(s => s.name).slice(0, 3)
      });
    }

    const noRobots = sources.filter(s => !s.robots_txt_url);
    if (noRobots.length > 0) {
      issues.push({
        severity: 'medium',
        title: 'Missing Robots.txt',
        description: `${noRobots.length} sources missing robots.txt configuration`,
        sources: noRobots.map(s => s.name).slice(0, 3)
      });
    }

    const noContact = sources.filter(s => !s.legal_contact_email);
    if (noContact.length > 0) {
      issues.push({
        severity: 'medium',
        title: 'Missing Legal Contact',
        description: `${noContact.length} sources missing legal contact information`,
        sources: noContact.map(s => s.name).slice(0, 3)
      });
    }

    return issues;
  };

  const criticalIssues = getCriticalIssues();

  return (
    <div className="admin-space-y-6">
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--admin-spacing-sm)' }}>
          <Shield className="h-6 w-6" style={{ color: 'var(--admin-primary)' }} />
          <h2 style={{ fontSize: '1.25rem', fontWeight: '600', color: 'var(--admin-text-primary)' }}>Compliance Dashboard</h2>
        </div>
        <Badge variant="secondary" style={{ display: 'flex', alignItems: 'center', gap: 'var(--admin-spacing-xs)' }}>
          <Zap className="h-3 w-3" />
          Live
        </Badge>
      </div>

      {/* Critical Issues Alert */}
      {criticalIssues.length > 0 && (
        <div className="admin-alert admin-alert-danger">
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription>
            <div className="admin-space-y-2">
              <div style={{ fontWeight: '500' }}>Critical Issues Detected:</div>
              {criticalIssues.map((issue, index) => (
                <div key={index} style={{ fontSize: '0.875rem' }}>
                  • <strong style={{ fontWeight: '600' }}>{issue.title}:</strong> {issue.description}
                  {issue.sources.length > 0 && (
                    <div style={{ marginLeft: 'var(--admin-spacing-md)', color: 'var(--admin-text-muted)' }}>
                      Affected: {issue.sources.join(', ')}
                      {issue.sources.length < sources.length && ' ...'}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </AlertDescription>
        </div>
      )}

      {/* Widgets Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: 'var(--admin-spacing-md)' }}>
        {widgets.map((widget) => {
          const colors = getWidgetColorClasses(widget.color);

          return (
            <div key={widget.id} className={`admin-card ${colors.bg}`} style={{ borderColor: 'var(--admin-border)' }}>
              <div style={{ paddingBottom: 'var(--admin-spacing-sm)' }}>
                <div style={{ fontSize: '0.875rem', fontWeight: '500', color: 'var(--admin-text-muted)', display: 'flex', alignItems: 'center', gap: 'var(--admin-spacing-sm)' }}>
                  <span className={colors.icon}>{widget.icon}</span>
                  {widget.title}
                </div>
              </div>
              <CardContent>
                <div className="admin-space-y-2">
                  <div style={{ fontSize: '1.5rem', fontWeight: '700' }} className={colors.text}>
                    {widget.value}
                  </div>
                  {widget.description && (
                    <div style={{ fontSize: '0.75rem', color: 'var(--admin-text-muted)' }}>
                      {widget.description}
                    </div>
                  )}
                </div>
              </CardContent>
            </div>
          );
        })}
      </div>

      {/* Compliance Summary */}
      <div className="admin-card">
        <div style={{ paddingBottom: 'var(--admin-spacing-md)' }}>
          <div style={{ fontSize: '1.125rem', fontWeight: '600', display: 'flex', alignItems: 'center', gap: 'var(--admin-spacing-sm)' }}>
            <TrendingUp className="h-4 w-4" />
            Compliance Summary
          </div>
        </div>
        <CardContent>
          <div className="admin-space-y-4">
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: 'var(--admin-spacing-md)' }}>
              <div className="admin-space-y-2">
                <div style={{ fontSize: '0.875rem', fontWeight: '500' }}>Status Distribution</div>
                <div className="admin-space-y-1">
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.875rem' }}>
                    <span className="admin-stat-green">✓ Compliant</span>
                    <span>{sources.filter(s => s.validation_status === 'validated').length}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.875rem' }}>
                    <span className="admin-stat-yellow">⏳ Pending</span>
                    <span>{sources.filter(s => s.validation_status === 'pending').length}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.875rem' }}>
                    <span className="admin-stat-red">✗ Failed</span>
                    <span>{sources.filter(s => s.validation_status === 'failed').length}</span>
                  </div>
                </div>
              </div>

              <div className="admin-space-y-2">
                <div style={{ fontSize: '0.875rem', fontWeight: '500' }}>Feature Coverage</div>
                <div className="admin-space-y-1">
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.875rem' }}>
                    <span>Robots.txt</span>
                    <span>{Math.round((sources.filter(s => s.robots_txt_url).length / sources.length) * 100)}%</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.875rem' }}>
                    <span>Terms of Service</span>
                    <span>{Math.round((sources.filter(s => s.terms_of_service_url).length / sources.length) * 100)}%</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.875rem' }}>
                    <span>Legal Contact</span>
                    <span>{Math.round((sources.filter(s => s.legal_contact_email).length / sources.length) * 100)}%</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.875rem' }}>
                    <span>Fair Use</span>
                    <span>{Math.round((sources.filter(s => s.fair_use_basis).length / sources.length) * 100)}%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </div>
    </div>
  );
};

export default ComplianceDashboard;
