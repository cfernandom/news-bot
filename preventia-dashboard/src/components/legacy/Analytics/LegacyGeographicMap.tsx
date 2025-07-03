import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

interface GeographicData {
  country: string;
  lat: number;
  lon: number;
  total: number;
  idioma: string;
  tono: string;
}

interface LegacyGeographicMapProps {
  data: GeographicData[];
  loading?: boolean;
}

// Custom component to fit bounds when data changes
const FitBounds: React.FC<{ data: GeographicData[] }> = ({ data }) => {
  const map = useMap();

  useEffect(() => {
    if (data.length > 0) {
      const bounds = data.map(item => [item.lat, item.lon] as [number, number]);
      map.fitBounds(bounds, { padding: [20, 20] });
    }
  }, [data, map]);

  return null;
};

const LegacyGeographicMap: React.FC<LegacyGeographicMapProps> = ({ data, loading }) => {
  const [mapLoaded, setMapLoaded] = useState(false);

  // Calculate circle size based on article count
  const getCircleSize = (count: number) => {
    const maxCount = Math.max(...data.map(d => d.total));
    const minSize = 8;
    const maxSize = 30;
    return minSize + ((count / maxCount) * (maxSize - minSize));
  };

  // Get color based on sentiment
  const getCircleColor = (tono: string) => {
    switch (tono.toLowerCase()) {
      case 'positivo':
        return '#10b981'; // green
      case 'negativo':
        return '#ef4444'; // red
      default:
        return '#6b7280'; // gray
    }
  };

  if (loading) {
    return (
      <div className="legacy-chart-container">
        <h3>Cobertura Geográfica</h3>
        <div style={{ height: '400px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <div className="legacy-loading-spinner">
            <i className="fas fa-spinner fa-spin" style={{ fontSize: '24px', color: 'var(--primary-blue)' }}></i>
            <p style={{ marginTop: '10px', color: 'var(--text-secondary)' }}>Cargando mapa...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="legacy-chart-container">
      <h3>Cobertura Geográfica</h3>

      {/* Map Legend */}
      <div className="legacy-map-legend">
        <div className="legend-item">
          <div className="legend-circle" style={{ backgroundColor: '#10b981' }}></div>
          <span>Tono Positivo</span>
        </div>
        <div className="legend-item">
          <div className="legend-circle" style={{ backgroundColor: '#6b7280' }}></div>
          <span>Tono Neutro</span>
        </div>
        <div className="legend-item">
          <div className="legend-circle" style={{ backgroundColor: '#ef4444' }}></div>
          <span>Tono Negativo</span>
        </div>
      </div>

      <div className="legacy-map-container" style={{ height: '380px', borderRadius: '8px', overflow: 'hidden' }}>
        <MapContainer
          center={[20, 0]}
          zoom={2}
          style={{ height: '100%', width: '100%' }}
          whenReady={() => setMapLoaded(true)}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          {mapLoaded && data.length > 0 && (
            <>
              <FitBounds data={data} />

              {data.map((location, index) => (
                <CircleMarker
                  key={index}
                  center={[location.lat, location.lon]}
                  radius={getCircleSize(location.total)}
                  fillColor={getCircleColor(location.tono)}
                  color="#ffffff"
                  weight={2}
                  opacity={0.8}
                  fillOpacity={0.7}
                >
                  <Popup>
                    <div className="legacy-map-popup">
                      <h4 style={{ margin: '0 0 8px 0', color: 'var(--primary-blue)' }}>
                        {location.country}
                      </h4>
                      <p style={{ margin: '4px 0', fontSize: '14px' }}>
                        <strong>Artículos:</strong> {location.total}
                      </p>
                      <p style={{ margin: '4px 0', fontSize: '14px' }}>
                        <strong>Idioma:</strong> {location.idioma}
                      </p>
                      <p style={{ margin: '4px 0', fontSize: '14px' }}>
                        <strong>Tono:</strong>
                        <span style={{
                          marginLeft: '5px',
                          padding: '2px 6px',
                          borderRadius: '3px',
                          backgroundColor: getCircleColor(location.tono),
                          color: 'white',
                          fontSize: '12px'
                        }}>
                          {location.tono}
                        </span>
                      </p>
                    </div>
                  </Popup>
                </CircleMarker>
              ))}
            </>
          )}
        </MapContainer>
      </div>

      {/* Map Stats */}
      <div className="legacy-map-stats">
        <div className="map-stat">
          <strong>{data.length}</strong>
          <span>Países</span>
        </div>
        <div className="map-stat">
          <strong>{data.reduce((sum, item) => sum + item.total, 0)}</strong>
          <span>Artículos</span>
        </div>
        <div className="map-stat">
          <strong>{data.filter(item => item.idioma === 'Español').length}</strong>
          <span>En Español</span>
        </div>
      </div>
    </div>
  );
};

export default LegacyGeographicMap;
