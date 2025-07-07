import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import LegacyKPICard from '../Common/LegacyKPICard';

// Mock Lucide React icons
vi.mock('lucide-react', () => ({
  TrendingUp: vi.fn(() => <div data-testid="trending-up-icon" />),
  TrendingDown: vi.fn(() => <div data-testid="trending-down-icon" />),
  Minus: vi.fn(() => <div data-testid="minus-icon" />),
  FileText: vi.fn(() => <div data-testid="file-text-icon" />),
  Users: vi.fn(() => <div data-testid="users-icon" />),
  Globe: vi.fn(() => <div data-testid="globe-icon" />),
  BarChart: vi.fn(() => <div data-testid="bar-chart-icon" />),
}));

describe('LegacyKPICard', () => {
  it('renders correctly with basic props', () => {
    render(
      <LegacyKPICard
        title="Total Articles"
        value="106"
        icon="FileText"
      />
    );

    expect(screen.getByText('Total Articles')).toBeInTheDocument();
    expect(screen.getByText('106')).toBeInTheDocument();
    expect(screen.getByTestId('file-text-icon')).toBeInTheDocument();
  });

  it('displays change percentage correctly', () => {
    render(
      <LegacyKPICard
        title="Total Articles"
        value="106"
        icon="FileText"
        // change={12.5}
      />
    );

    expect(screen.getByText('+12.5%')).toBeInTheDocument();
  });

  it('displays negative change correctly', () => {
    render(
      <LegacyKPICard
        title="Total Articles"
        value="106"
        icon="FileText"
        // change={-8.3}
      />
    );

    expect(screen.getByText('-8.3%')).toBeInTheDocument();
  });

  it('displays zero change correctly', () => {
    render(
      <LegacyKPICard
        title="Total Articles"
        value="106"
        icon="FileText"
        // change={0}
      />
    );

    expect(screen.getByText('0%')).toBeInTheDocument();
  });

  it('shows correct trend icon for positive change', () => {
    render(
      <LegacyKPICard
        title="Total Articles"
        value="106"
        icon="FileText"
        // change={12.5}
      />
    );

    expect(screen.getByTestId('trending-up-icon')).toBeInTheDocument();
  });

  it('shows correct trend icon for negative change', () => {
    render(
      <LegacyKPICard
        title="Total Articles"
        value="106"
        icon="FileText"
        // change={-8.3}
      />
    );

    expect(screen.getByTestId('trending-down-icon')).toBeInTheDocument();
  });

  it('shows correct trend icon for zero change', () => {
    render(
      <LegacyKPICard
        title="Total Articles"
        value="106"
        icon="FileText"
        // change={0}
      />
    );

    expect(screen.getByTestId('minus-icon')).toBeInTheDocument();
  });

  it('handles different icon types', () => {
    const iconTypes = [
      { icon: 'FileText', testId: 'file-text-icon' },
      { icon: 'Users', testId: 'users-icon' },
      { icon: 'Globe', testId: 'globe-icon' },
      { icon: 'BarChart', testId: 'bar-chart-icon' },
    ];

    iconTypes.forEach(({ icon, testId }) => {
      const { unmount } = render(
        <LegacyKPICard
          title="Test Title"
          value="100"
          icon={icon as any}
        />
      );

      expect(screen.getByTestId(testId)).toBeInTheDocument();
      unmount();
    });
  });

  it('handles large numbers correctly', () => {
    render(
      <LegacyKPICard
        title="Total Views"
        value="1,234,567"
        icon="BarChart"
      />
    );

    expect(screen.getByText('1,234,567')).toBeInTheDocument();
  });

  it('handles decimal values', () => {
    render(
      <LegacyKPICard
        title="Average Score"
        value="4.85"
        icon="BarChart"
      />
    );

    expect(screen.getByText('4.85')).toBeInTheDocument();
  });

  it('handles string values', () => {
    render(
      <LegacyKPICard
        title="Status"
        value="Active"
        icon="FileText"
      />
    );

    expect(screen.getByText('Active')).toBeInTheDocument();
  });

  it('applies correct CSS classes for positive change', () => {
    render(
      <LegacyKPICard
        title="Total Articles"
        value="106"
        icon="FileText"
        // change={12.5}
      />
    );

    const changeElement = screen.getByText('+12.5%');
    expect(changeElement).toHaveClass('text-green-600');
  });

  it('applies correct CSS classes for negative change', () => {
    render(
      <LegacyKPICard
        title="Total Articles"
        value="106"
        icon="FileText"
        // change={-8.3}
      />
    );

    const changeElement = screen.getByText('-8.3%');
    expect(changeElement).toHaveClass('text-red-600');
  });

  it('applies correct CSS classes for zero change', () => {
    render(
      <LegacyKPICard
        title="Total Articles"
        value="106"
        icon="FileText"
        // change={0}
      />
    );

    const changeElement = screen.getByText('0%');
    expect(changeElement).toHaveClass('text-gray-600');
  });

  it('works without change prop', () => {
    render(
      <LegacyKPICard
        title="Total Articles"
        value="106"
        icon="FileText"
      />
    );

    expect(screen.getByText('Total Articles')).toBeInTheDocument();
    expect(screen.getByText('106')).toBeInTheDocument();
    expect(screen.queryByText('%')).not.toBeInTheDocument();
  });

  it('handles very small change values', () => {
    render(
      <LegacyKPICard
        title="Total Articles"
        value="106"
        icon="FileText"
        // change={0.01}
      />
    );

    expect(screen.getByText('+0.01%')).toBeInTheDocument();
  });

  it('handles very large change values', () => {
    render(
      <LegacyKPICard
        title="Total Articles"
        value="106"
        icon="FileText"
        // change={999.99}
      />
    );

    expect(screen.getByText('+999.99%')).toBeInTheDocument();
  });

  it('maintains accessibility standards', () => {
    render(
      <LegacyKPICard
        title="Total Articles"
        value="106"
        icon="FileText"
        // change={12.5}
      />
    );

    // Should have proper structure for screen readers
    const titleElement = screen.getByText('Total Articles');
    expect(titleElement).toBeInTheDocument();

    const valueElement = screen.getByText('106');
    expect(valueElement).toBeInTheDocument();

    // Icon should be present
    expect(screen.getByTestId('file-text-icon')).toBeInTheDocument();
  });

  it('applies correct container CSS classes', () => {
    render(
      <LegacyKPICard
        title="Total Articles"
        value="106"
        icon="FileText"
      />
    );

    const container = screen.getByText('Total Articles').closest('div');
    expect(container).toHaveClass('bg-white', 'p-6', 'rounded-lg', 'shadow-sm');
  });

  it('handles long titles gracefully', () => {
    render(
      <LegacyKPICard
        title="This is a very long title that might cause layout issues in the KPI card component"
        value="106"
        icon="FileText"
      />
    );

    expect(screen.getByText('This is a very long title that might cause layout issues in the KPI card component')).toBeInTheDocument();
  });

  it('handles empty or undefined values', () => {
    render(
      <LegacyKPICard
        title="Total Articles"
        value=""
        icon="FileText"
      />
    );

    expect(screen.getByText('Total Articles')).toBeInTheDocument();
    // Should still render the component structure
    expect(screen.getByTestId('file-text-icon')).toBeInTheDocument();
  });
});
