import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import LegacyNewsTable from '../Analytics/LegacyNewsTable';

// Mock Lucide React icons
vi.mock('lucide-react', () => ({
  ExternalLink: vi.fn(() => <div data-testid="external-link-icon" />),
  Eye: vi.fn(() => <div data-testid="eye-icon" />),
  Calendar: vi.fn(() => <div data-testid="calendar-icon" />),
  Tag: vi.fn(() => <div data-testid="tag-icon" />),
  TrendingUp: vi.fn(() => <div data-testid="trending-up-icon" />),
  TrendingDown: vi.fn(() => <div data-testid="trending-down-icon" />),
  Minus: vi.fn(() => <div data-testid="minus-icon" />),
}));

describe('LegacyNewsTable', () => {
  const mockArticles = [
    {
      id: '1',
      title: 'New Breakthrough in Breast Cancer Treatment',
      summary: 'Researchers discover innovative approach to treatment...',
      url: 'https://example.com/article1',
      date: '2024-01-15',
      topic: 'treatment',
      tone: 'positive',
      country: 'US',
      language: 'EN'
    },
    {
      id: '2',
      title: 'Study Shows Concerning Trends in Cancer Diagnosis',
      summary: 'Latest research reveals troubling patterns...',
      url: 'https://example.com/article2',
      date: '2024-01-14',
      topic: 'research',
      tone: 'negative',
      country: 'UK',
      language: 'EN'
    },
    {
      id: '3',
      title: 'Prevention Guidelines Updated for 2024',
      summary: 'Health organizations release new prevention recommendations...',
      url: 'https://example.com/article3',
      date: '2024-01-13',
      topic: 'prevention',
      tone: 'neutral',
      country: 'CA',
      language: 'EN'
    }
  ];

  it('renders correctly with default props', () => {
    render(<LegacyNewsTable articles={mockArticles} />);

    expect(screen.getByText('News Articles')).toBeInTheDocument();
    expect(screen.getByRole('table')).toBeInTheDocument();
  });

  it('renders with custom title', () => {
    render(<LegacyNewsTable articles={mockArticles} title="Custom News Table" />);

    expect(screen.getByText('Custom News Table')).toBeInTheDocument();
  });

  it('displays correct table headers', () => {
    render(<LegacyNewsTable articles={mockArticles} />);

    expect(screen.getByText('Title')).toBeInTheDocument();
    expect(screen.getByText('Date')).toBeInTheDocument();
    expect(screen.getByText('Topic')).toBeInTheDocument();
    expect(screen.getByText('Sentiment')).toBeInTheDocument();
    expect(screen.getByText('Country')).toBeInTheDocument();
    expect(screen.getByText('Actions')).toBeInTheDocument();
  });

  it('displays all articles', () => {
    render(<LegacyNewsTable articles={mockArticles} />);

    expect(screen.getByText('New Breakthrough in Breast Cancer Treatment')).toBeInTheDocument();
    expect(screen.getByText('Study Shows Concerning Trends in Cancer Diagnosis')).toBeInTheDocument();
    expect(screen.getByText('Prevention Guidelines Updated for 2024')).toBeInTheDocument();
  });

  it('formats dates correctly', () => {
    render(<LegacyNewsTable articles={mockArticles} />);

    expect(screen.getByText('Jan 15, 2024')).toBeInTheDocument();
    expect(screen.getByText('Jan 14, 2024')).toBeInTheDocument();
    expect(screen.getByText('Jan 13, 2024')).toBeInTheDocument();
  });

  it('displays sentiment with correct styling', () => {
    render(<LegacyNewsTable articles={mockArticles} />);

    const positiveElement = screen.getByText('positive');
    const negativeElement = screen.getByText('negative');
    const neutralElement = screen.getByText('neutral');

    expect(positiveElement).toHaveClass('text-green-600');
    expect(negativeElement).toHaveClass('text-red-600');
    expect(neutralElement).toHaveClass('text-gray-600');
  });

  it('truncates long titles correctly', () => {
    const longTitleArticle = [{
      id: '1',
      title: 'This is a very long title that should be truncated when displayed in the table to prevent layout issues and maintain readability',
      summary: 'Short summary',
      url: 'https://example.com/article1',
      date: '2024-01-15',
      topic: 'treatment',
      tone: 'positive',
      country: 'US',
      language: 'EN'
    }];

    render(<LegacyNewsTable articles={longTitleArticle} />);

    // Should truncate long titles
    const titleElement = screen.getByText(/This is a very long title/);
    expect(titleElement).toBeInTheDocument();
  });

  it('provides view action for articles', () => {
    const mockOnView = vi.fn();
    render(<LegacyNewsTable articles={mockArticles} onView={mockOnView} />);

    const viewButtons = screen.getAllByTestId('eye-icon');
    expect(viewButtons).toHaveLength(3);

    fireEvent.click(viewButtons[0].closest('button')!);
    expect(mockOnView).toHaveBeenCalledWith(mockArticles[0]);
  });

  it('provides external link action for articles', () => {
    render(<LegacyNewsTable articles={mockArticles} />);

    const externalLinks = screen.getAllByTestId('external-link-icon');
    expect(externalLinks).toHaveLength(3);

    // Check that links have correct href attributes
    const linkElements = externalLinks.map(icon => icon.closest('a'));
    expect(linkElements[0]).toHaveAttribute('href', 'https://example.com/article1');
    expect(linkElements[1]).toHaveAttribute('href', 'https://example.com/article2');
    expect(linkElements[2]).toHaveAttribute('href', 'https://example.com/article3');
  });

  it('handles empty articles list', () => {
    render(<LegacyNewsTable articles={[]} />);

    expect(screen.getByText('News Articles')).toBeInTheDocument();
    expect(screen.getByText('No articles found')).toBeInTheDocument();
  });

  it('handles pagination correctly', () => {
    const manyArticles = Array.from({ length: 25 }, (_, i) => ({
      id: `${i + 1}`,
      title: `Article ${i + 1}`,
      summary: `Summary ${i + 1}`,
      url: `https://example.com/article${i + 1}`,
      date: '2024-01-15',
      topic: 'treatment',
      tone: 'positive',
      country: 'US',
      language: 'EN'
    }));

    render(<LegacyNewsTable articles={manyArticles} />);

    // Should show pagination controls
    expect(screen.getByText('Previous')).toBeInTheDocument();
    expect(screen.getByText('Next')).toBeInTheDocument();

    // Should show page info
    expect(screen.getByText('Page 1 of 3')).toBeInTheDocument();
  });

  it('handles pagination navigation', () => {
    const manyArticles = Array.from({ length: 25 }, (_, i) => ({
      id: `${i + 1}`,
      title: `Article ${i + 1}`,
      summary: `Summary ${i + 1}`,
      url: `https://example.com/article${i + 1}`,
      date: '2024-01-15',
      topic: 'treatment',
      tone: 'positive',
      country: 'US',
      language: 'EN'
    }));

    render(<LegacyNewsTable articles={manyArticles} />);

    // Click next page
    const nextButton = screen.getByText('Next');
    fireEvent.click(nextButton);

    expect(screen.getByText('Page 2 of 3')).toBeInTheDocument();
    expect(screen.getByText('Article 11')).toBeInTheDocument();
  });

  it('displays topic categories correctly', () => {
    render(<LegacyNewsTable articles={mockArticles} />);

    expect(screen.getByText('treatment')).toBeInTheDocument();
    expect(screen.getByText('research')).toBeInTheDocument();
    expect(screen.getByText('prevention')).toBeInTheDocument();
  });

  it('displays country codes correctly', () => {
    render(<LegacyNewsTable articles={mockArticles} />);

    expect(screen.getByText('US')).toBeInTheDocument();
    expect(screen.getByText('UK')).toBeInTheDocument();
    expect(screen.getByText('CA')).toBeInTheDocument();
  });

  it('handles sorting by date', () => {
    render(<LegacyNewsTable articles={mockArticles} />);

    // Click on date header to sort
    const dateHeader = screen.getByText('Date');
    fireEvent.click(dateHeader);

    // Should sort articles by date
    const rows = screen.getAllByRole('row');
    const firstDataRow = rows[1]; // Skip header row
    expect(firstDataRow).toHaveTextContent('Jan 15, 2024');
  });

  it('handles sorting by title', () => {
    render(<LegacyNewsTable articles={mockArticles} />);

    // Click on title header to sort
    const titleHeader = screen.getByText('Title');
    fireEvent.click(titleHeader);

    // Should sort articles alphabetically
    const rows = screen.getAllByRole('row');
    const firstDataRow = rows[1]; // Skip header row
    expect(firstDataRow).toHaveTextContent('New Breakthrough');
  });

  it('maintains accessibility standards', () => {
    render(<LegacyNewsTable articles={mockArticles} />);

    // Check for proper heading structure
    const heading = screen.getByRole('heading', { level: 3 });
    expect(heading).toBeInTheDocument();

    // Table should have proper structure
    const table = screen.getByRole('table');
    expect(table).toBeInTheDocument();

    // Should have proper column headers
    const columnHeaders = screen.getAllByRole('columnheader');
    expect(columnHeaders).toHaveLength(6);

    // External links should have proper attributes
    const externalLinks = screen.getAllByRole('link');
    externalLinks.forEach(link => {
      expect(link).toHaveAttribute('target', '_blank');
      expect(link).toHaveAttribute('rel', 'noopener noreferrer');
    });
  });

  it('handles articles with missing data', () => {
    const incompleteArticle = [{
      id: '1',
      title: 'Incomplete Article',
      url: 'https://example.com/article1',
      date: '2024-01-15',
      // missing summary, topic, tone, country, language
    }] as any;

    render(<LegacyNewsTable articles={incompleteArticle} />);

    expect(screen.getByText('Incomplete Article')).toBeInTheDocument();
    expect(screen.getByText('Jan 15, 2024')).toBeInTheDocument();
  });

  it('applies correct CSS classes', () => {
    render(<LegacyNewsTable articles={mockArticles} />);

    const tableContainer = screen.getByRole('table').parentElement;
    expect(tableContainer).toHaveClass('bg-white');
  });

  it('handles loading state', () => {
    render(<LegacyNewsTable articles={mockArticles} loading={true} />);

    expect(screen.getByText('Loading articles...')).toBeInTheDocument();
  });

  it('handles error state', () => {
    render(<LegacyNewsTable articles={[]} error="Failed to load articles" />);

    expect(screen.getByText('Error: Failed to load articles')).toBeInTheDocument();
  });
});
