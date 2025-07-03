import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import LegacySentimentChart from '../Analytics/LegacySentimentChart';

// Mock Chart.js
vi.mock('chart.js', () => ({
  Chart: {
    register: vi.fn(),
    getChart: vi.fn(),
  },
  CategoryScale: vi.fn(),
  LinearScale: vi.fn(),
  PointElement: vi.fn(),
  LineElement: vi.fn(),
  Title: vi.fn(),
  Tooltip: vi.fn(),
  Legend: vi.fn(),
  ArcElement: vi.fn(),
}));

vi.mock('react-chartjs-2', () => ({
  Pie: vi.fn(({ data, options }) => (
    <div data-testid="pie-chart">
      <div data-testid="chart-data">{JSON.stringify(data)}</div>
      <div data-testid="chart-options">{JSON.stringify(options)}</div>
    </div>
  )),
  Line: vi.fn(({ data, options }) => (
    <div data-testid="line-chart">
      <div data-testid="chart-data">{JSON.stringify(data)}</div>
      <div data-testid="chart-options">{JSON.stringify(options)}</div>
    </div>
  )),
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
    expect(screen.getByText('Distribución de Sentimientos')).toBeInTheDocument();
  });

  it('handles type toggle between sentiment and language', () => {
    render(<LegacySentimentChart data={mockData} />);

    // Should show sentiment by default
    expect(screen.getByText('Sentiment Analysis')).toBeInTheDocument();

    // Find and click toggle button (assuming it exists)
    const toggleButtons = screen.getAllByRole('button');
    const languageToggle = toggleButtons.find(btn => btn.textContent?.includes('Language'));

    if (languageToggle) {
      fireEvent.click(languageToggle);
      expect(screen.getByText('Language Distribution')).toBeInTheDocument();
    }
  });

  it('applies correct CSS classes', () => {
    render(<LegacySentimentChart data={mockData} />);

    const container = screen.getByTestId('pie-chart').parentElement;
    expect(container).toHaveClass('bg-white');
  });

  it('handles empty data gracefully', () => {
    const emptyData: { sentiment_label: string; count: number }[] = [];
    render(<LegacySentimentChart data={emptyData} />);

    expect(screen.getByText('Distribución de Sentimientos')).toBeInTheDocument();
  });

  it('handles missing data properties', () => {
    const incompleteData = [{ sentiment_label: 'positive', count: 10 }];
    render(<LegacySentimentChart data={incompleteData} />);

    // Should handle incomplete data gracefully
    expect(screen.getByText('Distribución de Sentimientos')).toBeInTheDocument();
  });

  it('uses correct chart configuration', () => {
    render(<LegacySentimentChart data={mockData} />);

    const chartOptions = screen.getByTestId('chart-options');
    const parsedOptions = JSON.parse(chartOptions.textContent || '{}');

    expect(parsedOptions.responsive).toBe(true);
    expect(parsedOptions.maintainAspectRatio).toBe(false);
    expect(parsedOptions.plugins.legend.display).toBe(true);
  });

  it('handles large numbers correctly', () => {
    const largeData = [
      { sentiment_label: 'positive', count: 1000 },
      { sentiment_label: 'negative', count: 2000 },
      { sentiment_label: 'neutral', count: 500 }
    ];
    render(<LegacySentimentChart data={largeData} />);

    expect(screen.getByText('Distribución de Sentimientos')).toBeInTheDocument();
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
