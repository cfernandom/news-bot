import React, { useState } from 'react';
import { Badge } from '@/components/ui/badge';
import {
  User,
  LogOut,
  Settings,
  Shield,
  ChevronDown
} from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';

export const UserMenu: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const { user, logout } = useAuth();

  if (!user) return null;

  const handleLogout = async () => {
    await logout();
  };

  return (
    <div className="admin-user-menu">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="admin-user-button"
      >
        <div className="admin-user-avatar">
          <User className="h-4 w-4" />
        </div>
        <div className="admin-user-info">
          <div className="admin-user-name">{user.full_name}</div>
          <div className="admin-user-role">
            {user.role === 'admin' && <Shield className="h-3 w-3" style={{ color: 'var(--admin-primary)' }} />}
            <span>{user.role}</span>
          </div>
        </div>
        <ChevronDown className="h-4 w-4" style={{ color: 'var(--admin-text-muted)' }} />
      </button>

      {isOpen && (
        <>
          {/* Overlay */}
          <div
            className="fixed inset-0 z-10"
            onClick={() => setIsOpen(false)}
          />

          {/* Dropdown */}
          <div className="admin-user-dropdown">
            <div className="admin-user-dropdown-header">
              <div className="flex items-center gap-3">
                <div className="admin-user-avatar">
                  <User className="h-5 w-5" />
                </div>
                <div className="flex-1">
                  <div className="admin-user-name" style={{ fontSize: '0.875rem' }}>{user.full_name}</div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--admin-text-secondary)' }}>{user.email}</div>
                  <div style={{ marginTop: '0.25rem' }}>
                    <Badge variant={user.role === 'admin' ? 'default' : 'secondary'} className="text-xs">
                      {user.role === 'admin' && <Shield className="h-3 w-3 mr-1" />}
                      <span className="capitalize">{user.role}</span>
                    </Badge>
                  </div>
                </div>
              </div>
            </div>

            <div className="admin-user-dropdown-menu">
              <button
                className="admin-user-menu-item"
                onClick={() => {
                  setIsOpen(false);
                  // Add settings navigation here
                }}
              >
                <Settings className="h-4 w-4" />
                Account Settings
              </button>

              <button
                className="admin-user-menu-item danger"
                onClick={() => {
                  setIsOpen(false);
                  handleLogout();
                }}
              >
                <LogOut className="h-4 w-4" />
                Sign Out
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
};
