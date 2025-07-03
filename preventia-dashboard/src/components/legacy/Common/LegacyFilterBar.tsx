import React from 'react';

interface FilterState {
  country: string;
  language: string;
  date: string;
  topic: string;
  keyword: string;
}

interface LegacyFilterBarProps {
  filters: FilterState;
  onFilterChange: (filters: Partial<FilterState>) => void;
  showCountryFilter?: boolean;
  showLanguageFilter?: boolean;
  showDateFilter?: boolean;
  showTopicFilter?: boolean;
  showWeekFilter?: boolean;
  showKeywordSearch?: boolean;
}

const LegacyFilterBar: React.FC<LegacyFilterBarProps> = ({
  filters,
  onFilterChange,
  showCountryFilter = false,
  showLanguageFilter = false,
  showDateFilter = false,
  showTopicFilter = false,
  showWeekFilter = false,
  showKeywordSearch = false,
}) => {
  const countries = [
    { value: '', label: 'Todos los países' },
    { value: 'US', label: 'Estados Unidos' },
    { value: 'CO', label: 'Colombia' },
    { value: 'ES', label: 'España' },
    { value: 'MX', label: 'México' },
  ];

  const languages = [
    { value: '', label: 'Todos los idiomas' },
    { value: 'en', label: 'Inglés' },
    { value: 'es', label: 'Español' },
  ];

  const topics = [
    { value: '', label: 'Todos los temas' },
    { value: 'prevention', label: 'Prevención' },
    { value: 'treatment', label: 'Tratamiento' },
    { value: 'diagnosis', label: 'Diagnóstico' },
    { value: 'testimonials', label: 'Testimonios' },
    { value: 'public_policy', label: 'Política Pública' },
    { value: 'research', label: 'Investigación' },
    { value: 'other', label: 'Otros' },
  ];

  return (
    <div className="legacy-filter-bar">
      <div className="legacy-filter-row">
        {showKeywordSearch && (
          <div className="legacy-filter-group">
            <label>Búsqueda por palabra clave:</label>
            <input
              type="text"
              className="legacy-input"
              placeholder="Buscar en título o medio..."
              value={filters.keyword}
              onChange={(e) => onFilterChange({ keyword: e.target.value })}
            />
          </div>
        )}

        {showCountryFilter && (
          <div className="legacy-filter-group">
            <label>País:</label>
            <select
              className="legacy-select"
              value={filters.country}
              onChange={(e) => onFilterChange({ country: e.target.value })}
            >
              {countries.map((country) => (
                <option key={country.value} value={country.value}>
                  {country.label}
                </option>
              ))}
            </select>
          </div>
        )}

        {showLanguageFilter && (
          <div className="legacy-filter-group">
            <label>Idioma:</label>
            <select
              className="legacy-select"
              value={filters.language}
              onChange={(e) => onFilterChange({ language: e.target.value })}
            >
              {languages.map((language) => (
                <option key={language.value} value={language.value}>
                  {language.label}
                </option>
              ))}
            </select>
          </div>
        )}

        {showDateFilter && (
          <div className="legacy-filter-group">
            <label>Fecha:</label>
            <input
              type="date"
              className="legacy-input"
              value={filters.date}
              onChange={(e) => onFilterChange({ date: e.target.value })}
            />
          </div>
        )}

        {showTopicFilter && (
          <div className="legacy-filter-group">
            <label>Tema:</label>
            <select
              className="legacy-select"
              value={filters.topic}
              onChange={(e) => onFilterChange({ topic: e.target.value })}
            >
              {topics.map((topic) => (
                <option key={topic.value} value={topic.value}>
                  {topic.label}
                </option>
              ))}
            </select>
          </div>
        )}

        {showWeekFilter && (
          <div className="legacy-filter-group">
            <label>Semana:</label>
            <select
              className="legacy-select"
              value={filters.date}
              onChange={(e) => onFilterChange({ date: e.target.value })}
            >
              <option value="">Todas las semanas</option>
              <option value="2024-W24">Semana 24</option>
              <option value="2024-W23">Semana 23</option>
              <option value="2024-W22">Semana 22</option>
              <option value="2024-W21">Semana 21</option>
            </select>
          </div>
        )}
      </div>

      <div className="legacy-filter-actions">
        <button
          className="legacy-btn-primary"
          onClick={() => {
            // Filters are already applied in real-time
            console.log('Filters applied:', filters);
          }}
        >
          <i className="fas fa-filter"></i>
          Aplicar filtros
        </button>

        <button
          className="legacy-btn-secondary"
          onClick={() => {
            onFilterChange({
              country: '',
              language: '',
              date: '',
              topic: '',
              keyword: '',
            });
          }}
        >
          <i className="fas fa-times"></i>
          Limpiar filtros
        </button>
      </div>
    </div>
  );
};

export default LegacyFilterBar;
