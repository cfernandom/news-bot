---
version: "1.0"
last_updated: "2025-07-07"
maintainer: "Claude (Technical Director)"
status: "active"
language: "English"
---

# Technology Stack Documentation

This document provides a comprehensive overview of the technology stack used in PreventIA News Analytics, including justifications for technology choices, version requirements, and implementation patterns.

## 🏗️ Architecture Overview

### System Architecture Pattern
- **Pattern**: Microservices with Modular Monolith transition
- **Communication**: REST API + WebSocket for real-time
- **Data Flow**: Event-driven with batch processing
- **Deployment**: Container-first with Docker Compose

### Technology Decision Principles
1. **Medical Domain Specialization**: Technologies optimized for healthcare content
2. **Academic Research Focus**: Open source, reproducible, auditable
3. **Compliance-First**: Legal and ethical considerations prioritized
4. **Performance**: Sub-3s dashboard response times
5. **Maintainability**: Clear separation of concerns, extensive testing

## 🐍 Backend Technology Stack

### Core Framework
```yaml
FastAPI: 0.115+
  Justification:
    - Async/await native support for high concurrency
    - Automatic OpenAPI documentation generation
    - Type hints integration with Pydantic
    - Excellent performance (comparable to Node.js)
    - Medical research API standards compliance

  Key Features Used:
    - Dependency injection for database connections
    - Background tasks for NLP processing
    - WebSocket support for real-time updates
    - Automatic request/response validation
    - JWT authentication middleware
```

### Database Layer
```yaml
PostgreSQL: 16+
  Justification:
    - JSONB support for flexible medical metadata
    - Full-text search capabilities for article content
    - ACID compliance for data integrity
    - Excellent analytics query performance
    - Strong geospatial support for geographic analysis

  Key Features:
    - JSONB columns for NLP analysis results
    - B-tree indexes for time-series queries
    - Partial indexes for active articles
    - Materialized views for analytics aggregation
    - Row-level security for multi-tenant future

SQLAlchemy: 2.0+
  Justification:
    - Hybrid ORM + raw SQL approach
    - Async session support with asyncpg
    - Type-safe query building
    - Migration management with Alembic
    - Connection pooling and health monitoring

  Usage Pattern:
    - ORM for CRUD operations
    - Raw SQL for complex analytics
    - Pydantic integration for API models
    - Background task database access
```

### Cache and Session Layer
```yaml
Redis: 7.0+
  Justification:
    - Sub-millisecond response times for dashboard
    - Session storage for authentication
    - Real-time WebSocket message broker
    - Rate limiting implementation
    - Analytics query result caching

  Usage Patterns:
    - Key structure: "analytics:{type}:{timeframe}:{hash}"
    - TTL-based cache invalidation
    - Pub/sub for real-time dashboard updates
    - Lua scripts for atomic operations
```

### NLP and Analytics
```yaml
spaCy: 3.8+
  Justification:
    - Industrial-strength NLP with medical models
    - Efficient batch processing capabilities
    - Custom pipeline components for medical entities
    - Multi-language support (English/Spanish)
    - Token-level analysis for keyword extraction

  Models Used:
    - en_core_web_sm: English language processing
    - Medical NER models for healthcare entities
    - Custom breast cancer terminology

VADER Sentiment: 3.3+
  Justification:
    - Rule-based approach suitable for medical content
    - No training data required (important for compliance)
    - Handles medical terminology and abbreviations
    - Explainable results for academic transparency
    - Conservative thresholds for medical news

  Configuration:
    - Compound score threshold: ±0.3 (vs ±0.05 standard)
    - Medical context adjustments
    - Batch processing optimization

Pandas: 2.0+
  Justification:
    - Analytics aggregation and time-series analysis
    - Data export functionality (CSV, Excel)
    - Statistical analysis for trend detection
    - Integration with visualization libraries
```

### Web Scraping
```yaml
Playwright: 1.40+
  Justification:
    - JavaScript-heavy medical sites support
    - Reliable rendering of React/Angular medical portals
    - Anti-bot detection evasion capabilities
    - Screenshot capture for debugging
    - Cross-browser testing support

  Usage:
    - Chromium browser for production scraping
    - Headless mode for server deployment
    - Network request interception
    - Mobile device emulation

BeautifulSoup4: 4.12+
  Justification:
    - Robust HTML parsing for diverse medical sites
    - Flexible selector system (CSS + XPath)
    - Encoding detection and handling
    - Memory-efficient for large documents
    - Excellent error handling for malformed HTML

aiohttp: 3.9+
  Justification:
    - Async HTTP client for concurrent scraping
    - Connection pooling and keep-alive
    - Timeout and retry configuration
    - Cookie and session management
    - Custom headers for compliance
```

