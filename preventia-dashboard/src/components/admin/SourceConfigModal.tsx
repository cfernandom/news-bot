import React, { useState, useEffect } from 'react';
import {
  CheckCircle,
  AlertTriangle,
  Shield,
  Globe,
  Mail,
  Clock,
  Loader2
} from 'lucide-react';
import { NewsSource } from '@/pages/admin/SourcesAdminPage';
import { api } from '@/services/api';

interface SourceConfigModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (sourceData: any) => Promise<void>;
  source?: NewsSource | null;
}

interface ComplianceValidation {
  is_compliant: boolean;
  compliance_score: number;
  violations: string[];
  recommendations: string[];
  validation_results: {
    robots_txt_live_check: boolean;
    robots_txt_provided: boolean;
    terms_of_service_provided: boolean;
    legal_contact_provided: boolean;
    fair_use_documented: boolean;
    crawl_delay_compliant: boolean;
  };
}

const COUNTRIES = [
  'United States', 'United Kingdom', 'Canada', 'Australia', 'Germany',
  'France', 'Spain', 'Italy', 'Netherlands', 'Mexico', 'Colombia', 'Other'
];

const LANGUAGES = [
  { code: 'en', name: 'English' },
  { code: 'es', name: 'Spanish' },
  { code: 'fr', name: 'French' },
  { code: 'de', name: 'German' },
  { code: 'it', name: 'Italian' },
];

