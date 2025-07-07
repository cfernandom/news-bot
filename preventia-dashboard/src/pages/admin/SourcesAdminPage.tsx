import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { Plus, Shield, AlertTriangle, CheckCircle } from 'lucide-react';
import { ComplianceStatusHeader } from '@/components/admin/ComplianceStatusHeader';
import { SourcesTable } from '@/components/admin/SourcesTable';
import { SourceConfigModal } from '@/components/admin/SourceConfigModal';
import { ComplianceMonitor } from '@/components/admin/ComplianceMonitor';
import { ComplianceDashboard } from '@/components/admin/ComplianceDashboard';
import { api } from '@/services/api';

export interface NewsSource {
  id: number;
  name: string;
  base_url: string;
  language: string;
  country: string;
  extractor_class?: string;
  is_active: boolean;
  validation_status: string;
  validation_error?: string;
  last_validation_at?: string;
  robots_txt_url?: string;
  robots_txt_last_checked?: string;
  crawl_delay_seconds: number;
  scraping_allowed?: boolean;
  terms_of_service_url?: string;
  terms_reviewed_at?: string;
  legal_contact_email?: string;
  fair_use_basis?: string;
  compliance_score?: number;
  last_compliance_check?: string;
  created_at: string;
  updated_at: string;
}

export interface ComplianceDashboard {
  total_sources: number;
  compliant_sources: number;
  pending_review: number;
  failed_validation: number;
  compliance_rate: number;
  sources_needing_attention: number;
  dashboard_updated_at: string;
}

export const SourcesAdminPage: React.FC = () => {
  const [sources, setSources] = useState<NewsSource[]>([]);
  const [complianceDashboard, setComplianceDashboard] = useState<ComplianceDashboard | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [selectedSource, setSelectedSource] = useState<NewsSource | null>(null);
  const [activeTab, setActiveTab] = useState<'overview' | 'monitor' | 'dashboard'>('overview');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    setError(null);

    try {
      // Load sources and compliance dashboard in parallel
      const [sourcesResponse, dashboardResponse] = await Promise.all([
        api.get('/api/v1/sources/'),
        api.get('/api/v1/sources/compliance/dashboard')
      ]);

      setSources(sourcesResponse.data);
      setComplianceDashboard(dashboardResponse.data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load data');
      console.error('Error loading sources data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleValidateSource = async (sourceId: number) => {
    try {
      await api.post(`/api/v1/sources/${sourceId}/validate`);
      // Reload data to reflect changes
      await loadData();
    } catch (err) {
      setError('Failed to validate source compliance');
      console.error('Error validating source:', err);
    }
  };

  const handleCreateSource = async (sourceData: any) => {
    try {
      await api.post('/api/v1/sources/', sourceData);
      setShowCreateModal(false);
      await loadData();
    } catch (err) {
      throw err; // Let the modal handle the error
    }
  };

  const handleEditSource = (source: NewsSource) => {
    setSelectedSource(source);
    setShowCreateModal(true);
  };

  const getComplianceStatusColor = (status: string) => {
    switch (status) {
      case 'validated': return 'bg-green-100 text-green-800';
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      case 'failed': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getComplianceIcon = (score?: number) => {
    if (!score) return <AlertTriangle className="h-4 w-4 text-gray-500" />;
    if (score >= 0.8) return <CheckCircle className="h-4 w-4 text-green-600" />;
    if (score >= 0.6) return <Shield className="h-4 w-4 text-yellow-600" />;
    return <AlertTriangle className="h-4 w-4 text-red-600" />;
  };

  if (loading) {
    return (
      <div className="container mx-auto p-6">
        <div className="flex items-center justify-center h-64">
          <div className="text-lg">Loading news sources...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="admin-space-y-12">
      {/* Page Header */}
      <div className="admin-card">
        <div className="admin-card-header">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="admin-card-title">News Sources Administration</h1>
              <p className="admin-card-subtitle">
                Manage news sources with compliance-first approach and real-time monitoring
              </p>
            </div>
            <button onClick={() => setShowCreateModal(true)} className="admin-btn admin-btn-primary">
              <Plus className="h-5 w-5" />
              Add New Source
            </button>
          </div>
        </div>
      </div>

      {/* Error Alert */}
      {error && (
        <Alert variant="destructive">
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Compliance Status Header */}
      {complianceDashboard && (
        <div className="mt-8 mb-8">
          <ComplianceStatusHeader dashboard={complianceDashboard} />
        </div>
      )}

      {/* Navigation Tabs */}
      <div className="admin-tabs">
        <nav className="admin-tabs-nav">
          <button
            onClick={() => setActiveTab('overview')}
            className={`admin-tab-button ${activeTab === 'overview' ? 'active' : ''}`}
          >
            📊 Overview
          </button>
          <button
            onClick={() => setActiveTab('monitor')}
            className={`admin-tab-button ${activeTab === 'monitor' ? 'active' : ''}`}
          >
            🔍 Monitor
          </button>
          <button
            onClick={() => setActiveTab('dashboard')}
            className={`admin-tab-button ${activeTab === 'dashboard' ? 'active' : ''}`}
          >
            📈 Dashboard
          </button>
        </nav>

        {/* Tab Content */}
        <div className="admin-tabs-content">
          {activeTab === 'overview' && (
            <div className="admin-space-y-8">
              <div className="admin-section-header">
                <div className="admin-section-title">
                  <Shield className="h-6 w-6" style={{ color: 'var(--admin-primary)' }} />
                  <span>News Sources ({sources.length})</span>
                </div>
                <div className="admin-section-badge">
                  Total sources managed with compliance tracking
                </div>
              </div>
              <SourcesTable
                sources={sources}
                onValidate={handleValidateSource}
                onEdit={handleEditSource}
                showComplianceColumns={true}
                highlightNonCompliant={true}
              />
            </div>
          )}

          {activeTab === 'monitor' && (
            <div className="admin-space-y-8">
              <div className="admin-section-header">
                <div className="admin-section-title">
                  <div className="admin-status-indicator">
                    <div className="admin-status-dot pulse" style={{ backgroundColor: 'var(--admin-accent)' }}></div>
                    <span>Real-time Compliance Monitor</span>
                  </div>
                </div>
                <div className="admin-section-badge" style={{ backgroundColor: '#f0fdf4', color: 'var(--admin-accent)' }}>
                  Live monitoring active
                </div>
              </div>
              <ComplianceMonitor
                sources={sources}
                onRefresh={loadData}
                refreshInterval={30}
              />
            </div>
          )}

          {activeTab === 'dashboard' && (
            <div className="admin-space-y-8">
              <div className="admin-section-header">
                <div className="admin-section-title">
                  <span>Compliance Analytics Dashboard</span>
                </div>
                <div className="admin-section-badge" style={{ backgroundColor: '#eff6ff', color: 'var(--admin-primary)' }}>
                  Comprehensive analytics
                </div>
              </div>
              <ComplianceDashboard sources={sources} />
            </div>
          )}

        </div>
      </div>

      {/* Sources Configuration Modal */}
      <SourceConfigModal
        isOpen={showCreateModal}
        onClose={() => {
          setShowCreateModal(false);
          setSelectedSource(null);
        }}
        onSubmit={handleCreateSource}
        source={selectedSource}
      />
    </div>
  );
};