### Task Processing and Automation
```yaml
asyncio: Built-in
  Justification:
    - Native async/await for I/O-bound operations
    - Concurrent scraping without threading complexity
    - Database connection pooling support
    - WebSocket real-time communication
    - Background task processing

APScheduler: 3.10+
  Justification:
    - Cron-like scheduling for batch processing
    - Persistent job storage in database
    - Multiple executor support (async, thread, process)
    - Job clustering for high availability
    - Dynamic job management via API
```

## ⚛️ Frontend Technology Stack

### Core Framework
```yaml
React: 19+
  Justification:
    - Large ecosystem for data visualization
    - Excellent TypeScript integration
    - Component reusability for dashboard widgets
    - Strong community support for medical UIs
    - Concurrent features for performance

  Key Libraries:
    - React Query for API state management
    - React Hook Form for form handling
    - React Router for navigation
    - React Suspense for loading states

TypeScript: 5.0+
  Justification:
    - Type safety for complex medical data structures
    - Better IDE support and refactoring
    - Compile-time error detection
    - Self-documenting code for academic standards
    - Interface definitions for API contracts
```

### Data Visualization
```yaml
Recharts: 2.8+
  Justification:
    - React-native charts with TypeScript support
    - Responsive design for dashboard widgets
    - Customizable medical data visualizations
    - Accessible charts for academic presentations
    - Easy theming and color schemes

Chart.js: 4.4+
  Justification:
    - Advanced chart types (radar, polar)
    - Animation support for engagement
    - Plugin ecosystem for medical visualizations
    - Canvas-based rendering for performance
    - Export capabilities for research papers

Leaflet: 1.9+
  Justification:
    - Interactive maps for geographic analysis
    - Lightweight with plugin ecosystem
    - Custom markers for medical facility mapping
    - GeoJSON support for country boundaries
    - Mobile-friendly touch interaction
```

### UI Framework and Styling
```yaml
Material-UI (MUI): 5.14+
  Justification:
    - Medical dashboard-appropriate design system
    - Accessibility built-in (WCAG compliance)
    - Consistent theming across components
    - Form components optimized for data entry
    - Professional appearance for academic use

Tailwind CSS: 3.3+
  Justification:
    - Utility-first for rapid prototyping
    - Responsive design system
    - Small bundle size with purging
    - Custom medical color schemes
    - Easy dark mode implementation
```

### Build Tools and Development
```yaml
Vite: 5.0+
  Justification:
    - Fast development server with HMR
    - Optimal production builds
    - TypeScript support out-of-the-box
    - Plugin ecosystem for optimization
    - ES modules for modern browsers

ESLint + Prettier: Latest
  Justification:
    - Code quality and consistency
    - Medical code review standards
    - Automated formatting for team collaboration
    - TypeScript-aware linting rules
    - Pre-commit hooks integration
```

## 🛠️ Development and DevOps

### Containerization
```yaml
Docker: 24.0+
  Justification:
    - Consistent development and production environments
    - Easy deployment to various cloud providers
    - Isolation for security compliance
    - Resource constraints for cost optimization
    - Multi-stage builds for optimization

Docker Compose: 2.20+
  Justification:
    - Local development stack orchestration
    - Service dependency management
    - Environment variable configuration
    - Health check integration
    - Volume management for data persistence
```

### Testing Framework
```yaml
pytest: 7.4+
  Justification:
    - Academic-standard testing with fixtures
    - Async test support for database operations
    - Parametrized tests for data validation
    - Coverage reporting for compliance
    - Plugin ecosystem for specialized testing

pytest-asyncio: 0.21+
  Justification:
    - Async database and API testing
    - WebSocket testing support
    - Background task testing
    - Integration test scenarios

Vitest: 1.0+
  Justification:
    - Fast TypeScript test execution
    - React component testing with RTL
    - API mocking capabilities
    - Coverage reporting
    - Watch mode for development

Playwright Test: 1.40+
  Justification:
    - End-to-end dashboard testing
    - Cross-browser compatibility testing
    - Visual regression testing
    - API testing capabilities
    - CI/CD integration
```

### Code Quality and Security
```yaml
Black: 23.0+
  Justification:
    - Consistent Python code formatting
    - Reduces code review overhead
    - Medical code standards compliance
    - IDE integration support

Ruff: 0.1+
  Justification:
    - Fast Python linting and formatting
    - Security vulnerability detection
    - Import sorting and organization
    - TypeScript-like performance for Python

pre-commit: 3.5+
  Justification:
    - Automated code quality checks
    - Prevents bad commits to main branch
    - Security scanning before commit
    - Consistent team development practices

Bandit: 1.7+
  Justification:
    - Security vulnerability scanning
    - Medical data privacy compliance
    - SQL injection detection
    - Credential scanning in code
```

## 🔧 Production Infrastructure

### Deployment
```yaml
Nginx: 1.24+
  Justification:
    - Reverse proxy for API and frontend
    - SSL/TLS termination
    - Static file serving
    - Load balancing capabilities
    - Rate limiting for API protection

Production Configuration:
    - Gzip compression for API responses
    - Caching headers for static assets
    - Security headers for medical compliance
    - Request size limits for uploads
```

