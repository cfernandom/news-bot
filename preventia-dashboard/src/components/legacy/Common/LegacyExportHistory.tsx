import React from 'react';

export interface ExportHistoryItem {
  id: string;
  filename: string;
  format: 'CSV' | 'XLSX' | 'PDF';
  timestamp: string;
  size: string;
  downloadUrl: string;
  status: 'completed' | 'failed' | 'pending';
}

interface LegacyExportHistoryProps {
  exports: ExportHistoryItem[];
  onDownload: (item: ExportHistoryItem) => void;
  onDelete: (id: string) => void;
  className?: string;
  title?: string; // Added title prop for consistency with tests
}

const LegacyExportHistory: React.FC<LegacyExportHistoryProps> = ({
  exports,
  onDownload,
  onDelete,
  className = '',
  title = 'Historial de Exportaciones'
}) => {

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

  // Sort exports by timestamp, newest first
  const sortedExports = [...exports].sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());

  return (
    <div className={`legacy-export-history ${className}`}>
      <div className="legacy-export-history-header">
        <h3>{title}</h3>
        {/* Removed update button as data is now passed via props */}
      </div>

      {sortedExports.length === 0 ? (
        <div className="legacy-empty-state">
          <i className="fas fa-download" style={{ fontSize: '48px', color: 'var(--text-secondary)' }}></i>
          <p>No hay exportaciones disponibles</p>
          <small>Las exportaciones aparecerán aquí después de generarlas</small>
        </div>
      ) : (
        <div className="legacy-export-history-list">
          {sortedExports.map((item) => (
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
                    onClick={() => onDownload(item)}
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
                  onClick={() => onDelete(item.id)}
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
