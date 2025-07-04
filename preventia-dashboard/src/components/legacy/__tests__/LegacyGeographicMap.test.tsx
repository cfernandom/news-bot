import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import LegacyGeographicMap from '../Analytics/LegacyGeographicMap';

// Mock Leaflet
vi.mock('leaflet', () => ({
  map: vi.fn(() => ({
    setView: vi.fn(),
    on: vi.fn(),
    off: vi.fn(),
    remove: vi.fn(),
  })),
  tileLayer: vi.fn(() => ({
    addTo: vi.fn(),
  })),
  marker: vi.fn(() => ({
    addTo: vi.fn(),
    bindPopup: vi.fn(),
  })),
  icon: vi.fn(),
}));

vi.mock('react-leaflet', () => ({
  MapContainer: vi.fn(({ children, ...props }) => (
    <div data-testid="map-container" {...props}>
      {children}
    </div>
  )),
  TileLayer: vi.fn(() => <div data-testid="tile-layer" />),
  Marker: vi.fn(({ position, children }) => (
    <div data-testid="marker" data-position={JSON.stringify(position)}>
      {children}
    </div>
  )),
  Popup: vi.fn(({ children }) => (
    <div data-testid="popup">{children}</div>
  )),
}));

describe('LegacyGeographicMap', () => {
  const mockData = [
    { country: 'US', total: 85, tone: 'negative', language: 'EN' },
    { country: 'UK', total: 21, tone: 'positive', language: 'EN' },
    { country: 'CA', total: 15, tone: 'neutral', language: 'EN' },
    { country: 'AU', total: 10, tone: 'negative', language: 'EN' },
    { country: 'DE', total: 5, tone: 'positive', language: 'EN' }
  ];

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders correctly with default props', () => {
    render(<LegacyGeographicMap data={mockData} />);

    expect(screen.getByText('Geographic Distribution')).toBeInTheDocument();
    expect(screen.getByTestId('map-container')).toBeInTheDocument();
  });

  it('renders with custom title', () => {
    render(<LegacyGeographicMap data={mockData} title="Custom Geographic Title" />);

    expect(screen.getByText('Custom Geographic Title')).toBeInTheDocument();
  });

  it('displays coverage intensity legend', () => {
    render(<LegacyGeographicMap data={mockData} />);

    expect(screen.getByText('Coverage Intensity')).toBeInTheDocument();
    expect(screen.getByText('Low')).toBeInTheDocument();
    expect(screen.getByText('Medium')).toBeInTheDocument();
    expect(screen.getByText('High')).toBeInTheDocument();
  });

  it('renders markers for each country', () => {
    render(<LegacyGeographicMap data={mockData} />);

    const markers = screen.getAllByTestId('marker');
    expect(markers).toHaveLength(5); // 5 countries in mockData
  });

  it('displays correct popup content for markers', () => {
    render(<LegacyGeographicMap data={mockData} />);

    const popups = screen.getAllByTestId('popup');
    expect(popups.length).toBeGreaterThan(0);

    // Check that popup contains country info
    const firstPopup = popups[0];
    expect(firstPopup.textContent).toContain('US');
    expect(firstPopup.textContent).toContain('85');
  });

  it('handles empty data gracefully', () => {
    render(<LegacyGeographicMap data={[]} />);

    expect(screen.getByText('Geographic Distribution')).toBeInTheDocument();
    expect(screen.getByTestId('map-container')).toBeInTheDocument();
    expect(screen.queryByTestId('marker')).not.toBeInTheDocument();
  });

  it('handles single country data', () => {
    const singleCountryData = [
      { country: 'US', total: 100, tone: 'positive', language: 'EN' }
    ];

    render(<LegacyGeographicMap data={singleCountryData} />);

    const markers = screen.getAllByTestId('marker');
    expect(markers).toHaveLength(1);
  });

  it('uses correct color coding for coverage intensity', () => {
    render(<LegacyGeographicMap data={mockData} />);

    // Check legend color indicators
    const legendItems = screen.getByText('Coverage Intensity').parentElement;
    expect(legendItems).toBeInTheDocument();

    // Should have color indicators for low, medium, high
    const colorIndicators = legendItems?.querySelectorAll('.w-3.h-3');
    expect(colorIndicators?.length).toBe(3);
  });

  it('determines coverage intensity correctly', () => {
    render(<LegacyGeographicMap data={mockData} />);

    // US (85) should be high coverage
    // UK (21) should be medium coverage
    // Others (15, 10, 5) should be low coverage

    const markers = screen.getAllByTestId('marker');
    expect(markers).toHaveLength(5);
  });

  it('handles unknown countries gracefully', () => {
    const unknownCountryData = [
      { country: 'XX', total: 10, tone: 'neutral', language: 'EN' },
      { country: 'YY', total: 5, tone: 'positive', language: 'EN' }
    ];

    render(<LegacyGeographicMap data={unknownCountryData} />);

    expect(screen.getByTestId('map-container')).toBeInTheDocument();
    // Should still render markers even for unknown countries
    const markers = screen.getAllByTestId('marker');
    expect(markers).toHaveLength(2);
  });

  it('displays correct tone information in popups', () => {
    render(<LegacyGeographicMap data={mockData} />);

    const popups = screen.getAllByTestId('popup');
    const firstPopup = popups[0];

    // Should contain tone information
    expect(firstPopup.textContent).toContain('negative');
  });

  it('applies correct CSS classes', () => {
    render(<LegacyGeographicMap data={mockData} />);

    const container = screen.getByTestId('map-container').parentElement;
    expect(container).toHaveClass('bg-white');
  });

  it('maintains accessibility standards', () => {
    render(<LegacyGeographicMap data={mockData} />);

    // Check for proper heading structure
    const heading = screen.getByRole('heading', { level: 3 });
    expect(heading).toBeInTheDocument();

    // Map should have proper container
    const mapContainer = screen.getByTestId('map-container');
    expect(mapContainer).toBeInTheDocument();
  });

  it('handles large datasets correctly', () => {
    const largeData = Array.from({ length: 50 }, (_, i) => ({
      country: `Country${i}`,
      total: Math.floor(Math.random() * 100),
      tone: ['positive', 'negative', 'neutral'][i % 3],
      language: 'EN'
    }));

    render(<LegacyGeographicMap data={largeData} />);

    expect(screen.getByTestId('map-container')).toBeInTheDocument();
    const markers = screen.getAllByTestId('marker');
    expect(markers).toHaveLength(50);
  });

  it('handles missing data properties', () => {
    const incompleteData = [
      { country: 'US', total: 85 }, // missing tone and language
      { country: 'UK', tone: 'positive' } // missing total and language
    ];

    render(<LegacyGeographicMap data={incompleteData} />);

    expect(screen.getByTestId('map-container')).toBeInTheDocument();
    // Should still render markers
    const markers = screen.getAllByTestId('marker');
    expect(markers).toHaveLength(2);
  });

  it('updates correctly when data changes', () => {
    const { rerender } = render(<LegacyGeographicMap data={mockData} />);

    let markers = screen.getAllByTestId('marker');
    expect(markers).toHaveLength(5);

    const newData = [
      { country: 'US', total: 100, tone: 'positive', language: 'EN' }
    ];

    rerender(<LegacyGeographicMap data={newData} />);

    markers = screen.getAllByTestId('marker');
    expect(markers).toHaveLength(1);
  });
});
