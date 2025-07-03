import React from 'react';

interface LegacyKPICardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon?: string;
  className?: string;
}

const LegacyKPICard: React.FC<LegacyKPICardProps> = ({
  title,
  value,
  subtitle,
  icon,
  className = ''
}) => {
  return (
    <div className={`legacy-info-card ${className}`}>
      {icon && (
        <div className="legacy-kpi-icon">
          <i className={`fas ${icon}`}></i>
        </div>
      )}

      <h3>{title}</h3>

      <div className="legacy-kpi-value">
        <strong>{value}</strong>
      </div>

      {subtitle && (
        <p className="legacy-kpi-subtitle">{subtitle}</p>
      )}
    </div>
  );
};

export default LegacyKPICard;
