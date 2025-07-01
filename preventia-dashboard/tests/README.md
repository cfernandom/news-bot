# Testing Strategy - PreventIA Dashboard

## Estrategia de Pruebas para Dashboard React

### Estructura de Testing

```
tests/
├── README.md                    # Esta guía
├── unit/                       # Pruebas unitarias
│   ├── components/             # Componentes React
│   ├── services/              # API client y servicios
│   └── hooks/                 # Custom hooks
├── integration/               # Pruebas de integración
│   ├── api-client/           # Integración con API
│   └── dashboard/            # Dashboard completo
├── e2e/                      # Pruebas end-to-end
│   ├── user-flows/           # Flujos de usuario
│   └── dual-mode/            # Funcionalidad dual-mode
└── utils/                    # Utilidades de testing
    ├── test-setup.js         # Configuración global
    ├── api-mocks.js          # Mocks de API
    └── fixtures/             # Datos de prueba
```

### Herramientas de Testing

#### Core Testing Stack
- **Vitest**: Framework de testing (compatible con Vite)
- **React Testing Library**: Testing de componentes React
- **MSW (Mock Service Worker)**: Mocking de API calls
- **Puppeteer**: Testing E2E y validaciones visuales

#### Instalación
```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom msw
npm install -D @testing-library/user-event jsdom
```

### Tipos de Pruebas

#### 1. Unit Tests (Pruebas Unitarias)
**Objetivo**: Probar componentes y funciones aisladamente

**Archivos a probar**:
- `src/services/api.ts` - MedicalApiClient
- `src/hooks/useMedicalData.ts` - Custom hooks
- `src/components/dashboard/MedicalKPIGrid.tsx` - Componente principal
- `src/components/adaptive/AdaptiveKPICard.tsx` - Componentes adaptativos

**Ejemplo de estructura**:
```javascript
// tests/unit/services/api.test.ts
describe('MedicalApiClient', () => {
  test('should fetch analytics summary', async () => {
    // Mock API response
    // Test transformation
    // Verify data structure
  });
});
```

#### 2. Integration Tests (Pruebas de Integración)
**Objetivo**: Probar interacciones entre componentes y servicios

**Casos a probar**:
- Dashboard completo con datos reales
- Hooks + API client + componentes
- Error boundaries con fallos simulados
- Dual-mode functionality

#### 3. E2E Tests (Pruebas End-to-End)
**Objetivo**: Probar flujos completos de usuario

**Casos implementados**:
- ✅ Carga inicial del dashboard
- ✅ Visualización de KPIs con datos reales
- ✅ Cambio entre modos profesional/educativo
- ✅ Manejo de errores de API

### Comandos de Testing

```bash
# Pruebas unitarias
npm run test:unit

# Pruebas de integración
npm run test:integration

# Pruebas E2E
npm run test:e2e

# Todas las pruebas
npm run test

# Coverage report
npm run test:coverage

# Watch mode (desarrollo)
npm run test:watch
```

### Testing Scripts Implementados

#### Scripts de Validación E2E (`tests/e2e/`)
1. **`simple-validation.js`** - Validación básica del dashboard
2. **`test-dual-mode.js`** - Funcionalidad dual-mode
3. **`test-api-client.js`** - Validación directa de API client
4. **`test-error-boundary.js`** - Pruebas de error boundary
5. **`validate-dashboard.js`** - Validación completa con screenshots
6. **`final-validation.js`** - Validación final comprehensiva

#### Metricas de Testing Actuales
- ✅ 9/9 validaciones básicas (100%)
- ✅ API integration funcionando
- ✅ Dual-mode operativo
- ✅ Error boundaries implementados

### Standards de Testing

#### Para Componentes React
```javascript
// Estructura estándar
describe('ComponentName', () => {
  beforeEach(() => {
    // Setup mocks
  });

  test('should render with medical data', () => {
    // Test rendering
    // Verify data display
    // Check accessibility
  });

  test('should handle loading states', () => {
    // Test loading UI
  });

  test('should handle error states', () => {
    // Test error UI
    // Test error recovery
  });
});
```

#### Para API Client
```javascript
// Estructura para servicios
describe('MedicalApiClient', () => {
  test('should transform API response correctly', () => {
    // Mock API response
    // Test data transformation
    // Verify TypeScript types
  });
});
```

### Coverage Goals

- **Unit Tests**: 80% minimum coverage
- **Components**: 90% coverage (critical medical components)
- **API Client**: 95% coverage (data integrity)
- **Error Boundaries**: 100% coverage (safety critical)

### Testing en CI/CD

```yaml
# GitHub Actions example
test:
  runs-on: ubuntu-latest
  steps:
    - name: Run unit tests
      run: npm run test:unit

    - name: Run integration tests
      run: npm run test:integration

    - name: Generate coverage
      run: npm run test:coverage
```

### Próximos Pasos

1. **Implementar Vitest configuration**
2. **Crear unit tests para MedicalApiClient**
3. **Implementar integration tests para dashboard**
4. **Configurar MSW para API mocking**
5. **Integrar tests en workflow Git**

### Notas de Implementación

- Los scripts actuales (Puppeteer) servirán como base para E2E tests
- Priorizar testing de componentes críticos médicos
- Mantener coverage alto para funcionalidad de seguridad
- Documentar casos edge específicos del dominio médico
