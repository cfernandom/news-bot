import React from 'react';
import { Link, useLocation } from 'react-router-dom';

interface LegacyHeaderProps {
  isVisible: boolean;
  isMobileMenuOpen: boolean;
  onToggleMobileMenu: () => void;
}

const LegacyHeader: React.FC<LegacyHeaderProps> = ({
  isVisible,
  isMobileMenuOpen,
  onToggleMobileMenu
}) => {
  const location = useLocation();

  const navigationItems = [
    { path: '/', label: 'Inicio', exact: true },
    { path: '/about', label: 'Sobre el Cáncer' },
    { path: '/prevention', label: 'Prevención' },
    { path: '/self-exam', label: 'Autoexamen' },
    { path: '/institutions', label: 'Instituciones' },
    { path: '/project', label: 'Proyecto' },
    { path: '/contact', label: 'Contacto' },
    { path: '/noticias', label: 'Noticias' }
  ];

  const isActive = (path: string, exact?: boolean) => {
    if (exact) {
      return location.pathname === path;
    }
    return location.pathname.startsWith(path);
  };

  return (
    <header className={`legacy-header ${isVisible ? '' : 'hidden'}`}>
      <div className="legacy-header-container">
        <Link to="/" className="legacy-logo">
          PreventIA
        </Link>

        <button
          className="legacy-mobile-menu-btn"
          onClick={onToggleMobileMenu}
          aria-label="Toggle mobile menu"
        >
          <i className={`fas ${isMobileMenuOpen ? 'fa-times' : 'fa-bars'}`}></i>
        </button>

        <nav className={`legacy-nav ${isMobileMenuOpen ? 'active' : ''}`}>
          {navigationItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={isActive(item.path, item.exact) ? 'active' : ''}
            >
              {item.label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
};

export default LegacyHeader;
