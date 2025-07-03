import React, { useState, useEffect } from 'react';
import { exportData, getExportSizeEstimate, ExportOptions } from '../../../utils/exportUtils';

interface LegacyExportModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const LegacyExportModal: React.FC<LegacyExportModalProps> = ({ isOpen, onClose }) => {
  const [isExporting, setIsExporting] = useState(false);
  const [exportProgress, setExportProgress] = useState('');
  const [articleCount, setArticleCount] = useState(0);
  const [selectedFormat, setSelectedFormat] = useState<'CSV' | 'XLSX' | 'PDF'>('CSV');

  useEffect(() => {
    if (isOpen) {
      // Get estimated article count
      getExportSizeEstimate().then(count => {
        setArticleCount(count);
      });
    }
  }, [isOpen]);

  const handleExport = async (format: 'CSV' | 'XLSX' | 'PDF') => {
    setIsExporting(true);
    setSelectedFormat(format);
    setExportProgress(`Preparando exportación ${format}...`);

    try {
      const options: ExportOptions = {
        format,
        filters: {} // Could be extended to include actual filters
      };

      setExportProgress(`Generando archivo ${format}...`);
      await exportData(options);

      setExportProgress(`¡Archivo ${format} descargado exitosamente!`);

      // Close modal after short delay
      setTimeout(() => {
        onClose();
        setIsExporting(false);
        setExportProgress('');
      }, 2000);

    } catch (error) {
      setExportProgress(`Error: ${error instanceof Error ? error.message : 'Error desconocido'}`);
      setIsExporting(false);
    }
  };

  const handleClose = () => {
    if (!isExporting) {
      onClose();
      setExportProgress('');
    }
  };

  if (!isOpen) return null;

  return (
    <div className="legacy-modal-overlay" onClick={handleClose}>
      <div className="legacy-modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="legacy-modal-header">
          <h3>Exportar Datos Analíticos</h3>
          {!isExporting && (
            <button
              className="legacy-modal-close"
              onClick={handleClose}
            >
              ×
            </button>
          )}
        </div>

        <div className="legacy-modal-body">
          {!isExporting ? (
            <>
              <p style={{ marginBottom: '20px', color: 'var(--text-secondary)' }}>
                Selecciona el formato de exportación para descargar los datos analíticos:
              </p>

              <div className="legacy-export-info">
                <div className="export-info-item">
                  <i className="fas fa-database" style={{ color: 'var(--primary-blue)' }}></i>
                  <span><strong>{articleCount}</strong> artículos disponibles</span>
                </div>
                <div className="export-info-item">
                  <i className="fas fa-calendar" style={{ color: 'var(--primary-blue)' }}></i>
                  <span>Datos actualizados hoy</span>
                </div>
              </div>

              <div className="legacy-export-options">
                <button
                  className="legacy-export-btn csv-btn"
                  onClick={() => handleExport('CSV')}
                >
                  <i className="fas fa-file-csv"></i>
                  <div className="btn-content">
                    <strong>Exportar como CSV</strong>
                    <small>Compatible con Excel, Google Sheets</small>
                  </div>
                </button>

                <button
                  className="legacy-export-btn xlsx-btn"
                  onClick={() => handleExport('XLSX')}
                >
                  <i className="fas fa-file-excel"></i>
                  <div className="btn-content">
                    <strong>Exportar como Excel</strong>
                    <small>Formato nativo de Microsoft Excel</small>
                  </div>
                </button>

                <button
                  className="legacy-export-btn pdf-btn"
                  onClick={() => handleExport('PDF')}
                >
                  <i className="fas fa-file-pdf"></i>
                  <div className="btn-content">
                    <strong>Exportar como PDF</strong>
                    <small>Informe completo con gráficos</small>
                  </div>
                </button>
              </div>
            </>
          ) : (
            <div className="legacy-export-progress">
              <div className="progress-content">
                <div className="progress-icon">
                  {exportProgress.includes('exitosamente') ? (
                    <i className="fas fa-check-circle" style={{ color: '#10b981', fontSize: '48px' }}></i>
                  ) : exportProgress.includes('Error') ? (
                    <i className="fas fa-exclamation-circle" style={{ color: '#ef4444', fontSize: '48px' }}></i>
                  ) : (
                    <i className="fas fa-spinner fa-spin" style={{ color: 'var(--primary-blue)', fontSize: '48px' }}></i>
                  )}
                </div>

                <h4 style={{ margin: '20px 0 10px', color: 'var(--text-primary)' }}>
                  {exportProgress.includes('exitosamente') ? 'Exportación Completada' :
                   exportProgress.includes('Error') ? 'Error en Exportación' :
                   `Exportando ${selectedFormat}`}
                </h4>

                <p style={{ color: 'var(--text-secondary)', marginBottom: '20px' }}>
                  {exportProgress}
                </p>

                {exportProgress.includes('Error') && (
                  <button
                    className="legacy-btn legacy-btn-secondary"
                    onClick={handleClose}
                  >
                    Cerrar
                  </button>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default LegacyExportModal;