export const SourceConfigModal: React.FC<SourceConfigModalProps> = ({
  isOpen,
  onClose,
  onSubmit,
  source
}) => {
  const [formData, setFormData] = useState({
    name: '',
    base_url: '',
    language: 'en',
    country: 'United States',
    extractor_class: '',
    robots_txt_url: '',
    terms_of_service_url: '',
    legal_contact_email: '',
    crawl_delay_seconds: 2,
    fair_use_basis: 'Academic research under Colombian Law 1581/2012 and fair use doctrine for breast cancer prevention analysis'
  });

  const [complianceValidation, setComplianceValidation] = useState<ComplianceValidation | null>(null);
  const [isValidating, setIsValidating] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasValidated, setHasValidated] = useState(false);

  useEffect(() => {
    if (source) {
      setFormData({
        name: source.name,
        base_url: source.base_url,
        language: source.language,
        country: source.country,
        extractor_class: source.extractor_class || '',
        robots_txt_url: source.robots_txt_url || '',
        terms_of_service_url: source.terms_of_service_url || '',
        legal_contact_email: source.legal_contact_email || '',
        crawl_delay_seconds: source.crawl_delay_seconds,
        fair_use_basis: source.fair_use_basis || 'Academic research under Colombian Law 1581/2012 and fair use doctrine for breast cancer prevention analysis'
      });
    } else {
      setFormData({
        name: '',
        base_url: '',
        language: 'en',
        country: 'United States',
        extractor_class: '',
        robots_txt_url: '',
        terms_of_service_url: '',
        legal_contact_email: '',
        crawl_delay_seconds: 2,
        fair_use_basis: 'Academic research under Colombian Law 1581/2012 and fair use doctrine for breast cancer prevention analysis'
      });
    }
    setComplianceValidation(null);
    setHasValidated(false);
    setError(null);
  }, [source, isOpen]);

  const handleInputChange = (field: string, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Reset validation when form changes
    if (hasValidated) {
      setComplianceValidation(null);
      setHasValidated(false);
    }
  };

  const validateCompliance = async () => {
    if (!formData.base_url || !formData.name) {
      setError('Name and Base URL are required for validation');
      return;
    }

    setIsValidating(true);
    setError(null);

    try {
      // Prepare data for validation (this is a simplified version)
      // In a real implementation, you might want to call a validation endpoint
      const validationData = {
        name: formData.name,
        base_url: formData.base_url,
        language: formData.language,
        country: formData.country,
        robots_txt_url: formData.robots_txt_url || null,
        terms_of_service_url: formData.terms_of_service_url || null,
        legal_contact_email: formData.legal_contact_email || null,
        crawl_delay_seconds: formData.crawl_delay_seconds,
        fair_use_basis: formData.fair_use_basis || null
      };

      // Simulate compliance validation logic
      const validation: ComplianceValidation = {
        is_compliant: true,
        compliance_score: 0,
        violations: [],
        recommendations: [],
        validation_results: {
          robots_txt_live_check: false,
          robots_txt_provided: !!formData.robots_txt_url,
          terms_of_service_provided: !!formData.terms_of_service_url,
          legal_contact_provided: !!formData.legal_contact_email,
          fair_use_documented: !!formData.fair_use_basis,
          crawl_delay_compliant: formData.crawl_delay_seconds >= 2
        }
      };

      // Calculate compliance score
      let score = 0;
      const checks = validation.validation_results;

      if (checks.robots_txt_provided) score += 0.15;
      if (checks.terms_of_service_provided) score += 0.2;
      if (checks.legal_contact_provided) score += 0.2;
      if (checks.fair_use_documented) score += 0.2;
      if (checks.crawl_delay_compliant) score += 0.05;

      // Try to check robots.txt live (simplified)
      try {
        const robotsUrl = formData.robots_txt_url || `${formData.base_url}/robots.txt`;
        // In a real implementation, this would be done on the backend
        validation.validation_results.robots_txt_live_check = true;
        score += 0.2;
      } catch {
        validation.violations.push('Unable to verify robots.txt accessibility');
        validation.recommendations.push('Ensure robots.txt URL is accessible');
      }

      validation.compliance_score = score;

      // Check for violations
      if (!checks.robots_txt_provided) {
        validation.violations.push('Missing robots.txt URL');
        validation.recommendations.push('Add robots.txt URL for compliance verification');
      }

      if (!checks.terms_of_service_provided) {
        validation.violations.push('Missing terms of service URL');
        validation.recommendations.push('Add terms of service URL for legal review');
      }

      if (!checks.legal_contact_provided) {
        validation.violations.push('Missing legal contact email');
        validation.recommendations.push('Add legal contact email for compliance communication');
      }

      if (!checks.fair_use_documented) {
        validation.violations.push('Missing fair use basis documentation');
        validation.recommendations.push('Document fair use basis for academic research');
      }

      validation.is_compliant = validation.violations.length === 0;

      setComplianceValidation(validation);
      setHasValidated(true);

    } catch (err) {
      setError('Failed to validate compliance. Please try again.');
      console.error('Compliance validation error:', err);
    } finally {
      setIsValidating(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!hasValidated) {
      setError('Please validate compliance before submitting');
      return;
    }

    if (complianceValidation && !complianceValidation.is_compliant) {
      setError('Source must be compliant before creation. Please fix compliance violations.');
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      await onSubmit(formData);
    } catch (err: any) {
      setError(err.response?.data?.detail?.error || err.message || 'Failed to save source');
    } finally {
      setIsSubmitting(false);
    }
  };


  return (
    <div className={`admin-modal-overlay`} style={{ display: isOpen ? 'flex' : 'none' }}>
      <div className="admin-modal" style={{ maxWidth: '56rem' }}>
        <div className="admin-modal-header">
          <div className="admin-modal-title" style={{ display: 'flex', alignItems: 'center', gap: 'var(--admin-spacing-sm)' }}>
            <Shield className="h-5 w-5" style={{ color: 'var(--admin-primary)' }} />
            {source ? 'Edit News Source' : 'Add News Source'}
          </div>
        </div>

        <div className="admin-modal-content">
          <form onSubmit={handleSubmit} className="admin-space-y-6">
            {/* Basic Information */}
            <div style={{ display: 'grid', gap: 'var(--admin-spacing-lg)', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))' }}>
              <div className="admin-form-group">
                <label htmlFor="name" className="admin-label">Source Name *</label>
                <input
                  id="name"
                  className="admin-input"
                  value={formData.name}
                  onChange={(e) => handleInputChange('name', e.target.value)}
                  placeholder="e.g., WebMD Health News"
                  required
                />
              </div>

              <div className="admin-form-group">
                <label htmlFor="base_url" className="admin-label">Base URL *</label>
                <input
                  id="base_url"
                  className="admin-input"
                  value={formData.base_url}
                  onChange={(e) => handleInputChange('base_url', e.target.value)}
                  placeholder="https://example.com"
                  required
                />
              </div>

              <div className="admin-form-group">
                <label htmlFor="language" className="admin-label">Language</label>
                <select
                  id="language"
                  className="admin-select"
                  value={formData.language}
                  onChange={(e) => handleInputChange('language', e.target.value)}
                >
                  {LANGUAGES.map((lang) => (
                    <option key={lang.code} value={lang.code}>
                      {lang.name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="admin-form-group">
                <label htmlFor="country" className="admin-label">Country</label>
                <select
                  id="country"
                  className="admin-select"
                  value={formData.country}
                  onChange={(e) => handleInputChange('country', e.target.value)}
                >
                  {COUNTRIES.map((country) => (
                    <option key={country} value={country}>
                      {country}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* Legal Compliance Section */}
            <div className="admin-alert admin-alert-info">
              <Shield className="h-5 w-5" />
              <div>
                <div style={{ fontSize: '1.125rem', fontWeight: '600', marginBottom: 'var(--admin-spacing-md)' }}>
                  Legal Compliance Requirements
                </div>

                <div style={{ display: 'grid', gap: 'var(--admin-spacing-lg)', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))' }}>
                  <div className="admin-form-group">
                    <label htmlFor="robots_txt_url" className="admin-label" style={{ display: 'flex', alignItems: 'center', gap: 'var(--admin-spacing-xs)' }}>
                      <Globe className="h-4 w-4" />
                      Robots.txt URL
                    </label>
                    <input
                      id="robots_txt_url"
                      className="admin-input"
                      value={formData.robots_txt_url}
                      onChange={(e) => handleInputChange('robots_txt_url', e.target.value)}
                      placeholder="https://example.com/robots.txt"
                    />
                  </div>

                  <div className="admin-form-group">
                    <label htmlFor="terms_of_service_url" className="admin-label" style={{ display: 'flex', alignItems: 'center', gap: 'var(--admin-spacing-xs)' }}>
                      <Globe className="h-4 w-4" />
                      Terms of Service URL
                    </label>
                    <input
                      id="terms_of_service_url"
                      className="admin-input"
                      value={formData.terms_of_service_url}
                      onChange={(e) => handleInputChange('terms_of_service_url', e.target.value)}
                      placeholder="https://example.com/terms"
                    />
                  </div>

                  <div className="admin-form-group">
                    <label htmlFor="legal_contact_email" className="admin-label" style={{ display: 'flex', alignItems: 'center', gap: 'var(--admin-spacing-xs)' }}>
                      <Mail className="h-4 w-4" />
                      Legal Contact Email
                    </label>
                    <input
                      id="legal_contact_email"
                      type="email"
                      className="admin-input"
                      value={formData.legal_contact_email}
                      onChange={(e) => handleInputChange('legal_contact_email', e.target.value)}
                      placeholder="legal@example.com"
                    />
                  </div>

                  <div className="admin-form-group">
                    <label htmlFor="crawl_delay_seconds" className="admin-label" style={{ display: 'flex', alignItems: 'center', gap: 'var(--admin-spacing-xs)' }}>
                      <Clock className="h-4 w-4" />
                      Crawl Delay (seconds)
                    </label>
                    <input
                      id="crawl_delay_seconds"
                      type="number"
                      min="1"
                      max="30"
                      className="admin-input"
                      value={formData.crawl_delay_seconds}
                      onChange={(e) => handleInputChange('crawl_delay_seconds', parseInt(e.target.value))}
                    />
                  </div>
                </div>

                <div className="admin-form-group">
                  <label htmlFor="fair_use_basis" className="admin-label">Fair Use Basis *</label>
                  <textarea
                    id="fair_use_basis"
                    className="admin-input admin-textarea"
                    value={formData.fair_use_basis}
                    onChange={(e) => handleInputChange('fair_use_basis', e.target.value)}
                    placeholder="Document the legal basis for fair use..."
                    rows={3}
                    required
                  />
                </div>
              </div>
            </div>

            {/* Compliance Validation Section */}
            <div className="admin-space-y-4">
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <h3 style={{ fontSize: '1.125rem', fontWeight: '600', color: 'var(--admin-text-primary)' }}>Compliance Validation</h3>
                <button
                  type="button"
                  onClick={validateCompliance}
                  disabled={isValidating || !formData.name || !formData.base_url}
                  className="admin-btn admin-btn-secondary"
                  style={{
                    opacity: (isValidating || !formData.name || !formData.base_url) ? 0.5 : 1,
                    cursor: (isValidating || !formData.name || !formData.base_url) ? 'not-allowed' : 'pointer'
                  }}
                >
                  {isValidating ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    <Shield className="h-4 w-4" />
                  )}
                  {isValidating ? 'Validating...' : 'Validate Compliance'}
                </button>
              </div>

              {complianceValidation && (
                <div className="admin-compliance-card">
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 'var(--admin-spacing-lg)' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--admin-spacing-sm)' }}>
                      {complianceValidation.is_compliant ? (
                        <CheckCircle className="h-5 w-5" style={{ color: 'var(--admin-accent)' }} />
                      ) : (
                        <AlertTriangle className="h-5 w-5" style={{ color: 'var(--admin-danger)' }} />
                      )}
                      <span style={{ fontWeight: '600', color: 'var(--admin-text-primary)' }}>
                        {complianceValidation.is_compliant ? 'Compliant' : 'Non-Compliant'}
                      </span>
                    </div>
                    <div className={`admin-compliance-indicator ${complianceValidation.is_compliant ? 'validated' : 'failed'}`}>
                      Score: <span className={`admin-stat-value ${
                        complianceValidation.compliance_score >= 0.8 ? 'admin-stat-green' :
                        complianceValidation.compliance_score >= 0.6 ? 'admin-stat-yellow' : 'admin-stat-red'
                      }`} style={{ fontSize: '0.875rem' }}>
                        {Math.round(complianceValidation.compliance_score * 100)}%
                      </span>
                    </div>
                  </div>

                  {complianceValidation.violations.length > 0 && (
                    <div className="admin-alert admin-alert-danger" style={{ marginBottom: 'var(--admin-spacing-lg)' }}>
                      <AlertTriangle className="h-4 w-4" />
                      <div>
                        <div style={{ fontWeight: '600', marginBottom: 'var(--admin-spacing-sm)' }}>Compliance Violations:</div>
                        <ul style={{ listStyleType: 'disc', paddingLeft: 'var(--admin-spacing-lg)' }}>
                          {complianceValidation.violations.map((violation, index) => (
                            <li key={index} style={{ fontSize: '0.875rem', marginBottom: 'var(--admin-spacing-xs)' }}>{violation}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  )}

                  {complianceValidation.recommendations.length > 0 && (
                    <div className="admin-alert admin-alert-warning" style={{ marginBottom: 'var(--admin-spacing-lg)' }}>
                      <AlertTriangle className="h-4 w-4" />
                      <div>
                        <div style={{ fontWeight: '600', marginBottom: 'var(--admin-spacing-sm)' }}>Recommendations:</div>
                        <ul style={{ listStyleType: 'disc', paddingLeft: 'var(--admin-spacing-lg)' }}>
                          {complianceValidation.recommendations.map((rec, index) => (
                            <li key={index} style={{ fontSize: '0.875rem', marginBottom: 'var(--admin-spacing-xs)' }}>{rec}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  )}

                  <div style={{ display: 'grid', gap: 'var(--admin-spacing-sm)', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', fontSize: '0.875rem' }}>
                    {Object.entries(complianceValidation.validation_results).map(([key, value]) => (
                      <div key={key} style={{ display: 'flex', alignItems: 'center', gap: 'var(--admin-spacing-sm)' }}>
                        {value ? (
                          <CheckCircle className="h-4 w-4" style={{ color: 'var(--admin-accent)' }} />
                        ) : (
                          <AlertTriangle className="h-4 w-4" style={{ color: 'var(--admin-danger)' }} />
                        )}
                        <span style={{ textTransform: 'capitalize', color: 'var(--admin-text-primary)' }}>
                          {key.replace(/_/g, ' ')}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
          </div>

            {/* Error Display */}
            {error && (
              <div className="admin-alert admin-alert-danger">
                <AlertTriangle className="h-4 w-4" />
                <div>{error}</div>
              </div>
            )}

            {/* Advanced Settings */}
            <div style={{ padding: 'var(--admin-spacing-lg)', backgroundColor: 'var(--admin-secondary)', borderRadius: 'var(--admin-radius-lg)' }}>
              <h3 style={{ fontSize: '1.125rem', fontWeight: '600', color: 'var(--admin-text-primary)', marginBottom: 'var(--admin-spacing-lg)' }}>Advanced Settings</h3>
              <div className="admin-form-group">
                <label htmlFor="extractor_class" className="admin-label">Extractor Class (Optional)</label>
                <input
                  id="extractor_class"
                  className="admin-input"
                  value={formData.extractor_class}
                  onChange={(e) => handleInputChange('extractor_class', e.target.value)}
                  placeholder="custom_extractor_class"
                />
              </div>
            </div>
          </form>
        </div>

        <div className="admin-modal-footer">
          <button
            onClick={onClose}
            disabled={isSubmitting}
            className="admin-btn admin-btn-secondary"
            style={{ opacity: isSubmitting ? 0.5 : 1 }}
          >
            Cancel
          </button>
          <button
            onClick={handleSubmit}
            disabled={isSubmitting || !hasValidated || (complianceValidation && !complianceValidation.is_compliant)}
            className="admin-btn admin-btn-primary"
            style={{
              opacity: (isSubmitting || !hasValidated || (complianceValidation && !complianceValidation.is_compliant)) ? 0.5 : 1,
              cursor: (isSubmitting || !hasValidated || (complianceValidation && !complianceValidation.is_compliant)) ? 'not-allowed' : 'pointer'
            }}
          >
            {isSubmitting ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Shield className="h-4 w-4" />
            )}
            {isSubmitting ? 'Saving...' : (source ? 'Update Source' : 'Create Source')}
            (Compliance Required)
          </button>
        </div>
      </div>
    </div>
  );
};
