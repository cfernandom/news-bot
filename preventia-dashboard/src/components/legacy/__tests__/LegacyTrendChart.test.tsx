import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import LegacyTrendChart from '../Analytics/LegacyTrendChart';

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
}));

vi.mock('react-chartjs-2', () => ({
  Line: vi.fn(({ data, options }) => (
    <div data-testid="line-chart">
      <div data-testid="chart-data">{JSON.stringify(data)}</div>
      <div data-testid="chart-options">{JSON.stringify(options)}</div>
    </div>
  )),
}));

describe('LegacyTrendChart', () => {
  const mockData = {
    labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5'],
    positive: [10, 15, 12, 18, 20],
    negative: [25, 20, 28, 15, 22],
    neutral: [5, 8, 6, 7, 10]
  };

  it('renders correctly with default props', () => {
    render(<LegacyTrendChart data={mockData} />);

    expect(screen.getByText('Sentiment Trends')).toBeInTheDocument();
    expect(screen.getByTestId('line-chart')).toBeInTheDocument();
  });

  it('renders with custom title', () => {
    render(<LegacyTrendChart data={mockData} title="Custom Trend Analysis" />);

    expect(screen.getByText('Custom Trend Analysis')).toBeInTheDocument();
  });

  it('displays correct chart data structure', () => {
    render(<LegacyTrendChart data={mockData} />);

    const chartData = screen.getByTestId('chart-data');
    const parsedData = JSON.parse(chartData.textContent || '{}');

    expect(parsedData.labels).toEqual(['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5']);
    expect(parsedData.datasets).toHaveLength(3);

    // Check dataset labels
    const datasetLabels = parsedData.datasets.map((ds: any) => ds.label);
    expect(datasetLabels).toContain('Positive');
    expect(datasetLabels).toContain('Negative');
    expect(datasetLabels).toContain('Neutral');
  });

  it('uses correct colors for sentiment lines', () => {
    render(<LegacyTrendChart data={mockData} />);

    const chartData = screen.getByTestId('chart-data');
    const parsedData = JSON.parse(chartData.textContent || '{}');

    const positiveDataset = parsedData.datasets.find((ds: any) => ds.label === 'Positive');
    const negativeDataset = parsedData.datasets.find((ds: any) => ds.label === 'Negative');
    const neutralDataset = parsedData.datasets.find((ds: any) => ds.label === 'Neutral');

    expect(positiveDataset.borderColor).toBe('#10b981'); // green
    expect(negativeDataset.borderColor).toBe('#ef4444'); // red
    expect(neutralDataset.borderColor).toBe('#6b7280'); // gray
  });

  it('displays correct data values', () => {
    render(<LegacyTrendChart data={mockData} />);

    const chartData = screen.getByTestId('chart-data');
    const parsedData = JSON.parse(chartData.textContent || '{}');

    const positiveDataset = parsedData.datasets.find((ds: any) => ds.label === 'Positive');
    const negativeDataset = parsedData.datasets.find((ds: any) => ds.label === 'Negative');
    const neutralDataset = parsedData.datasets.find((ds: any) => ds.label === 'Neutral');

    expect(positiveDataset.data).toEqual([10, 15, 12, 18, 20]);
    expect(negativeDataset.data).toEqual([25, 20, 28, 15, 22]);
    expect(neutralDataset.data).toEqual([5, 8, 6, 7, 10]);
  });

  it('handles empty data gracefully', () => {
    const emptyData = {
      labels: [],
      positive: [],
      negative: [],
      neutral: []
    };

    render(<LegacyTrendChart data={emptyData} />);

    expect(screen.getByText('Sentiment Trends')).toBeInTheDocument();
    expect(screen.getByTestId('line-chart')).toBeInTheDocument();
  });

  it('handles single data point', () => {
    const singlePointData = {
      labels: ['Week 1'],
      positive: [10],
      negative: [5],
      neutral: [3]
    };

    render(<LegacyTrendChart data={singlePointData} />);

    const chartData = screen.getByTestId('chart-data');
    const parsedData = JSON.parse(chartData.textContent || '{}');

    expect(parsedData.labels).toEqual(['Week 1']);
    expect(parsedData.datasets[0].data).toEqual([10]);
  });

  it('handles missing data properties', () => {
    const incompleteData = {
      labels: ['Week 1', 'Week 2'],
      positive: [10, 15],
      // missing negative and neutral
    } as any;

    render(<LegacyTrendChart data={incompleteData} />);

    const chartData = screen.getByTestId('chart-data');
    const parsedData = JSON.parse(chartData.textContent || '{}');

    // Should handle missing data gracefully
    expect(parsedData.datasets.length).toBeGreaterThan(0);
  });

  it('uses correct chart configuration', () => {
    render(<LegacyTrendChart data={mockData} />);

    const chartOptions = screen.getByTestId('chart-options');
    const parsedOptions = JSON.parse(chartOptions.textContent || '{}');

    expect(parsedOptions.responsive).toBe(true);
    expect(parsedOptions.maintainAspectRatio).toBe(false);
    expect(parsedOptions.plugins.legend.display).toBe(true);
    expect(parsedOptions.scales.y.beginAtZero).toBe(true);
  });

  it('handles large data sets', () => {
    const largeData = {
      labels: Array.from({ length: 52 }, (_, i) => `Week ${i + 1}`),
      positive: Array.from({ length: 52 }, (_, i) => i * 2),
      negative: Array.from({ length: 52 }, (_, i) => i * 3),
      neutral: Array.from({ length: 52 }, (_, i) => i)
    };

    render(<LegacyTrendChart data={largeData} />);

    const chartData = screen.getByTestId('chart-data');
    const parsedData = JSON.parse(chartData.textContent || '{}');

    expect(parsedData.labels).toHaveLength(52);
    expect(parsedData.datasets[0].data).toHaveLength(52);
  });

  it('handles zero values correctly', () => {
    const zeroData = {
      labels: ['Week 1', 'Week 2', 'Week 3'],
      positive: [0, 0, 0],
      negative: [0, 0, 0],
      neutral: [0, 0, 0]
    };

    render(<LegacyTrendChart data={zeroData} />);

    const chartData = screen.getByTestId('chart-data');
    const parsedData = JSON.parse(chartData.textContent || '{}');

    expect(parsedData.datasets[0].data).toEqual([0, 0, 0]);
    expect(parsedData.datasets[1].data).toEqual([0, 0, 0]);
    expect(parsedData.datasets[2].data).toEqual([0, 0, 0]);
  });

  it('handles negative values correctly', () => {
    const negativeData = {
      labels: ['Week 1', 'Week 2'],
      positive: [10, -5], // Should handle negative values
      negative: [-3, 8],
      neutral: [2, -1]
    };

    render(<LegacyTrendChart data={negativeData} />);

    const chartData = screen.getByTestId('chart-data');
    const parsedData = JSON.parse(chartData.textContent || '{}');

    expect(parsedData.datasets[0].data).toEqual([10, -5]);
    expect(parsedData.datasets[1].data).toEqual([-3, 8]);
    expect(parsedData.datasets[2].data).toEqual([2, -1]);
  });

  it('maintains accessibility standards', () => {
    render(<LegacyTrendChart data={mockData} />);

    // Check for proper heading structure
    const heading = screen.getByRole('heading', { level: 3 });
    expect(heading).toBeInTheDocument();

    // Chart should have proper container
    const chartContainer = screen.getByTestId('line-chart');
    expect(chartContainer).toBeInTheDocument();
  });

  it('applies correct CSS classes', () => {
    render(<LegacyTrendChart data={mockData} />);

    const container = screen.getByTestId('line-chart').parentElement;
    expect(container).toHaveClass('bg-white');
  });

  it('handles mismatched data arrays', () => {
    const mismatchedData = {
      labels: ['Week 1', 'Week 2', 'Week 3'],
      positive: [10, 15], // shorter than labels
      negative: [25, 20, 28, 15], // longer than labels
      neutral: [5, 8, 6]
    };

    render(<LegacyTrendChart data={mismatchedData} />);

    // Should still render without errors
    expect(screen.getByTestId('line-chart')).toBeInTheDocument();
  });

  it('handles time period customization', () => {
    render(<LegacyTrendChart data={mockData} timePeriod="monthly" />);

    expect(screen.getByText('Sentiment Trends')).toBeInTheDocument();
    // Should handle different time periods
    expect(screen.getByTestId('line-chart')).toBeInTheDocument();
  });

  it('provides legend interaction', () => {
    render(<LegacyTrendChart data={mockData} />);

    const chartOptions = screen.getByTestId('chart-options');
    const parsedOptions = JSON.parse(chartOptions.textContent || '{}');

    // Legend should be interactive
    expect(parsedOptions.plugins.legend.display).toBe(true);
    expect(parsedOptions.plugins.legend.onClick).toBeDefined();
  });

  it('handles data updates correctly', () => {
    const { rerender } = render(<LegacyTrendChart data={mockData} />);

    const newData = {
      labels: ['Week 6', 'Week 7'],
      positive: [25, 30],
      negative: [10, 5],
      neutral: [15, 20]
    };

    rerender(<LegacyTrendChart data={newData} />);

    const chartData = screen.getByTestId('chart-data');
    const parsedData = JSON.parse(chartData.textContent || '{}');

    expect(parsedData.labels).toEqual(['Week 6', 'Week 7']);
    expect(parsedData.datasets[0].data).toEqual([25, 30]);
  });
});
