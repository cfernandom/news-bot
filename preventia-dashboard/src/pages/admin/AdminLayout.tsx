import React from 'react';
import { ProtectedRoute } from '@/components/auth/ProtectedRoute';
import { UserMenu } from '@/components/auth/UserMenu';
import { AuthProvider } from '@/contexts/AuthContext';
import '../../styles/admin-theme.css';

interface AdminLayoutProps {
  children: React.ReactNode;
}

export const AdminLayout: React.FC<AdminLayoutProps> = ({ children }) => {
  return (
    <AuthProvider>
      <ProtectedRoute requireAdmin={true}>
        <div className="admin-page">
          {/* Header */}
          <header className="admin-header">
            <div className="admin-header-container">
              <div className="admin-logo">
                <div className="admin-logo-icon">
                  <span className="text-white font-bold text-sm">P</span>
                </div>
                <div>
                  <div className="admin-logo-text">PreventIA</div>
                  <div className="admin-logo-subtitle">Administración de Fuentes de Noticias</div>
                </div>
              </div>
              <UserMenu />
            </div>
          </header>

          {/* Main Content */}
          <main className="admin-main">
            <div className="admin-container">
              <div className="admin-content">
                {children}
              </div>
            </div>
          </main>
        </div>
      </ProtectedRoute>
    </AuthProvider>
  );
};
