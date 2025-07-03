import React, { useState, useEffect } from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import LegacyHeader from './LegacyHeader';
import '../../../styles/legacy/legacy-theme.css';

interface LegacyLayoutProps {
  children?: React.ReactNode;
}

const LegacyLayout: React.FC<LegacyLayoutProps> = ({ children }) => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const location = useLocation();

  // Removed scroll-based header hiding for better UX

  // Close mobile menu when route changes
  useEffect(() => {
    setIsMobileMenuOpen(false);
  }, [location]);

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  return (
    <div className="legacy-app">
      <LegacyHeader
        isVisible={true}
        isMobileMenuOpen={isMobileMenuOpen}
        onToggleMobileMenu={toggleMobileMenu}
      />

      <main className="legacy-main">
        <div className="legacy-container">
          {children || <Outlet />}
        </div>
      </main>
    </div>
  );
};

export default LegacyLayout;
