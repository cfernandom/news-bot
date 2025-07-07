// @ts-nocheck
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import LegacyTopicsChart from '../Analytics/LegacyTopicsChart';

// Mock Chart.js
vi.mock('chart.js', () => ({
  Chart: {
    register: vi.fn(),
    getChart: vi.fn(),
  },
  CategoryScale: vi.fn(),
  LinearScale: vi.fn(),
  BarElement: vi.fn(),
  Title: vi.fn(),
  Tooltip: vi.fn(),
  Legend: vi.fn(),
}));

vi.mock('react-chartjs-2', () => ({
  Bar: vi.fn(({ data, options }) => (
    <div data-testid="bar-chart">
      <div data-testid="chart-data">{JSON.stringify(data)}</div>
      <div data-testid="chart-options">{JSON.stringify(options)}</div>
    </div>
  )),
}));

describe('LegacyTopicsChart', () => {
  const mockData = {
    'treatment': 45,
    'research': 30,
    'prevention': 25,
    'diagnosis': 20,
    'awareness': 15
  };

  it('renders correctly with default props', () => {
    render(<LegacyTopicsChart data={mockData} />);

    expect(screen.getByText('Topics Distribution')).toBeInTheDocument();
    expect(screen.getByTestId('bar-chart')).toBeInTheDocument();
  });

  it('renders with custom title', () => {
    render(<LegacyTopicsChart data={mockData} title="Custom Topics Title" />);

    expect(screen.getByText('Custom Topics Title')).toBeInTheDocument();
  });

  it('displays correct data for topics chart', () => {
    render(<LegacyTopicsChart data={mockData} />);

    const chartData = screen.getByTestId('chart-data');
    const parsedData = JSON.parse(chartData.textContent || '{}');

    expect(parsedData.labels).toEqual(['treatment', 'research', 'prevention', 'diagnosis', 'awareness']);
    expect(parsedData.datasets[0].data).toEqual([45, 30, 25, 20, 15]);
    expect(parsedData.datasets[0].backgroundColor).toBeDefined();
  });

  it('handles language breakdown correctly', () => {
    render(<LegacyTopicsChart data={mockData} />);

    const chartData = screen.getByTestId('chart-data');
    const parsedData = JSON.parse(chartData.textContent || '{}');

    // Check that chart shows language breakdown (Spanish/English)
    expect(parsedData.datasets[0].label).toBe('Spanish');
    expect(parsedData.datasets[1].label).toBe('English');
  });

  it('uses correct color scheme for languages', () => {
    render(<LegacyTopicsChart data={mockData} />);

    const chartData = screen.getByTestId('chart-data');
    const parsedData = JSON.parse(chartData.textContent || '{}');

    // Spanish should be blue, English should be green
    expect(parsedData.datasets[0].backgroundColor).toBe('#3b82f6'); // Spanish - blue
    expect(parsedData.datasets[1].backgroundColor).toBe('#10b981'); // English - green
  });

  it('handles empty data gracefully', () => {
    const emptyData = {};
    render(<LegacyTopicsChart data={emptyData} />);

    expect(screen.getByText('Topics Distribution')).toBeInTheDocument();
    expect(screen.getByTestId('bar-chart')).toBeInTheDocument();
  });

  it('handles single topic correctly', () => {
    const singleTopicData = { 'treatment': 100 };
    render(<LegacyTopicsChart data={singleTopicData} />);

    const chartData = screen.getByTestId('chart-data');
    const parsedData = JSON.parse(chartData.textContent || '{}');

    expect(parsedData.labels).toEqual(['treatment']);
    expect(parsedData.datasets[0].data).toEqual([100]);
  });

  it('sorts topics by value in descending order', () => {
    const unsortedData = {
      'awareness': 15,
      'treatment': 45,
      'prevention': 25,
      'research': 30,
      'diagnosis': 20
    };

    render(<LegacyTopicsChart data={unsortedData} />);

    const chartData = screen.getByTestId('chart-data');
    const parsedData = JSON.parse(chartData.textContent || '{}');

    // Should be sorted by value (descending)
    expect(parsedData.labels).toEqual(['treatment', 'research', 'prevention', 'diagnosis', 'awareness']);
    expect(parsedData.datasets[0].data).toEqual([45, 30, 25, 20, 15]);
  });

  it('uses correct chart configuration', () => {
    render(<LegacyTopicsChart data={mockData} />);

    const chartOptions = screen.getByTestId('chart-options');
    const parsedOptions = JSON.parse(chartOptions.textContent || '{}');

    expect(parsedOptions.responsive).toBe(true);
    expect(parsedOptions.maintainAspectRatio).toBe(false);
    expect(parsedOptions.plugins.legend.display).toBe(true);
    expect(parsedOptions.scales.y.beginAtZero).toBe(true);
  });

  it('handles large numbers correctly', () => {
    const largeData = { 'treatment': 10000, 'research': 5000 };
    render(<LegacyTopicsChart data={largeData} />);

    const chartData = screen.getByTestId('chart-data');
    const parsedData = JSON.parse(chartData.textContent || '{}');

    expect(parsedData.datasets[0].data).toEqual([10000, 5000]);
  });

  it('maintains accessibility standards', () => {
    render(<LegacyTopicsChart data={mockData} />);

    // Check for proper heading structure
    const heading = screen.getByRole('heading', { level: 3 });
    expect(heading).toBeInTheDocument();

    // Chart should have proper container
    const chartContainer = screen.getByTestId('bar-chart');
    expect(chartContainer).toBeInTheDocument();
  });

  it('handles topic name formatting', () => {
    const dataWithSpecialChars = {
      'breast-cancer-treatment': 30,
      'early_detection': 25,
      'RESEARCH': 20
    };

    render(<LegacyTopicsChart data={dataWithSpecialChars} />);

    const chartData = screen.getByTestId('chart-data');
    const parsedData = JSON.parse(chartData.textContent || '{}');

    // Should handle special characters in topic names
    expect(parsedData.labels).toContain('breast-cancer-treatment');
    expect(parsedData.labels).toContain('early_detection');
    expect(parsedData.labels).toContain('RESEARCH');
  });

  it('applies correct CSS classes', () => {
    render(<LegacyTopicsChart data={mockData} />);

    const container = screen.getByTestId('bar-chart').parentElement;
    expect(container).toHaveClass('bg-white');
  });
});
