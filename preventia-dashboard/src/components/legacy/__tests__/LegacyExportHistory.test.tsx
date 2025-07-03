import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import LegacyExportHistory from '../Common/LegacyExportHistory';

// Mock date for consistent testing
const mockDate = new Date('2024-01-15T10:30:00Z');
vi.setSystemTime(mockDate);

describe('LegacyExportHistory', () => {
  const mockExports = [
    {
      id: '1',
      type: 'PDF',
      timestamp: '2024-01-15T10:30:00Z',
      filename: 'analytics-report-2024-01-15.pdf',
      status: 'completed',
      size: '2.3 MB'
    },
    {
      id: '2',
      type: 'CSV',
      timestamp: '2024-01-14T15:45:00Z',
      filename: 'data-export-2024-01-14.csv',
      status: 'completed',
      size: '1.8 MB'
    },
    {
      id: '3',
      type: 'Excel',
      timestamp: '2024-01-13T09:20:00Z',
      filename: 'full-report-2024-01-13.xlsx',
      status: 'failed',
      size: '3.1 MB'
    }
  ];

  it('renders correctly with default props', () => {
    render(<LegacyExportHistory exports={mockExports} />);

    expect(screen.getByText('Export History')).toBeInTheDocument();
    expect(screen.getByRole('table')).toBeInTheDocument();
  });

  it('renders with custom title', () => {
    render(<LegacyExportHistory exports={mockExports} title="Custom Export History" />);

    expect(screen.getByText('Custom Export History')).toBeInTheDocument();
  });

  it('displays correct table headers', () => {
    render(<LegacyExportHistory exports={mockExports} />);

    expect(screen.getByText('Date')).toBeInTheDocument();
    expect(screen.getByText('Type')).toBeInTheDocument();
    expect(screen.getByText('File')).toBeInTheDocument();
    expect(screen.getByText('Status')).toBeInTheDocument();
    expect(screen.getByText('Size')).toBeInTheDocument();
    expect(screen.getByText('Actions')).toBeInTheDocument();
  });

  it('displays all export entries', () => {
    render(<LegacyExportHistory exports={mockExports} />);

    // Check that all 3 exports are displayed
    expect(screen.getByText('analytics-report-2024-01-15.pdf')).toBeInTheDocument();
    expect(screen.getByText('data-export-2024-01-14.csv')).toBeInTheDocument();
    expect(screen.getByText('full-report-2024-01-13.xlsx')).toBeInTheDocument();
  });

  it('formats timestamps correctly', () => {
    render(<LegacyExportHistory exports={mockExports} />);

    // Should format timestamps to readable format
    expect(screen.getByText('Jan 15, 2024')).toBeInTheDocument();
    expect(screen.getByText('Jan 14, 2024')).toBeInTheDocument();
    expect(screen.getByText('Jan 13, 2024')).toBeInTheDocument();
  });

  it('displays correct file types', () => {
    render(<LegacyExportHistory exports={mockExports} />);

    expect(screen.getByText('PDF')).toBeInTheDocument();
    expect(screen.getByText('CSV')).toBeInTheDocument();
    expect(screen.getByText('Excel')).toBeInTheDocument();
  });

  it('shows correct status indicators', () => {
    render(<LegacyExportHistory exports={mockExports} />);

    // Should show status with appropriate styling
    const completedStatuses = screen.getAllByText('completed');
    expect(completedStatuses).toHaveLength(2);

    const failedStatus = screen.getByText('failed');
    expect(failedStatus).toBeInTheDocument();
  });

  it('displays file sizes correctly', () => {
    render(<LegacyExportHistory exports={mockExports} />);

    expect(screen.getByText('2.3 MB')).toBeInTheDocument();
    expect(screen.getByText('1.8 MB')).toBeInTheDocument();
    expect(screen.getByText('3.1 MB')).toBeInTheDocument();
  });

  it('provides download action for completed exports', () => {
    const mockOnDownload = vi.fn();
    render(<LegacyExportHistory exports={mockExports} onDownload={mockOnDownload} />);

    const downloadButtons = screen.getAllByText('Download');
    expect(downloadButtons).toHaveLength(2); // Only for completed exports

    fireEvent.click(downloadButtons[0]);
    expect(mockOnDownload).toHaveBeenCalledWith(mockExports[0]);
  });

  it('provides delete action for all exports', () => {
    const mockOnDelete = vi.fn();
    render(<LegacyExportHistory exports={mockExports} onDelete={mockOnDelete} />);

    const deleteButtons = screen.getAllByText('Delete');
    expect(deleteButtons).toHaveLength(3); // For all exports

    fireEvent.click(deleteButtons[0]);
    expect(mockOnDelete).toHaveBeenCalledWith(mockExports[0]);
  });

  it('handles empty exports list', () => {
    render(<LegacyExportHistory exports={[]} />);

    expect(screen.getByText('Export History')).toBeInTheDocument();
    expect(screen.getByText('No exports found')).toBeInTheDocument();
  });

  it('handles single export', () => {
    const singleExport = [mockExports[0]];
    render(<LegacyExportHistory exports={singleExport} />);

    expect(screen.getByText('analytics-report-2024-01-15.pdf')).toBeInTheDocument();
    expect(screen.getAllByRole('row')).toHaveLength(2); // Header + 1 data row
  });

  it('sorts exports by timestamp (newest first)', () => {
    render(<LegacyExportHistory exports={mockExports} />);

    const rows = screen.getAllByRole('row');
    // Skip header row
    const dataRows = rows.slice(1);

    // Should be sorted by timestamp (newest first)
    expect(dataRows[0]).toHaveTextContent('Jan 15, 2024');
    expect(dataRows[1]).toHaveTextContent('Jan 14, 2024');
    expect(dataRows[2]).toHaveTextContent('Jan 13, 2024');
  });

  it('handles long filenames gracefully', () => {
    const longFilenameExport = [{
      id: '1',
      type: 'PDF',
      timestamp: '2024-01-15T10:30:00Z',
      filename: 'very-long-filename-that-might-cause-layout-issues-in-the-table-display.pdf',
      status: 'completed',
      size: '2.3 MB'
    }];

    render(<LegacyExportHistory exports={longFilenameExport} />);

    expect(screen.getByText('very-long-filename-that-might-cause-layout-issues-in-the-table-display.pdf')).toBeInTheDocument();
  });

  it('handles different status types correctly', () => {
    const mixedStatusExports = [
      { ...mockExports[0], status: 'completed' },
      { ...mockExports[1], status: 'pending' },
      { ...mockExports[2], status: 'failed' }
    ];

    render(<LegacyExportHistory exports={mixedStatusExports} />);

    expect(screen.getByText('completed')).toBeInTheDocument();
    expect(screen.getByText('pending')).toBeInTheDocument();
    expect(screen.getByText('failed')).toBeInTheDocument();
  });

  it('applies correct CSS classes for status', () => {
    render(<LegacyExportHistory exports={mockExports} />);

    const completedStatus = screen.getAllByText('completed')[0];
    expect(completedStatus).toHaveClass('text-green-600');

    const failedStatus = screen.getByText('failed');
    expect(failedStatus).toHaveClass('text-red-600');
  });

  it('maintains accessibility standards', () => {
    render(<LegacyExportHistory exports={mockExports} />);

    // Check for proper heading structure
    const heading = screen.getByRole('heading', { level: 3 });
    expect(heading).toBeInTheDocument();

    // Table should have proper structure
    const table = screen.getByRole('table');
    expect(table).toBeInTheDocument();

    // Should have proper column headers
    const columnHeaders = screen.getAllByRole('columnheader');
    expect(columnHeaders).toHaveLength(6);
  });

  it('handles missing optional properties', () => {
    const incompleteExport = [{
      id: '1',
      type: 'PDF',
      timestamp: '2024-01-15T10:30:00Z',
      filename: 'test.pdf',
      status: 'completed'
      // missing size
    }] as any;

    render(<LegacyExportHistory exports={incompleteExport} />);

    expect(screen.getByText('test.pdf')).toBeInTheDocument();
    expect(screen.getByText('completed')).toBeInTheDocument();
  });
});
