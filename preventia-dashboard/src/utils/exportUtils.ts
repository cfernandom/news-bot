import apiClient from '../api/client';

export interface ExportOptions {
  format: 'CSV' | 'XLSX' | 'PDF';
  filename?: string;
  filters?: {
    topic?: string;
    date_from?: string;
    date_to?: string;
    search?: string;
  };
}

export const downloadFile = (blob: Blob, filename: string) => {
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
};

export const exportData = async (options: ExportOptions): Promise<void> => {
  const { format, filename, filters = {} } = options;

  try {
    let endpoint = '';
    let defaultFilename = '';
    let contentType = '';

    switch (format) {
      case 'CSV':
        endpoint = '/api/v1/export/news.csv';
        defaultFilename = `preventia-articles-${new Date().toISOString().split('T')[0]}.csv`;
        contentType = 'text/csv';
        break;
      case 'XLSX':
        endpoint = '/api/v1/export/news.xlsx';
        defaultFilename = `preventia-articles-${new Date().toISOString().split('T')[0]}.xlsx`;
        contentType = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
        break;
      case 'PDF':
        endpoint = '/api/v1/export/report';
        defaultFilename = `preventia-report-${new Date().toISOString().split('T')[0]}.pdf`;
        contentType = 'application/pdf';
        break;
      default:
        throw new Error(`Unsupported format: ${format}`);
    }

    // Build query parameters
    const params = new URLSearchParams();
    if (filters.topic) params.append('topic', filters.topic);
    if (filters.date_from) params.append('date_from', filters.date_from);
    if (filters.date_to) params.append('date_to', filters.date_to);
    if (filters.search) params.append('search', filters.search);

    const url = params.toString() ? `${endpoint}?${params.toString()}` : endpoint;

    // For PDF, we might need to use POST
    let response;
    if (format === 'PDF') {
      response = await apiClient.post(endpoint, {
        filters,
        include_ai_summaries: true
      }, {
        responseType: 'blob'
      });
    } else {
      response = await apiClient.get(url, {
        responseType: 'blob'
      });
    }

    // Create blob with correct content type
    const blob = new Blob([response.data], { type: contentType });

    // Download the file
    const finalFilename = filename || defaultFilename;
    downloadFile(blob, finalFilename);

    return Promise.resolve();
  } catch (error) {
    console.error('Export failed:', error);
    throw new Error(`Error al exportar ${format}: ${error instanceof Error ? error.message : 'Error desconocido'}`);
  }
};

export const getExportSizeEstimate = async (filters: ExportOptions['filters'] = {}): Promise<number> => {
  try {
    // Get article count with current filters
    const params = new URLSearchParams({
      page: '1',
      page_size: '1',
      ...(filters.topic && { topic: filters.topic }),
      ...(filters.date_from && { date_from: filters.date_from }),
      ...(filters.date_to && { date_to: filters.date_to }),
      ...(filters.search && { search: filters.search })
    });

    const response = await apiClient.get(`/api/v1/news?${params.toString()}`);
    return response.data.meta?.total || 0;
  } catch (error) {
    console.error('Failed to get export size estimate:', error);
    return 0;
  }
};
