import React, { useState } from 'react';
import { Shield, Eye, EyeOff, LogIn, AlertCircle } from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';
import '../../styles/admin-theme.css';

export const LoginForm: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      await login(username, password);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Inicio de sesión fallido');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center" style={{ backgroundColor: 'var(--admin-bg)', padding: '1rem' }}>
      <div className="admin-card w-full max-w-md">
        <div className="admin-card-header text-center">
          <div className="flex items-center justify-center mb-6">
            <div className="admin-logo-icon">
              <Shield className="h-6 w-6 text-white" />
            </div>
          </div>
          <div className="admin-card-title">Bienvenido de Nuevo</div>
          <div className="admin-card-subtitle">
            Inicie sesión para acceder al Panel de Administración de Fuentes de Noticias
          </div>
        </div>
        <div>
          <form onSubmit={handleSubmit} className="admin-space-y-4">
            {error && (
              <div className="admin-alert admin-alert-danger">
                <AlertCircle className="h-4 w-4" />
                <span>{error}</span>
              </div>
            )}

            <div className="admin-form-group">
              <label className="admin-label" htmlFor="username">Usuario</label>
              <input
                id="username"
                type="text"
                placeholder="Ingrese su usuario"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                disabled={isLoading}
                className="admin-input"
              />
            </div>

            <div className="admin-form-group">
              <label className="admin-label" htmlFor="password">Contraseña</label>
              <div className="relative">
                <input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  placeholder="Ingrese su contraseña"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  disabled={isLoading}
                  className="admin-input"
                />
                <button
                  type="button"
                  className="admin-btn-ghost"
                  style={{
                    position: 'absolute',
                    right: '0',
                    top: '0',
                    height: '100%',
                    padding: '0.5rem 0.75rem',
                    border: 'none',
                    background: 'transparent'
                  }}
                  onClick={() => setShowPassword(!showPassword)}
                  disabled={isLoading}
                >
                  {showPassword ? (
                    <EyeOff className="h-4 w-4" />
                  ) : (
                    <Eye className="h-4 w-4" />
                  )}
                </button>
              </div>
            </div>

            <button
              type="submit"
              className="admin-btn admin-btn-primary w-full"
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2" />
                  Iniciando sesión...
                </>
              ) : (
                <>
                  <LogIn className="h-4 w-4 mr-2" />
                  Iniciar Sesión
                </>
              )}
            </button>
          </form>

        </div>
      </div>
    </div>
  );
};
