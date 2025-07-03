import React, { useState, useEffect } from 'react';

interface ExportHistoryItem {
  id: string;
  filename: string;
  format: 'CSV' | 'XLSX' | 'PDF';
  timestamp: string;
  size: string;
  downloadUrl: string;
  status: 'completed' | 'failed';
}

interface LegacyExportHistoryProps {
  className?: string;
}

const LegacyExportHistory: React.FC<LegacyExportHistoryProps> = ({ className = '' }) => {
  const [exportHistory, setExportHistory] = useState<ExportHistoryItem[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadExportHistory();
  }, []);

  const loadExportHistory = async () => {
    setLoading(true);
    try {
      // Simulate API call - in real implementation this would fetch from backend
      const mockHistory: ExportHistoryItem[] = [
        {
          id: '1',
          filename: 'preventia_analytics_2025-07-03.csv',
          format: 'CSV',
          timestamp: '2025-07-03T10:30:00Z',
          size: '2.4 MB',
          downloadUrl: '#',
          status: 'completed'
        },
        {
          id: '2',
          filename: 'preventia_report_2025-07-02.pdf',
          format: 'PDF',
          timestamp: '2025-07-02T15:45:00Z',
          size: '8.7 MB',
          downloadUrl: '#',
          status: 'completed'
        },
        {
          id: '3',
          filename: 'preventia_data_2025-07-01.xlsx',
          format: 'XLSX',
          timestamp: '2025-07-01T09:20:00Z',
          size: '3.1 MB',
          downloadUrl: '#',
          status: 'completed'
        },
        {
          id: '4',
          filename: 'preventia_backup_2025-06-30.csv',
          format: 'CSV',
          timestamp: '2025-06-30T14:10:00Z',
          size: '2.2 MB',
          downloadUrl: '#',
          status: 'failed'
        }
      ];

      setExportHistory(mockHistory);
    } catch (error) {
      console.error('Error loading export history:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    return new Intl.DateTimeFormat('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(date);
  };

  const getFormatIcon = (format: string) => {
    switch (format) {
      case 'CSV':
        return 'fas fa-file-csv';
      case 'XLSX':
        return 'fas fa-file-excel';
      case 'PDF':
        return 'fas fa-file-pdf';
      default:
        return 'fas fa-file';
    }
  };

  const getFormatColor = (format: string) => {
    switch (format) {
      case 'CSV':
        return '#10b981';
      case 'XLSX':
        return '#059669';
      case 'PDF':
        return '#ef4444';
      default:
        return '#6b7280';
    }
  };

  const handleDownload = (item: ExportHistoryItem) => {
    if (item.status === 'completed') {
      // In real implementation, this would trigger actual download
      console.log('Downloading:', item.filename);
      // For demo purposes, just show a message
      alert(`Descargando ${item.filename}...`);
    }
  };

  const handleDelete = (id: string) => {
    setExportHistory(prev => prev.filter(item => item.id !== id));
  };

  if (loading) {
    return (
      <div className={`legacy-export-history ${className}`}>
        <h3>Historial de Exportaciones</h3>
        <div className="legacy-loading-container">
          <i className="fas fa-spinner fa-spin" style={{ color: 'var(--primary-blue)' }}></i>
          <span>Cargando historial...</span>
        </div>
      </div>
    );
  }

  return (
    <div className={`legacy-export-history ${className}`}>
      <div className="legacy-export-history-header">
        <h3>Historial de Exportaciones</h3>
        <button
          className="legacy-btn-secondary"
          onClick={loadExportHistory}
          disabled={loading}
        >
          <i className="fas fa-sync-alt"></i>
          Actualizar
        </button>
      </div>

      {exportHistory.length === 0 ? (
        <div className="legacy-empty-state">
          <i className="fas fa-download" style={{ fontSize: '48px', color: 'var(--text-secondary)' }}></i>
          <p>No hay exportaciones disponibles</p>
          <small>Las exportaciones aparecerán aquí después de generarlas</small>
        </div>
      ) : (
        <div className="legacy-export-history-list">
          {exportHistory.map((item) => (
            <div key={item.id} className={`legacy-export-history-item ${item.status}`}>
              <div className="export-file-info">
                <div className="export-file-icon">
                  <i
                    className={getFormatIcon(item.format)}
                    style={{ color: getFormatColor(item.format) }}
                  ></i>
                </div>
                <div className="export-file-details">
                  <div className="export-filename">{item.filename}</div>
                  <div className="export-metadata">
                    <span className="export-timestamp">{formatTimestamp(item.timestamp)}</span>
                    <span className="export-size">{item.size}</span>
                    <span className={`export-status ${item.status}`}>
                      {item.status === 'completed' ? 'Completado' : 'Fallido'}
                    </span>
                  </div>
                </div>
              </div>

              <div className="export-actions">
                {item.status === 'completed' ? (
                  <button
                    className="legacy-btn-icon"
                    onClick={() => handleDownload(item)}
                    title="Descargar archivo"
                  >
                    <i className="fas fa-download"></i>
                  </button>
                ) : (
                  <button
                    className="legacy-btn-icon failed"
                    title="Exportación fallida"
                    disabled
                  >
                    <i className="fas fa-exclamation-triangle"></i>
                  </button>
                )}

                <button
                  className="legacy-btn-icon delete"
                  onClick={() => handleDelete(item.id)}
                  title="Eliminar del historial"
                >
                  <i className="fas fa-trash"></i>
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default LegacyExportHistory;
