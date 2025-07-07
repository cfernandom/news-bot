// Sources Administration API Client
// Extends the existing API client for news sources management with compliance

import axios, { AxiosInstance } from 'axios';

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

export interface ComplianceValidationResult {
  source_id: number;
  is_compliant: boolean;
  validation_results: {
    robots_txt_live_check: boolean;
    robots_txt_provided: boolean;
    terms_of_service_provided: boolean;
    legal_contact_provided: boolean;
    fair_use_documented: boolean;
    crawl_delay_compliant: boolean;
    compliance_score: number;
    violations_count: number;
    recommendations_count: number;
  };
  risk_level: string;
  compliance_score: number;
  violations: string[];
  recommendations: string[];
  validated_at: string;
}

export interface SourceCreateRequest {
  name: string;
  base_url: string;
  language: string;
  country: string;
  extractor_class?: string;
  robots_txt_url?: string;
  terms_of_service_url?: string;
  legal_contact_email?: string;
  crawl_delay_seconds: number;
  fair_use_basis?: string;
}

export interface SourceUpdateRequest {
  name?: string;
  base_url?: string;
  language?: string;
  country?: string;
  extractor_class?: string;
  is_active?: boolean;
  robots_txt_url?: string;
  terms_of_service_url?: string;
  legal_contact_email?: string;
  crawl_delay_seconds?: number;
  fair_use_basis?: string;
}

export interface AuditTrailEntry {
  id: number;
  table_name: string;
  record_id: number;
  action: string;
  old_values?: any;
  new_values?: any;
  legal_basis: string;
  performed_by: string;
  performed_at: string;
  compliance_score_before?: number;
  compliance_score_after?: number;
  risk_level?: string;
  violations_count: number;
  created_at: string;
}

export interface AuditTrailResponse {
  audit_entries: AuditTrailEntry[];
  total_entries: number;
  limit: number;
  offset: number;
  filters_applied: {
    action?: string;
    source_id?: number;
  };
  compliance_framework: string;
}

export interface ComplianceStats {
  total_sources: number;
  validation_status_breakdown: {
    validated: number;
    pending: number;
    failed: number;
  };
  compliance_fields_coverage: {
    robots_txt_provided: number;
    terms_of_service_provided: number;
    legal_contact_provided: number;
    fair_use_documented: number;
  };
  compliance_percentage: {
    robots_txt: number;
    terms_of_service: number;
    legal_contact: number;
    overall_compliance: number;
  };
  generated_at: string;
}

export class SourcesApiClient {
  private baseURL: string;
  private client: AxiosInstance;

  // Getter for accessing the axios client
  get axiosClient(): AxiosInstance {
    return this.client;
  }

  constructor(baseURL: string = import.meta.env.VITE_API_URL || 'http://localhost:8000') {
    this.baseURL = baseURL;
    this.client = axios.create({
      baseURL: this.baseURL,
      timeout: 15000, // 15s timeout for compliance checks
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    });

    // Request interceptor for compliance context
    this.client.interceptors.request.use(
      (config) => {
        config.headers['X-Compliance-Context'] = 'sources-administration';
        config.headers['X-Institution'] = 'UCOMPENSAR';
        config.headers['X-Legal-Framework'] = 'Colombian-Law-1581-2012';
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        console.error('Sources API Error:', error);
        return Promise.reject(error);
      }
    );
  }

  // Get all news sources with optional filtering
  async getSources(filters: {
    skip?: number;
    limit?: number;
    is_active?: boolean;
    language?: string;
    country?: string;
  } = {}): Promise<NewsSource[]> {
    const response = await this.client.get('/api/v1/sources/', { params: filters });
    return response.data;
  }

  // Get specific news source by ID
  async getSource(sourceId: number): Promise<NewsSource> {
    const response = await this.client.get(`/api/v1/sources/${sourceId}`);
    return response.data;
  }

  // Create new news source with compliance validation
  async createSource(sourceData: SourceCreateRequest): Promise<NewsSource> {
    const response = await this.client.post('/api/v1/sources/', sourceData);
    return response.data;
  }

  // Update existing news source
  async updateSource(sourceId: number, sourceData: SourceUpdateRequest): Promise<NewsSource> {
    const response = await this.client.put(`/api/v1/sources/${sourceId}`, sourceData);
    return response.data;
  }

  // Delete (deactivate) news source
  async deleteSource(sourceId: number): Promise<{ message: string }> {
    const response = await this.client.delete(`/api/v1/sources/${sourceId}`);
    return response.data;
  }

  // Validate source compliance
  async validateSourceCompliance(sourceId: number): Promise<ComplianceValidationResult> {
    const response = await this.client.post(`/api/v1/sources/${sourceId}/validate`);
    return response.data;
  }

  // Get compliance dashboard data
  async getComplianceDashboard(): Promise<ComplianceDashboard> {
    const response = await this.client.get('/api/v1/sources/compliance/dashboard');
    return response.data;
  }

  // Get detailed compliance statistics
  async getComplianceStats(): Promise<ComplianceStats> {
    const response = await this.client.get('/api/v1/sources/compliance/stats');
    return response.data;
  }

  // Get non-compliant sources
  async getNonCompliantSources(): Promise<NewsSource[]> {
    const response = await this.client.get('/api/v1/sources/non-compliant');
    return response.data;
  }

  // Bulk compliance check for multiple sources
  async bulkComplianceCheck(sourceIds: number[]): Promise<{
    total_sources: number;
    successful_validations: number;
    failed_validations: number;
    results: Array<{
      source_id: number;
      error?: string;
      validation_result?: ComplianceValidationResult;
    }>;
  }> {
    const response = await this.client.post('/api/v1/sources/bulk-compliance-check', sourceIds);
    return response.data;
  }

  // Legal review for news source
  async legalReviewSource(sourceId: number, reviewData: {
    reviewer_email: string;
    review_status: 'approved' | 'rejected' | 'needs_review';
    review_notes: string;
  }): Promise<{
    source_id: number;
    review_status: string;
    reviewed_at: string;
    reviewer: string;
    message: string;
  }> {
    const response = await this.client.post(`/api/v1/sources/${sourceId}/legal-review`, reviewData);
    return response.data;
  }

  // Get audit trail with filtering
  async getAuditTrail(filters: {
    limit?: number;
    offset?: number;
    action?: string;
    source_id?: number;
  } = {}): Promise<AuditTrailResponse> {
    const response = await this.client.get('/api/v1/sources/audit-trail', { params: filters });
    return response.data;
  }

  // Health check for sources API
  async checkHealth(): Promise<{ status: string; message?: string }> {
    try {
      const response = await this.client.get('/health');
      return { status: 'healthy', message: 'Sources API is operational' };
    } catch (error) {
      return { status: 'unhealthy', message: 'Sources API is not responding' };
    }
  }
}

// Singleton instance for sources API client
export const sourcesApiClient = new SourcesApiClient();

// Export default instance
export default sourcesApiClient;
