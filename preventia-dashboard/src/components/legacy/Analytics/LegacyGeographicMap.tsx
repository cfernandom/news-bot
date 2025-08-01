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
  title?: string;
  subtitle?: string;
  showClickableMarkers?: boolean;
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

const LegacyGeographicMap: React.FC<LegacyGeographicMapProps> = ({
  data,
  loading,
  subtitle
}) => {
  const [mapLoaded, setMapLoaded] = useState(false);

  // Handle different empty states
  const hasRealData = data && data.length > 0;
  const hasValidCoordinates = hasRealData && data.some(item => item.lat !== 0 && item.lon !== 0);

  // Calculate circle size based on article count
  const getCircleSize = (count: number) => {
    if (!hasRealData) return 8;

    const validCounts = data.filter(d => d.total && d.total > 0).map(d => d.total);
    const maxCount = validCounts.length > 0 ? Math.max(...validCounts) : 1;
    const minSize = 8;
    const maxSize = 30;
    const safeCount = Math.max(count || 0, 1);
    return minSize + ((safeCount / maxCount) * (maxSize - minSize));
  };

  // Get color based on article count intensity
  const getCircleColor = (count: number) => {
    if (!hasRealData) return '#93c5fd';

    const validCounts = data.filter(d => d.total && d.total > 0).map(d => d.total);
    const maxCount = validCounts.length > 0 ? Math.max(...validCounts) : 1;
    const intensity = (count || 0) / maxCount;

    if (intensity > 0.7) {
      return '#1e40af'; // Dark blue
    } else if (intensity > 0.4) {
      return '#3b82f6'; // Medium blue
    } else {
      return '#93c5fd'; // Light blue
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

  if (!hasRealData) {
    return (
      <div className="legacy-chart-container">
        <h3>Cobertura Geográfica</h3>
        <div style={{ height: '400px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
          <i className="fas fa-globe-americas" style={{ fontSize: '48px', color: '#6b7280', marginBottom: '20px' }}></i>
          <p style={{ color: 'var(--text-secondary)', textAlign: 'center' }}>
            No se pudieron obtener los datos geográficos.<br />
            Verifique la conexión con la API.
          </p>
        </div>
      </div>
    );
  }

  if (!hasValidCoordinates) {
    return (
      <div className="legacy-chart-container">
        <h3>Cobertura Geográfica</h3>
        <div style={{ height: '400px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
          <i className="fas fa-map-marker-alt" style={{ fontSize: '48px', color: '#6b7280', marginBottom: '20px' }}></i>
          <p style={{ color: 'var(--text-secondary)', textAlign: 'center' }}>
            Los datos geográficos no contienen coordenadas válidas.<br />
            No es posible mostrar el mapa en este momento.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="legacy-chart-container">
      <h3>Cobertura Geográfica</h3>
      {subtitle && <p className="legacy-chart-subtitle">{subtitle}</p>}

      {/* Map Legend */}
      <div className="legacy-map-legend">
        <div className="legend-item">
          <div className="legend-circle" style={{ backgroundColor: '#93c5fd' }}></div>
          <span>Baja Cobertura</span>
        </div>
        <div className="legend-item">
          <div className="legend-circle" style={{ backgroundColor: '#3b82f6' }}></div>
          <span>Media Cobertura</span>
        </div>
        <div className="legend-item">
          <div className="legend-circle" style={{ backgroundColor: '#1e40af' }}></div>
          <span>Alta Cobertura</span>
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
                  fillColor={getCircleColor(location.total)}
                  color="#ffffff"
                  weight={2}
                  opacity={0.8}
                  fillOpacity={0.7}
                >
                  <Popup>
                    <div className="legacy-map-popup">
                      <h4 style={{ margin: '0 0 8px 0', color: 'var(--primary-blue)' }}>
                        {location.country || 'País desconocido'}
                      </h4>
                      <p style={{ margin: '4px 0', fontSize: '14px' }}>
                        <strong>Artículos:</strong> {location.total || 0}
                      </p>
                      <p style={{ margin: '4px 0', fontSize: '14px' }}>
                        <strong>Idioma:</strong> {location.idioma || 'No especificado'}
                      </p>
                      <p style={{ margin: '4px 0', fontSize: '14px' }}>
                        <strong>Cobertura:</strong>
                        <span style={{
                          marginLeft: '5px',
                          padding: '2px 6px',
                          borderRadius: '3px',
                          backgroundColor: getCircleColor(location.total),
                          color: 'white',
                          fontSize: '12px'
                        }}>
                          {(() => {
                            const validCounts = data.filter(d => d.total && d.total > 0).map(d => d.total);
                            const maxCount = validCounts.length > 0 ? Math.max(...validCounts) : 1;
                            const total = location.total || 0;

                            if (total > maxCount * 0.7) return 'Alta';
                            if (total > maxCount * 0.4) return 'Media';
                            return 'Baja';
                          })()}
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
          <strong>{data.length || 0}</strong>
          <span>Países</span>
        </div>
        <div className="map-stat">
          <strong>{data.reduce((sum, item) => sum + (item.total || 0), 0)}</strong>
          <span>Artículos</span>
        </div>
        <div className="map-stat">
          <strong>{data.filter(item => item.idioma === 'es' || item.idioma === 'ES').length}</strong>
          <span>En Español</span>
        </div>
      </div>
    </div>
  );
};

export default LegacyGeographicMap;
