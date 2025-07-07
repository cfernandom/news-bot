import React from 'react';
import { Badge } from '@/components/ui/badge';
import {
  CheckCircle,
  AlertTriangle,
  Clock,
  Shield,
  Globe,
  Mail,
  AlertCircle
} from 'lucide-react';
import { NewsSource } from '@/pages/admin/SourcesAdminPage';

interface ComplianceStatusIndicatorProps {
  source: NewsSource;
  showDetails?: boolean;
  size?: 'sm' | 'md' | 'lg';
}

export const ComplianceStatusIndicator: React.FC<ComplianceStatusIndicatorProps> = ({
  source,
  showDetails = false,
  size = 'md'
}) => {
  const getComplianceColor = (status: string) => {
    switch (status) {
      case 'validated': return 'text-green-600';
      case 'pending': return 'text-yellow-600';
      case 'failed': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  const getComplianceIcon = (score?: number) => {
    const iconSize = size === 'sm' ? 'h-3 w-3' : size === 'lg' ? 'h-6 w-6' : 'h-4 w-4';

    if (!score) return <AlertCircle className={`${iconSize} text-gray-500`} />;
    if (score >= 0.8) return <CheckCircle className={`${iconSize} text-green-600`} />;
    if (score >= 0.6) return <Shield className={`${iconSize} text-yellow-600`} />;
    return <AlertTriangle className={`${iconSize} text-red-600`} />;
  };

  const getValidationStatusBadge = (status: string) => {
    const badgeSize = size === 'sm' ? 'text-xs px-2 py-1' : 'text-sm px-3 py-1';

    switch (status) {
      case 'validated':
        return <Badge variant="default" className={`gap-1 ${badgeSize}`}>
          <CheckCircle className="h-3 w-3" />
          Conforme
        </Badge>;
      case 'pending':
        return <Badge variant="secondary" className={`gap-1 ${badgeSize}`}>
          <Clock className="h-3 w-3" />
          Pendiente
        </Badge>;
      case 'failed':
        return <Badge variant="destructive" className={`gap-1 ${badgeSize}`}>
          <AlertTriangle className="h-3 w-3" />
          No Conforme
        </Badge>;
      default:
        return <Badge variant="outline" className={badgeSize}>{status}</Badge>;
    }
  };

  const getComplianceFeatures = () => {
    const features = [];
    const iconSize = size === 'sm' ? 'h-3 w-3' : 'h-4 w-4';
    const textSize = size === 'sm' ? 'text-xs' : 'text-sm';

    if (source.robots_txt_url) {
      features.push(
        <div key="robots" className={`flex items-center gap-1 ${textSize} text-green-600`}>
          <Shield className={iconSize} />
          {size !== 'sm' && 'Robots.txt'}
        </div>
      );
    }

    if (source.terms_of_service_url) {
      features.push(
        <div key="tos" className={`flex items-center gap-1 ${textSize} text-blue-600`}>
          <Globe className={iconSize} />
          {size !== 'sm' && 'Términos de Servicio'}
        </div>
      );
    }

    if (source.legal_contact_email) {
      features.push(
        <div key="contact" className={`flex items-center gap-1 ${textSize} text-purple-600`}>
          <Mail className={iconSize} />
          {size !== 'sm' && 'Contacto'}
        </div>
      );
    }

    if (source.fair_use_basis) {
      features.push(
        <div key="fair-use" className={`flex items-center gap-1 ${textSize} text-indigo-600`}>
          <CheckCircle className={iconSize} />
          {size !== 'sm' && 'Uso Justo'}
        </div>
      );
    }

    return features;
  };

  const formatComplianceScore = (score?: number) => {
    if (!score) return 'N/A';
    return `${Math.round(score * 100)}%`;
  };

  if (size === 'sm') {
    return (
      <div className="flex items-center gap-2">
        {getComplianceIcon(source.compliance_score)}
        <span className={`text-xs font-medium ${getComplianceColor(source.validation_status)}`}>
          {formatComplianceScore(source.compliance_score)}
        </span>
      </div>
    );
  }

  return (
    <div className="compliance-status-indicator space-y-2">
      {/* Main Status */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          {getComplianceIcon(source.compliance_score)}
          <span className={`font-medium ${getComplianceColor(source.validation_status)}`}>
            {source.validation_status === 'validated' ? 'Conforme' :
             source.validation_status === 'pending' ? 'Pendiente de Revisión' :
             source.validation_status === 'failed' ? 'No Conforme' : 'Desconocido'}
          </span>
        </div>
        {getValidationStatusBadge(source.validation_status)}
      </div>

      {/* Compliance Score */}
      <div className="flex items-center justify-between">
        <span className="text-sm text-muted-foreground">Puntuación de Cumplimiento:</span>
        <span className={`font-semibold ${getComplianceColor(source.validation_status)}`}>
          {formatComplianceScore(source.compliance_score)}
        </span>
      </div>

      {/* Compliance Features */}
      {showDetails && (
        <div className="space-y-2">
          <span className="text-sm font-medium text-muted-foreground">Características:</span>
          <div className="flex flex-wrap gap-2">
            {getComplianceFeatures()}
          </div>

          {/* Validation Error */}
          {source.validation_error && (
            <div className="mt-2 p-2 bg-red-50 border border-red-200 rounded text-xs text-red-700">
              <strong>Problemas:</strong> {source.validation_error}
            </div>
          )}

          {/* Last Validated */}
          {source.last_validation_at && (
            <div className="text-xs text-muted-foreground">
              Última validación: {new Date(source.last_validation_at).toLocaleDateString()}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

// Tooltip component for hover details
interface ComplianceTooltipProps {
  source: NewsSource;
  children: React.ReactNode;
}

export const ComplianceTooltip: React.FC<ComplianceTooltipProps> = ({
  source,
  children
}) => {
  const [showTooltip, setShowTooltip] = React.useState(false);

  return (
    <div
      className="relative inline-block"
      onMouseEnter={() => setShowTooltip(true)}
      onMouseLeave={() => setShowTooltip(false)}
    >
      {children}

      {showTooltip && (
        <div className="absolute z-10 bottom-full left-1/2 transform -translate-x-1/2 mb-2 p-3 bg-white border rounded-lg shadow-lg min-w-[200px]">
          <ComplianceStatusIndicator
            source={source}
            showDetails={true}
            size="sm"
          />

          {/* Arrow */}
          <div className="absolute top-full left-1/2 transform -translate-x-1/2 border-4 border-transparent border-t-white"></div>
        </div>
      )}
    </div>
  );
};

export default ComplianceStatusIndicator;