### Monitoring and Observability
```yaml
Prometheus: 2.45+
  Justification:
    - Time-series metrics collection
    - Custom medical analytics metrics
    - Alert rule configuration
    - Integration with FastAPI metrics
    - Historical performance analysis

Grafana: 10.0+
  Justification:
    - Medical dashboard monitoring
    - Custom metric visualization
    - Alert notification management
    - Team collaboration features
    - Data source integration

Sentry: 1.32+
  Justification:
    - Error tracking and monitoring
    - Performance monitoring
    - Medical data privacy compliance
    - Team notification integration
    - Release tracking
```

## 🔍 Technology Alternatives Considered

### Backend Framework Alternatives
| Technology | Pros | Cons | Decision |
|------------|------|------|----------|
| Django REST | Mature, admin interface | Synchronous, heavy | ❌ Slower for real-time |
| Flask | Lightweight, familiar | Manual setup, no async | ❌ Too much boilerplate |
| Node.js + Express | JavaScript ecosystem | Different language | ❌ Team expertise |
| **FastAPI** | Modern, async, types | Newer ecosystem | ✅ **Selected** |

### Database Alternatives
| Technology | Pros | Cons | Decision |
|------------|------|------|----------|
| MongoDB | Flexible schema | No ACID, complex queries | ❌ Medical data needs ACID |
| MySQL | Familiar, widespread | Limited JSON support | ❌ Weaker analytics features |
| SQLite | Simple, embedded | Not scalable | ❌ Production limitations |
| **PostgreSQL** | Feature-rich, reliable | Setup complexity | ✅ **Selected** |

### Frontend Framework Alternatives
| Technology | Pros | Cons | Decision |
|------------|------|------|----------|
| Vue.js | Gentle learning curve | Smaller ecosystem | ❌ Less visualization libs |
| Angular | Enterprise features | Complex, TypeScript required | ❌ Overkill for dashboard |
| Svelte | Performance, simplicity | Smaller community | ❌ Limited medical UI libs |
| **React** | Large ecosystem, mature | Learning curve | ✅ **Selected** |

## 📊 Performance Benchmarks

### Database Performance
```yaml
Query Types:
  - Simple article lookup: <50ms
  - Analytics aggregation: <500ms
  - Complex dashboard queries: <2s
  - Full-text search: <100ms
  - Batch NLP processing: 0.5s/article

Optimization Strategies:
  - Partial indexes for active articles
  - Materialized views for weekly analytics
  - Connection pooling (10-20 connections)
  - Query result caching (1-hour TTL)
```

### API Performance
```yaml
Endpoint Benchmarks:
  - Health check: <100ms
  - Article CRUD: <200ms
  - Dashboard analytics: <1s
  - Search endpoints: <300ms
  - Export generation: <5s

Concurrency:
  - 100 concurrent users supported
  - Rate limiting: 60 requests/minute
  - WebSocket: 50 concurrent connections
  - Background tasks: 10 concurrent workers
```

### Frontend Performance
```yaml
Loading Times:
  - Initial dashboard load: <2s
  - Chart rendering: <500ms
  - Data table updates: <200ms
  - Real-time updates: <100ms
  - Report export: <3s

Bundle Sizes:
  - Main bundle: ~800KB (gzipped)
  - Chart libraries: ~200KB
  - UI framework: ~150KB
  - Total initial load: ~1.2MB
```

## 🔄 Technology Upgrade Strategy

### Version Management
```yaml
Strategy: Conservative with Security Priority
  - Security patches: Immediate
  - Minor versions: Monthly review
  - Major versions: Quarterly evaluation
  - Breaking changes: Planned migration

Testing Approach:
  - Development environment first
  - Automated test suite validation
  - Performance regression testing
  - Staging environment validation
  - Gradual production rollout
```

### Dependency Management
```python
# Python dependencies with pinned versions
fastapi==0.115.0
sqlalchemy==2.0.25
redis==5.0.1
spacy==3.8.2

# JavaScript dependencies with semantic versioning
"react": "^19.0.0",
"typescript": "^5.3.0",
"vite": "^5.0.0"
```

## 📚 Documentation and Resources

### Official Documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [React Documentation](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

### Internal Resources
- [Local Development Setup](../development/setup/local-development.md)
- [Environment Variables](../development/setup/environment-variables.md)
- [Testing Strategy](../development/standards/testing-strategy.md)
- [API Documentation](../api/services/)

---

**Technology Stack Principles:**
- **Medical Focus**: Every technology choice considers healthcare domain requirements
- **Academic Standards**: Open source, reproducible, well-documented
- **Performance**: Sub-3s response times for all user interactions
- **Compliance**: GDPR, medical data privacy, legal compliance built-in
- **Maintainability**: Clear patterns, extensive testing, monitoring

**Last Updated**: 2025-07-07
**Next Review**: 2025-10-07
**Maintainer**: Claude (Technical Director)
