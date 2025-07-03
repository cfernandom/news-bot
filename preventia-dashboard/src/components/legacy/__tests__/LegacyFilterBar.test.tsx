import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import LegacyFilterBar from '../Common/LegacyFilterBar';

// Mock Lucide React icons
vi.mock('lucide-react', () => ({
  Filter: vi.fn(() => <div data-testid="filter-icon" />),
  Calendar: vi.fn(() => <div data-testid="calendar-icon" />),
  Search: vi.fn(() => <div data-testid="search-icon" />),
  X: vi.fn(() => <div data-testid="x-icon" />),
}));

describe('LegacyFilterBar', () => {
  const mockOnFilterChange = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders correctly with default props', () => {
    render(<LegacyFilterBar onFilterChange={mockOnFilterChange} />);

    expect(screen.getByTestId('filter-icon')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Search articles...')).toBeInTheDocument();
    expect(screen.getByText('All Topics')).toBeInTheDocument();
    expect(screen.getByText('All Countries')).toBeInTheDocument();
    expect(screen.getByText('All Sentiments')).toBeInTheDocument();
  });

  it('displays search input correctly', () => {
    render(<LegacyFilterBar onFilterChange={mockOnFilterChange} />);

    const searchInput = screen.getByPlaceholderText('Search articles...');
    expect(searchInput).toBeInTheDocument();
    expect(searchInput).toHaveAttribute('type', 'text');
  });

  it('handles search input changes', () => {
    render(<LegacyFilterBar onFilterChange={mockOnFilterChange} />);

    const searchInput = screen.getByPlaceholderText('Search articles...');
    fireEvent.change(searchInput, { target: { value: 'breast cancer' } });

    expect(mockOnFilterChange).toHaveBeenCalledWith(
      expect.objectContaining({
        search: 'breast cancer'
      })
    );
  });

  it('displays topic filter dropdown', () => {
    render(<LegacyFilterBar onFilterChange={mockOnFilterChange} />);

    const topicSelect = screen.getByDisplayValue('All Topics');
    expect(topicSelect).toBeInTheDocument();

    // Check if dropdown options are available
    const options = screen.getAllByRole('option');
    expect(options.length).toBeGreaterThan(1);
  });

  it('handles topic filter changes', () => {
    render(<LegacyFilterBar onFilterChange={mockOnFilterChange} />);

    const topicSelect = screen.getByDisplayValue('All Topics');
    fireEvent.change(topicSelect, { target: { value: 'treatment' } });

    expect(mockOnFilterChange).toHaveBeenCalledWith(
      expect.objectContaining({
        topic: 'treatment'
      })
    );
  });

  it('displays country filter dropdown', () => {
    render(<LegacyFilterBar onFilterChange={mockOnFilterChange} />);

    const countrySelect = screen.getByDisplayValue('All Countries');
    expect(countrySelect).toBeInTheDocument();
  });

  it('handles country filter changes', () => {
    render(<LegacyFilterBar onFilterChange={mockOnFilterChange} />);

    const countrySelect = screen.getByDisplayValue('All Countries');
    fireEvent.change(countrySelect, { target: { value: 'US' } });

    expect(mockOnFilterChange).toHaveBeenCalledWith(
      expect.objectContaining({
        country: 'US'
      })
    );
  });

  it('displays sentiment filter dropdown', () => {
    render(<LegacyFilterBar onFilterChange={mockOnFilterChange} />);

    const sentimentSelect = screen.getByDisplayValue('All Sentiments');
    expect(sentimentSelect).toBeInTheDocument();
  });

  it('handles sentiment filter changes', () => {
    render(<LegacyFilterBar onFilterChange={mockOnFilterChange} />);

    const sentimentSelect = screen.getByDisplayValue('All Sentiments');
    fireEvent.change(sentimentSelect, { target: { value: 'positive' } });

    expect(mockOnFilterChange).toHaveBeenCalledWith(
      expect.objectContaining({
        sentiment: 'positive'
      })
    );
  });

  it('displays date range inputs', () => {
    render(<LegacyFilterBar onFilterChange={mockOnFilterChange} />);

    const fromDateInput = screen.getByLabelText('From Date');
    const toDateInput = screen.getByLabelText('To Date');

    expect(fromDateInput).toBeInTheDocument();
    expect(toDateInput).toBeInTheDocument();
    expect(fromDateInput).toHaveAttribute('type', 'date');
    expect(toDateInput).toHaveAttribute('type', 'date');
  });

  it('handles date range changes', () => {
    render(<LegacyFilterBar onFilterChange={mockOnFilterChange} />);

    const fromDateInput = screen.getByLabelText('From Date');
    const toDateInput = screen.getByLabelText('To Date');

    fireEvent.change(fromDateInput, { target: { value: '2024-01-01' } });
    fireEvent.change(toDateInput, { target: { value: '2024-12-31' } });

    expect(mockOnFilterChange).toHaveBeenCalledWith(
      expect.objectContaining({
        dateFrom: '2024-01-01'
      })
    );

    expect(mockOnFilterChange).toHaveBeenCalledWith(
      expect.objectContaining({
        dateTo: '2024-12-31'
      })
    );
  });

  it('provides clear filters functionality', () => {
    render(<LegacyFilterBar onFilterChange={mockOnFilterChange} />);

    // First apply some filters
    const searchInput = screen.getByPlaceholderText('Search articles...');
    fireEvent.change(searchInput, { target: { value: 'test' } });

    // Then clear them
    const clearButton = screen.getByText('Clear Filters');
    fireEvent.click(clearButton);

    expect(mockOnFilterChange).toHaveBeenCalledWith({
      search: '',
      topic: '',
      country: '',
      sentiment: '',
      dateFrom: '',
      dateTo: ''
    });
  });

  it('shows active filter count', () => {
    render(<LegacyFilterBar onFilterChange={mockOnFilterChange} />);

    // Apply some filters
    const searchInput = screen.getByPlaceholderText('Search articles...');
    fireEvent.change(searchInput, { target: { value: 'test' } });

    const topicSelect = screen.getByDisplayValue('All Topics');
    fireEvent.change(topicSelect, { target: { value: 'treatment' } });

    // Should show active filter count
    expect(screen.getByText('2 active filters')).toBeInTheDocument();
  });

  it('handles initial filter values', () => {
    const initialFilters = {
      search: 'initial search',
      topic: 'treatment',
      country: 'US',
      sentiment: 'positive',
      dateFrom: '2024-01-01',
      dateTo: '2024-12-31'
    };

    render(<LegacyFilterBar onFilterChange={mockOnFilterChange} initialFilters={initialFilters} />);

    expect(screen.getByDisplayValue('initial search')).toBeInTheDocument();
    expect(screen.getByDisplayValue('treatment')).toBeInTheDocument();
    expect(screen.getByDisplayValue('US')).toBeInTheDocument();
    expect(screen.getByDisplayValue('positive')).toBeInTheDocument();
    expect(screen.getByDisplayValue('2024-01-01')).toBeInTheDocument();
    expect(screen.getByDisplayValue('2024-12-31')).toBeInTheDocument();
  });

  it('validates date range input', () => {
    render(<LegacyFilterBar onFilterChange={mockOnFilterChange} />);

    const fromDateInput = screen.getByLabelText('From Date');
    const toDateInput = screen.getByLabelText('To Date');

    // Set 'to' date before 'from' date
    fireEvent.change(fromDateInput, { target: { value: '2024-12-31' } });
    fireEvent.change(toDateInput, { target: { value: '2024-01-01' } });

    // Should show validation message
    expect(screen.getByText('End date must be after start date')).toBeInTheDocument();
  });

  it('applies correct CSS classes', () => {
    render(<LegacyFilterBar onFilterChange={mockOnFilterChange} />);

    const filterContainer = screen.getByTestId('filter-icon').closest('div');
    expect(filterContainer).toHaveClass('bg-white', 'p-4', 'rounded-lg', 'shadow-sm');
  });

  it('maintains accessibility standards', () => {
    render(<LegacyFilterBar onFilterChange={mockOnFilterChange} />);

    // Check for proper labels
    expect(screen.getByLabelText('Search articles')).toBeInTheDocument();
    expect(screen.getByLabelText('Filter by topic')).toBeInTheDocument();
    expect(screen.getByLabelText('Filter by country')).toBeInTheDocument();
    expect(screen.getByLabelText('Filter by sentiment')).toBeInTheDocument();
    expect(screen.getByLabelText('From Date')).toBeInTheDocument();
    expect(screen.getByLabelText('To Date')).toBeInTheDocument();
  });

  it('handles multiple rapid filter changes', () => {
    render(<LegacyFilterBar onFilterChange={mockOnFilterChange} />);

    const searchInput = screen.getByPlaceholderText('Search articles...');

    // Rapid changes
    fireEvent.change(searchInput, { target: { value: 'a' } });
    fireEvent.change(searchInput, { target: { value: 'ab' } });
    fireEvent.change(searchInput, { target: { value: 'abc' } });

    // Should debounce the calls
    expect(mockOnFilterChange).toHaveBeenCalledTimes(3);
  });

  it('handles empty filter state correctly', () => {
    render(<LegacyFilterBar onFilterChange={mockOnFilterChange} />);

    // Should show no active filters initially
    expect(screen.queryByText('active filters')).not.toBeInTheDocument();

    // Should show default dropdown values
    expect(screen.getByDisplayValue('All Topics')).toBeInTheDocument();
    expect(screen.getByDisplayValue('All Countries')).toBeInTheDocument();
    expect(screen.getByDisplayValue('All Sentiments')).toBeInTheDocument();
  });

  it('persists filter state correctly', () => {
    const { rerender } = render(<LegacyFilterBar onFilterChange={mockOnFilterChange} />);

    // Apply a filter
    const searchInput = screen.getByPlaceholderText('Search articles...');
    fireEvent.change(searchInput, { target: { value: 'test search' } });

    // Re-render with same props
    rerender(<LegacyFilterBar onFilterChange={mockOnFilterChange} />);

    // State should be persisted
    expect(screen.getByDisplayValue('test search')).toBeInTheDocument();
  });
});
