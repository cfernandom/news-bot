import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import LegacyExportHistory, { ExportHistoryItem } from '../Common/LegacyExportHistory';

describe('LegacyExportHistory', () => {
  const mockExports: ExportHistoryItem[] = [
    {
      id: '1',
      format: 'PDF',
      timestamp: '2024-01-15T10:30:00Z',
      filename: 'analytics-report-2024-01-15.pdf',
      status: 'completed',
      size: '2.3 MB',
      downloadUrl: '#'
    },
    {
      id: '2',
      format: 'CSV',
      timestamp: '2024-01-14T15:45:00Z',
      filename: 'data-export-2024-01-14.csv',
      status: 'completed',
      size: '1.8 MB',
      downloadUrl: '#'
    },
    {
      id: '3',
      format: 'XLSX',
      timestamp: '2024-01-13T09:20:00Z',
      filename: 'full-report-2024-01-13.xlsx',
      status: 'failed',
      size: '3.1 MB',
      downloadUrl: '#'
    }
  ];

  const defaultProps = {
    exports: mockExports,
    onDownload: vi.fn(),
    onDelete: vi.fn(),
  };

  it('renders correctly with default props', () => {
    render(<LegacyExportHistory {...defaultProps} />);

    expect(screen.getByText('Historial de Exportaciones')).toBeInTheDocument();
    expect(screen.getByText('analytics-report-2024-01-15.pdf')).toBeInTheDocument();
  });

  it('renders with custom title', () => {
    render(<LegacyExportHistory {...defaultProps} title="Custom Export History" />);

    expect(screen.getByText('Custom Export History')).toBeInTheDocument();
  });

  it('displays correct table headers', () => {
    render(<LegacyExportHistory {...defaultProps} />);

    // The component no longer renders a table, so these assertions are updated
    expect(screen.getByText('Fecha y Hora')).toBeInTheDocument();
    expect(screen.getByText('Tipo')).toBeInTheDocument();
    expect(screen.getByText('Archivo')).toBeInTheDocument();
    expect(screen.getByText('Estado')).toBeInTheDocument();
    expect(screen.getByText('Tamaño')).toBeInTheDocument();
    expect(screen.getByText('Acciones')).toBeInTheDocument();
  });

  it('displays all export entries', () => {
    render(<LegacyExportHistory {...defaultProps} />);

    // Check that all 3 exports are displayed
    expect(screen.getByText('analytics-report-2024-01-15.pdf')).toBeInTheDocument();
    expect(screen.getByText('data-export-2024-01-14.csv')).toBeInTheDocument();
    expect(screen.getByText('full-report-2024-01-13.xlsx')).toBeInTheDocument();
  });

  it('formats timestamps correctly', () => {
    render(<LegacyExportHistory {...defaultProps} />);

    // Should format timestamps to readable format (Spanish locale)
    expect(screen.getByText('15 ene. 2024, 10:30')).toBeInTheDocument();
    expect(screen.getByText('14 ene. 2024, 15:45')).toBeInTheDocument();
    expect(screen.getByText('13 ene. 2024, 09:20')).toBeInTheDocument();
  });

  it('displays correct file types', () => {
    render(<LegacyExportHistory {...defaultProps} />);

    expect(screen.getByText('PDF')).toBeInTheDocument();
    expect(screen.getByText('CSV')).toBeInTheDocument();
    expect(screen.getByText('XLSX')).toBeInTheDocument();
  });

  it('shows correct status indicators', () => {
    render(<LegacyExportHistory {...defaultProps} />);

    // Should show status with appropriate styling (Spanish translations)
    const completedStatuses = screen.getAllByText('Completado');
    expect(completedStatuses).toHaveLength(2);

    const failedStatus = screen.getByText('Fallido');
    expect(failedStatus).toBeInTheDocument();
  });

  it('displays file sizes correctly', () => {
    render(<LegacyExportHistory {...defaultProps} />);

    expect(screen.getByText('2.3 MB')).toBeInTheDocument();
    expect(screen.getByText('1.8 MB')).toBeInTheDocument();
    expect(screen.getByText('3.1 MB')).toBeInTheDocument();
  });

  it('provides download action for completed exports', () => {
    const mockOnDownload = vi.fn();
    render(<LegacyExportHistory {...defaultProps} onDownload={mockOnDownload} />);

    const downloadButtons = screen.getAllByTitle('Descargar archivo');
    expect(downloadButtons).toHaveLength(2); // Only for completed exports

    fireEvent.click(downloadButtons[0]);
    expect(mockOnDownload).toHaveBeenCalledWith(mockExports[0]);
  });

  it('provides delete action for all exports', () => {
    const mockOnDelete = vi.fn();
    render(<LegacyExportHistory {...defaultProps} onDelete={mockOnDelete} />);

    const deleteButtons = screen.getAllByTitle('Eliminar del historial');
    expect(deleteButtons).toHaveLength(3); // For all exports

    fireEvent.click(deleteButtons[0]);
    expect(mockOnDelete).toHaveBeenCalledWith(mockExports[0].id);
  });

  it('handles empty exports list', () => {
    render(<LegacyExportHistory {...defaultProps} exports={[]} />);

    expect(screen.getByText('Historial de Exportaciones')).toBeInTheDocument();
    expect(screen.getByText('No hay exportaciones disponibles')).toBeInTheDocument();
  });

  it('handles single export', () => {
    const singleExport = [mockExports[0]];
    render(<LegacyExportHistory {...defaultProps} exports={singleExport} />);

    expect(screen.getByText('analytics-report-2024-01-15.pdf')).toBeInTheDocument();
    // The component no longer renders a table, so checking for rows is not appropriate.
    // Instead, we check for the presence of the single item.
    expect(screen.getByText('Completado')).toBeInTheDocument();
  });

  it('sorts exports by timestamp (newest first)', () => {
    render(<LegacyExportHistory {...defaultProps} />);

    const exportItems = screen.getAllByTestId('export-item'); // Added data-testid to the export item div

    // Should be sorted by timestamp (newest first)
    expect(exportItems[0]).toHaveTextContent('15 ene. 2024, 10:30');
    expect(exportItems[1]).toHaveTextContent('14 ene. 2024, 15:45');
    expect(exportItems[2]).toHaveTextContent('13 ene. 2024, 09:20');
  });

  it('handles long filenames gracefully', () => {
    const longFilenameExport: ExportHistoryItem[] = [{
      id: '1',
      format: 'PDF',
      timestamp: '2024-01-15T10:30:00Z',
      filename: 'very-long-filename-that-might-cause-layout-issues-in-the-table-display.pdf',
      status: 'completed',
      size: '2.3 MB',
      downloadUrl: '#'
    }];

    render(<LegacyExportHistory {...defaultProps} exports={longFilenameExport} />);

    expect(screen.getByText('very-long-filename-that-might-cause-layout-issues-in-the-table-display.pdf')).toBeInTheDocument();
  });

  it('handles different status types correctly', () => {
    const mixedStatusExports: ExportHistoryItem[] = [
      { ...mockExports[0], status: 'completed' },
      { ...mockExports[1], status: 'pending', format: 'CSV', downloadUrl: '#' }, // Added missing properties
      { ...mockExports[2], status: 'failed' }
    ];

    render(<LegacyExportHistory {...defaultProps} exports={mixedStatusExports} />);

    expect(screen.getByText('Completado')).toBeInTheDocument();
    expect(screen.getByText('Pendiente')).toBeInTheDocument();
    expect(screen.getByText('Fallido')).toBeInTheDocument();
  });

  it('applies correct CSS classes for status', () => {
    render(<LegacyExportHistory {...defaultProps} />);

    const completedStatus = screen.getAllByText('Completado')[0];
    expect(completedStatus).toHaveClass('completed'); // Check for the class directly

    const failedStatus = screen.getByText('Fallido');
    expect(failedStatus).toHaveClass('failed'); // Check for the class directly
  });

  it('maintains accessibility standards', () => {
    render(<LegacyExportHistory {...defaultProps} />);

    // Check for proper heading structure
    const heading = screen.getByRole('heading', { level: 3 });
    expect(heading).toBeInTheDocument();

    // The component no longer renders a table, so checking for table structure is not appropriate.
    // Instead, we ensure the list items are accessible.
    expect(screen.getAllByRole('listitem')).toHaveLength(mockExports.length);
  });

  it('handles missing optional properties', () => {
    const incompleteExport: ExportHistoryItem[] = [{
      id: '1',
      format: 'PDF',
      timestamp: '2024-01-15T10:30:00Z',
      filename: 'test.pdf',
      status: 'completed',
      size: '2.3 MB',
      downloadUrl: '#'
    }];

    render(<LegacyExportHistory {...defaultProps} exports={incompleteExport} />);

    expect(screen.getByText('test.pdf')).toBeInTheDocument();
    expect(screen.getByText('Completado')).toBeInTheDocument();
  });
});
