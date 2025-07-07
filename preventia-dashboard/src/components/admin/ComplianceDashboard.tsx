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
          bg: 'bg-green-50',
          text: 'text-green-700',
          icon: 'text-green-600',
          border: 'border-green-200'
        };
      case 'yellow':
        return {
          bg: 'bg-yellow-50',
          text: 'text-yellow-700',
          icon: 'text-yellow-600',
          border: 'border-yellow-200'
        };
      case 'red':
        return {
          bg: 'bg-red-50',
          text: 'text-red-700',
          icon: 'text-red-600',
          border: 'border-red-200'
        };
      case 'blue':
        return {
          bg: 'bg-blue-50',
          text: 'text-blue-700',
          icon: 'text-blue-600',
          border: 'border-blue-200'
        };
      case 'purple':
        return {
          bg: 'bg-purple-50',
          text: 'text-purple-700',
          icon: 'text-purple-600',
          border: 'border-purple-200'
        };
      default:
        return {
          bg: 'bg-gray-50',
          text: 'text-gray-700',
          icon: 'text-gray-600',
          border: 'border-gray-200'
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
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Shield className="h-6 w-6 text-blue-600" />
          <h2 className="text-xl font-semibold">Compliance Dashboard</h2>
        </div>
        <Badge variant="secondary" className="gap-1">
          <Zap className="h-3 w-3" />
          Live
        </Badge>
      </div>

      {/* Critical Issues Alert */}
      {criticalIssues.length > 0 && (
        <Alert>
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription>
            <div className="space-y-2">
              <div className="font-medium">Critical Issues Detected:</div>
              {criticalIssues.map((issue, index) => (
                <div key={index} className="text-sm">
                  • <strong>{issue.title}:</strong> {issue.description}
                  {issue.sources.length > 0 && (
                    <div className="ml-4 text-muted-foreground">
                      Affected: {issue.sources.join(', ')}
                      {issue.sources.length < sources.length && ' ...'}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </AlertDescription>
        </Alert>
      )}

      {/* Widgets Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {widgets.map((widget) => {
          const colors = getWidgetColorClasses(widget.color);

          return (
            <Card key={widget.id} className={`${colors.bg} ${colors.border}`}>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground flex items-center gap-2">
                  <span className={colors.icon}>{widget.icon}</span>
                  {widget.title}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <div className={`text-2xl font-bold ${colors.text}`}>
                    {widget.value}
                  </div>
                  {widget.description && (
                    <div className="text-xs text-muted-foreground">
                      {widget.description}
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Compliance Summary */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base flex items-center gap-2">
            <TrendingUp className="h-4 w-4" />
            Compliance Summary
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <div className="text-sm font-medium">Status Distribution</div>
                <div className="space-y-1">
                  <div className="flex justify-between text-sm">
                    <span className="text-green-600">✓ Compliant</span>
                    <span>{sources.filter(s => s.validation_status === 'validated').length}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-yellow-600">⏳ Pending</span>
                    <span>{sources.filter(s => s.validation_status === 'pending').length}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-red-600">✗ Failed</span>
                    <span>{sources.filter(s => s.validation_status === 'failed').length}</span>
                  </div>
                </div>
              </div>

              <div className="space-y-2">
                <div className="text-sm font-medium">Feature Coverage</div>
                <div className="space-y-1">
                  <div className="flex justify-between text-sm">
                    <span>Robots.txt</span>
                    <span>{Math.round((sources.filter(s => s.robots_txt_url).length / sources.length) * 100)}%</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span>Terms of Service</span>
                    <span>{Math.round((sources.filter(s => s.terms_of_service_url).length / sources.length) * 100)}%</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span>Legal Contact</span>
                    <span>{Math.round((sources.filter(s => s.legal_contact_email).length / sources.length) * 100)}%</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span>Fair Use</span>
                    <span>{Math.round((sources.filter(s => s.fair_use_basis).length / sources.length) * 100)}%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default ComplianceDashboard;
