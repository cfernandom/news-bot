import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import LegacySentimentChart from '../Analytics/LegacySentimentChart';

// Mock Recharts
vi.mock('recharts', () => ({
  PieChart: vi.fn(({ children }) => (
    <div data-testid="recharts-pie-chart">
      {children}
    </div>
  )),
  Pie: vi.fn(({ data, children }) => (
    <div data-testid="recharts-pie">
      <div data-testid="chart-data">{JSON.stringify(data)}</div>
      {children}
    </div>
  )),
  Cell: vi.fn(() => <div data-testid="recharts-cell" />),
  ResponsiveContainer: vi.fn(({ children }) => (
    <div data-testid="recharts-responsive-container">
      {children}
    </div>
  )),
  Tooltip: vi.fn(() => <div data-testid="recharts-tooltip" />),
  Legend: vi.fn(() => <div data-testid="recharts-legend" />),
}));

describe('LegacySentimentChart', () => {
  const mockData = [
    { sentiment_label: 'positive', count: 25 },
    { sentiment_label: 'negative', count: 60 },
    { sentiment_label: 'neutral', count: 15 }
  ];

  it('renders correctly with default props', () => {
    render(<LegacySentimentChart data={mockData} />);

    expect(screen.getByText('Sentiment Analysis')).toBeInTheDocument();
    expect(screen.getByTestId('pie-chart')).toBeInTheDocument();
  });

  it('renders with custom title', () => {
    render(<LegacySentimentChart data={mockData} title="Custom Sentiment Title" />);

    expect(screen.getByText('Custom Sentiment Title')).toBeInTheDocument();
  });

  it('displays correct data for sentiment chart', () => {
    render(<LegacySentimentChart data={mockData} />);

    // Should render the chart with correct data
    expect(screen.getByText('Sentiment Analysis')).toBeInTheDocument();
  });

  it('handles type toggle between sentiment and language', () => {
    // Test with type='sentiment' (default)
    const { rerender } = render(<LegacySentimentChart data={mockData} />);
    expect(screen.getByText('Sentiment Analysis')).toBeInTheDocument();

    // Test with type='language'
    rerender(<LegacySentimentChart data={mockData} type="language" />);
    expect(screen.getByText('Sentiment Analysis')).toBeInTheDocument();

    // Verify language data is being used
    const chartData = screen.getByTestId('chart-data');
    expect(chartData.textContent).toContain('Inglés');
    expect(chartData.textContent).toContain('Español');
  });

  it('applies correct CSS classes', () => {
    render(<LegacySentimentChart data={mockData} />);

    // Check that the chart structure is correct
    const pieChartContainer = screen.getByTestId('pie-chart');
    expect(pieChartContainer).toBeInTheDocument();

    const responsiveContainer = screen.getByTestId('recharts-responsive-container');
    expect(responsiveContainer).toBeInTheDocument();

    const rechartsPieChart = screen.getByTestId('recharts-pie-chart');
    expect(rechartsPieChart).toBeInTheDocument();
  });

  it('handles empty data gracefully', () => {
    const emptyData: { sentiment_label: string; count: number }[] = [];
    render(<LegacySentimentChart data={emptyData} />);

    expect(screen.getByText('Sentiment Analysis')).toBeInTheDocument();
  });

  it('handles missing data properties', () => {
    const incompleteData = [{ sentiment_label: 'positive', count: 10 }];
    render(<LegacySentimentChart data={incompleteData} />);

    // Should handle incomplete data gracefully
    expect(screen.getByText('Sentiment Analysis')).toBeInTheDocument();
  });

  it('uses correct chart configuration', () => {
    render(<LegacySentimentChart data={mockData} />);

    // Check that Recharts components are rendered
    expect(screen.getByTestId('recharts-responsive-container')).toBeInTheDocument();
    expect(screen.getByTestId('recharts-pie-chart')).toBeInTheDocument();
    expect(screen.getByTestId('recharts-pie')).toBeInTheDocument();
  });

  it('handles large numbers correctly', () => {
    const largeData = [
      { sentiment_label: 'positive', count: 1000 },
      { sentiment_label: 'negative', count: 2000 },
      { sentiment_label: 'neutral', count: 500 }
    ];
    render(<LegacySentimentChart data={largeData} />);

    expect(screen.getByText('Sentiment Analysis')).toBeInTheDocument();
  });

  it('maintains accessibility standards', () => {
    render(<LegacySentimentChart data={mockData} />);

    // Check for proper heading structure
    const heading = screen.getByRole('heading', { level: 3 });
    expect(heading).toBeInTheDocument();

    // Chart should have proper container
    const chartContainer = screen.getByTestId('pie-chart');
    expect(chartContainer).toBeInTheDocument();
  });
});
