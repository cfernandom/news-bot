# PreventIA Dashboard - React Frontend

## Overview

React + TypeScript + Vite dashboard for PreventIA News Analytics with dual-mode architecture (Professional/Educational) and comprehensive medical data visualizations.

## Features

- **Dual-Mode Interface**: Switch between Professional and Educational modes
- **Real-time Analytics**: Live sentiment analysis and medical topic tracking
- **Medical Visualizations**: Specialized charts for healthcare data
- **API Integration**: Full integration with FastAPI backend
- **Professional Testing**: E2E validation with 100% success rate

## Quick Start

### Environment Setup

1. **Copy environment template**:
   ```bash
   cp .env.production.template .env.production
   ```

2. **Configure environment variables** in `.env.production`:
   ```bash
   # Update API URL for your environment
   VITE_API_URL=http://your-api-url:8000/api
   ```

### Development Mode

```bash
npm install
npm run dev
```

Access: http://localhost:5173

### Docker Development

```bash
# From project root
docker compose up frontend -d
```

Access: http://localhost:3000

### Production Build

```bash
npm run build
npm run preview
```

## Environment Configuration

### Required Environment Files

- `.env` - Development environment (tracked)
- `.env.production` - Production environment (**not tracked**)
- `.env.production.template` - Template for production setup

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API endpoint | `http://localhost:8000/api` |
| `VITE_NODE_ENV` | Environment mode | `development` |
| `VITE_ENABLE_DEVTOOLS` | React Query devtools | `true` (dev) |
| `VITE_API_TIMEOUT` | API request timeout | `10000` |

## Architecture

### Tech Stack

- **React 19** + **TypeScript** + **Vite 7**
- **TanStack Query** - Server state management
- **Tailwind CSS v4** - Styling with medical design tokens
- **Recharts** - Data visualizations
- **Framer Motion** - Animations

### Project Structure

```
src/
├── api/           # API clients and integration
├── components/    # Reusable UI components
├── contexts/      # React contexts (DualMode)
├── pages/         # Page components
├── services/      # Business logic
├── types/         # TypeScript definitions
└── utils/         # Helper functions
```

### Key Components

- **DualModeProvider** - Educational/Professional mode switching
- **MedicalKPIGrid** - Healthcare metrics dashboard
- **SentimentChart** - Medical sentiment visualization
- **TopicsChart** - Medical topic distribution
- **ErrorBoundary** - Medical context error handling

## Testing

```bash
# Unit tests
npm run test:unit

# Integration tests
npm run test:integration

# E2E validation
npm run test:e2e

# Coverage report
npm run test:coverage
```

## API Integration

### Endpoints Used

- `GET /api/analytics/dashboard` - Main metrics
- `GET /api/articles/?size=200` - Articles data
- `GET /api/analytics/topics/distribution` - Topic analysis
- `GET /api/analytics/geographic/distribution` - Geographic data

### Performance

All API calls optimized for < 2s response time with 106 articles dataset.

## Security

- **Environment files** properly excluded from version control
- **API keys** managed through environment variables
- **CORS** configured for development and production
- **Content Security Policy** headers in production

## Deployment

### Docker Production

```bash
# Build production image
docker build -f Dockerfile -t preventia-dashboard .

# Run with Nginx
docker run -p 80:80 preventia-dashboard
```

### Manual Production

```bash
npm run build
# Serve dist/ folder with your preferred web server
```

## Contributing

1. Follow existing code patterns and dual-mode architecture
2. Update tests for new components
3. Ensure environment template is updated for new variables
4. Test both Professional and Educational modes

## License

PreventIA Dashboard - Academic Research Project
