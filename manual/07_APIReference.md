# 7. Referencia de API

## Índice del Contenido

1. [Información General](#información-general)
2. [Autenticación](#autenticación)
3. [Endpoints de Artículos](#endpoints-de-artículos)
4. [Endpoints de Fuentes](#endpoints-de-fuentes)
5. [Endpoints de Analytics](#endpoints-de-analytics)
6. [Endpoints de Administración](#endpoints-de-administración)
7. [Modelos de Datos](#modelos-de-datos)
8. [Códigos de Error](#códigos-de-error)
9. [Ejemplos de Uso](#ejemplos-de-uso)

## Información General

### URL Base
```
http://localhost:8000
```

### Versiones de API
- **v1**: `/api/v1/` (legacy, mantiene compatibilidad)
- **Actual**: `/api/` (versión principal)

### Formato de Respuesta
Todas las respuestas están en formato JSON con la siguiente estructura:

```json
{
  "data": { ... },
  "message": "string (opcional)",
  "status": "success|error",
  "timestamp": "2025-07-29T12:00:00Z"
}
```

### Rate Limiting
- **Límite por defecto**: 100 requests por minuto
- **Headers de respuesta**:
  - `X-RateLimit-Limit`: Límite total
  - `X-RateLimit-Remaining`: Requests restantes
  - `X-RateLimit-Reset`: Timestamp de reset

## Autenticación

### Login
Obtener token de acceso para autenticación.

```http
POST /api/auth/login
Content-Type: application/x-www-form-urlencoded

username=admin&password=admin123
```

**Respuesta exitosa:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

### Uso del Token
Include el token en el header Authorization:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Endpoints de Artículos

### Listar Artículos

```http
GET /api/articles/
```

**Parámetros de consulta:**
- `skip` (int): Offset para paginación (default: 0)
- `limit` (int): Número de resultados (default: 100, max: 1000)
- `source_id` (int): Filtrar por fuente específica
- `sentiment` (string): Filtrar por sentimiento (positive, negative, neutral)
- `topic` (string): Filtrar por categoría de tópico
- `date_from` (string): Fecha inicio (ISO 8601)
- `date_to` (string): Fecha fin (ISO 8601)

**Ejemplo de respuesta:**
```json
{
  "data": {
    "articles": [
      {
        "id": 1,
        "title": "Nuevos avances en detección temprana",
        "content": "Los investigadores han desarrollado...",
        "url": "https://example.com/article1",
        "published_at": "2025-07-29T10:00:00Z",
        "source": {
          "id": 1,
          "name": "Instituto Nacional del Cáncer",
          "base_url": "https://cancer.gov"
        },
        "sentiment": {
          "score": 0.75,
          "label": "positive",
          "confidence": 0.89
        },
        "topic": {
          "category": "diagnosis",
          "confidence": 0.92
        },
        "processing_status": "completed",
        "word_count": 1248,
        "created_at": "2025-07-29T10:05:00Z"
      }
    ],
    "total": 1,
    "skip": 0,
    "limit": 100
  },
  "status": "success"
}
```

### Obtener Artículo por ID

```http
GET /api/articles/{article_id}
```

**Parámetros de ruta:**
- `article_id` (int): ID del artículo

### Buscar Artículos

```http
GET /api/articles/search/?q={query}
```

**Parámetros de consulta:**
- `q` (string): Término de búsqueda
- `limit` (int): Número de resultados (default: 50)
- `search_in` (string): Campos a buscar (title, content, both)

### Estadísticas de Artículos

```http
GET /api/articles/stats/summary
```

**Respuesta:**
```json
{
  "data": {
    "total_articles": 121,
    "articles_last_7_days": 15,
    "articles_by_sentiment": {
      "positive": 65,
      "neutral": 38,
      "negative": 18
    },
    "articles_by_topic": {
      "prevention": 35,
      "treatment": 28,
      "diagnosis": 22,
      "research": 20,
      "testimonials": 16
    },
    "avg_processing_time": 2.3
  },
  "status": "success"
}
```

## Endpoints de Fuentes

### Listar Fuentes de Noticias

```http
GET /api/sources/
```

**Parámetros de consulta:**
- `skip` (int): Offset para paginación
- `limit` (int): Número de resultados
- `is_active` (bool): Filtrar por estado activo
- `validation_status` (string): pending, validated, failed
- `country` (string): Filtrar por país

**Ejemplo de respuesta:**
```json
{
  "data": {
    "sources": [
      {
        "id": 1,
        "name": "Instituto Nacional del Cáncer",
        "base_url": "https://cancer.gov/espanol",
        "language": "es",
        "country": "Estados Unidos",
        "is_active": true,
        "validation_status": "validated",
        "compliance_score": 0.95,
        "articles_count": 45,
        "last_scraped_at": "2025-07-29T08:00:00Z",
        "created_at": "2025-07-15T10:00:00Z"
      }
    ],
    "total": 8,
    "skip": 0,
    "limit": 100
  },
  "status": "success"
}
```

### Crear Nueva Fuente

```http
POST /api/sources/
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Nueva Fuente Médica",
  "base_url": "https://nuevafuente.com",
  "language": "es",
  "country": "España",
  "fair_use_basis": "Información médica educativa sin fines comerciales"
}
```

### Actualizar Fuente

```http
PUT /api/sources/{source_id}
Authorization: Bearer {token}
```

### Eliminar Fuente

```http
DELETE /api/sources/{source_id}
Authorization: Bearer {token}
```

### Validar Compliance de Fuente

```http
POST /api/sources/{source_id}/validate
Authorization: Bearer {token}
```

**Respuesta:**
```json
{
  "data": {
    "validation_results": {
      "robots_txt": {
        "status": "passed",
        "message": "robots.txt allows scraping with 2s delay"
      },
      "fair_use": {
        "status": "passed",
        "message": "Fair use basis documented"
      },
      "terms_of_service": {
        "status": "warning",
        "message": "Terms not explicitly reviewed"
      }
    },
    "compliance_score": 0.88,
    "overall_status": "passed"
  },
  "status": "success"
}
```

## Endpoints de Analytics

### Dashboard Principal

```http
GET /api/analytics/dashboard
Authorization: Bearer {token}
```

**Respuesta:**
```json
{
  "data": {
    "summary": {
      "total_articles": 121,
      "active_sources": 8,
      "avg_sentiment": 0.42,
      "processing_rate": "95.8%"
    },
    "sentiment_distribution": {
      "positive": 53.7,
      "neutral": 31.4,
      "negative": 14.9
    },
    "topic_distribution": {
      "prevention": 28.9,
      "treatment": 23.1,
      "diagnosis": 18.2,
      "research": 16.5,
      "testimonials": 13.3
    },
    "recent_articles": [
      {
        "id": 121,
        "title": "Último artículo procesado...",
        "sentiment_label": "positive",
        "topic_category": "prevention"
      }
    ]
  },
  "status": "success"
}
```

### Tendencias de Sentimiento

```http
GET /api/analytics/sentiment/trends
```

**Parámetros de consulta:**
- `days` (int): Período en días (default: 30)
- `granularity` (string): daily, weekly, monthly

### Distribución Geográfica

```http
GET /api/analytics/geographic/distribution
```

### Distribución de Tópicos

```http
GET /api/analytics/topics/distribution
```

**Respuesta:**
```json
{
  "data": {
    "topics": [
      {
        "category": "prevention",
        "count": 35,
        "percentage": 28.9,
        "avg_sentiment": 0.68,
        "trend": "up"
      },
      {
        "category": "treatment",
        "count": 28,
        "percentage": 23.1,
        "avg_sentiment": 0.12,
        "trend": "stable"
      }
    ],
    "total_articles": 121
  },
  "status": "success"
}
```

### Performance de Fuentes

```http
GET /api/analytics/sources/performance
```

### Tendencias Semanales

```http
GET /api/analytics/trends/weekly
```

## Endpoints de Administración

### Health Check

```http
GET /health
```

**Respuesta:**
```json
{
  "status": "healthy",
  "database": "connected",
  "articles_count": 121,
  "version": "1.0.0",
  "timestamp": "2025-07-29T12:00:00Z"
}
```

### Información del Sistema

```http
GET /api/system/info
Authorization: Bearer {token}
```

### Logs del Sistema

```http
GET /api/system/logs
Authorization: Bearer {token}
```

**Parámetros de consulta:**
- `level` (string): DEBUG, INFO, WARNING, ERROR
- `service` (string): api, scraper, nlp
- `limit` (int): Número de entradas

## Modelos de Datos

### Article
```typescript
interface Article {
  id: number;
  title: string;
  content: string;
  url: string;
  published_at: string;
  source_id: number;
  source?: Source;
  processing_status: 'pending' | 'processing' | 'completed' | 'failed';
  sentiment_score?: number;
  sentiment_label?: 'positive' | 'neutral' | 'negative';
  topic_category?: string;
  topic_confidence?: number;
  content_hash: string;
  word_count: number;
  summary?: string;
  metadata?: Record<string, any>;
  created_at: string;
  updated_at: string;
}
```

### Source
```typescript
interface Source {
  id: number;
  name: string;
  base_url: string;
  language: string;
  country: string;
  extractor_class?: string;
  is_active: boolean;
  validation_status: 'pending' | 'validated' | 'failed';
  validation_error?: string;
  last_validation_at?: string;
  robots_txt_url?: string;
  crawl_delay_seconds: number;
  scraping_allowed?: boolean;
  fair_use_basis?: string;
  compliance_score?: number;
  last_compliance_check?: string;
  created_at: string;
  updated_at: string;
}
```

### SentimentAnalysis
```typescript
interface SentimentAnalysis {
  article_id: number;
  sentiment_score: number;
  sentiment_label: 'positive' | 'neutral' | 'negative';
  confidence_score: number;
  analyzed_at: string;
}
```

### TopicClassification
```typescript
interface TopicClassification {
  article_id: number;
  topic_category: string;
  confidence_score: number;
  classified_at: string;
}
```

## Códigos de Error

### Códigos HTTP
- `200` - OK
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Unprocessable Entity
- `429` - Too Many Requests
- `500` - Internal Server Error

### Errores de Aplicación
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "URL inválida para fuente de noticias",
    "details": {
      "field": "base_url",
      "value": "invalid-url"
    }
  },
  "status": "error",
  "timestamp": "2025-07-29T12:00:00Z"
}
```

**Códigos de error comunes:**
- `VALIDATION_ERROR` - Error de validación de datos
- `AUTH_REQUIRED` - Autenticación requerida
- `INSUFFICIENT_PERMISSIONS` - Permisos insuficientes
- `RESOURCE_NOT_FOUND` - Recurso no encontrado
- `RATE_LIMIT_EXCEEDED` - Límite de tasa excedido
- `PROCESSING_ERROR` - Error en procesamiento
- `COMPLIANCE_ERROR` - Error de compliance legal

## Ejemplos de Uso

### Flujo Completo: Agregar Fuente y Analizar Artículos

1. **Autenticarse:**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

2. **Crear nueva fuente:**
```bash
curl -X POST http://localhost:8000/api/sources/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Fundación Cáncer España",
    "base_url": "https://fundacioncancer.es",
    "language": "es",
    "country": "España",
    "fair_use_basis": "Información educativa médica"
  }'
```

3. **Validar compliance:**
```bash
curl -X POST http://localhost:8000/api/sources/1/validate \
  -H "Authorization: Bearer $TOKEN"
```

4. **Buscar artículos recientes:**
```bash
curl "http://localhost:8000/api/articles/?date_from=2025-07-25&limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

5. **Analizar tendencias:**
```bash
curl "http://localhost:8000/api/analytics/sentiment/trends?days=7" \
  -H "Authorization: Bearer $TOKEN"
```

### Ejemplo JavaScript/TypeScript

```typescript
class PreventiaAPI {
  private baseUrl = 'http://localhost:8000';
  private token: string | null = null;

  async login(username: string, password: string) {
    const response = await fetch(`${this.baseUrl}/api/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: `username=${username}&password=${password}`
    });

    const data = await response.json();
    if (data.access_token) {
      this.token = data.access_token;
    }
    return data;
  }

  async getArticles(params: {
    skip?: number;
    limit?: number;
    source_id?: number;
    sentiment?: string;
  } = {}) {
    const queryParams = new URLSearchParams(params as any);

    const response = await fetch(`${this.baseUrl}/api/articles/?${queryParams}`, {
      headers: {
        'Authorization': `Bearer ${this.token}`
      }
    });

    return response.json();
  }

  async getDashboard() {
    const response = await fetch(`${this.baseUrl}/api/analytics/dashboard`, {
      headers: {
        'Authorization': `Bearer ${this.token}`
      }
    });

    return response.json();
  }
}

// Uso
const api = new PreventiaAPI();
await api.login('admin', 'admin123');
const articles = await api.getArticles({ limit: 10, sentiment: 'positive' });
const dashboard = await api.getDashboard();
```

### Ejemplo Python

```python
import requests
from typing import Dict, Optional

class PreventiaAPI:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.token: Optional[str] = None
        self.session = requests.Session()

    def login(self, username: str, password: str) -> Dict:
        response = self.session.post(
            f"{self.base_url}/api/auth/login",
            data={"username": username, "password": password}
        )
        data = response.json()

        if "access_token" in data:
            self.token = data["access_token"]
            self.session.headers.update({
                "Authorization": f"Bearer {self.token}"
            })

        return data

    def get_articles(self, **params) -> Dict:
        response = self.session.get(
            f"{self.base_url}/api/articles/",
            params=params
        )
        return response.json()

    def create_source(self, source_data: Dict) -> Dict:
        response = self.session.post(
            f"{self.base_url}/api/sources/",
            json=source_data
        )
        return response.json()

    def get_analytics_dashboard(self) -> Dict:
        response = self.session.get(
            f"{self.base_url}/api/analytics/dashboard"
        )
        return response.json()

# Uso
api = PreventiaAPI()
api.login("admin", "admin123")

# Obtener artículos positivos
articles = api.get_articles(sentiment="positive", limit=5)

# Crear nueva fuente
new_source = api.create_source({
    "name": "Ejemplo Fuente",
    "base_url": "https://ejemplo.com",
    "language": "es",
    "country": "España"
})

# Ver dashboard
dashboard = api.get_analytics_dashboard()
```

---

## Notas Importantes

### Seguridad
- Todos los endpoints administrativos requieren autenticación
- Los tokens JWT expiran en 24 horas por defecto
- Implementar HTTPS en producción
- Validar y sanitizar todas las entradas

### Performance
- Usar paginación para listados grandes
- Implementar cache para consultas frecuentes
- Considerar rate limiting en producción
- Optimizar consultas de analytics para datasets grandes

### Compliance
- Respetar robots.txt de las fuentes
- Documentar base legal para scraping
- Implementar crawl delays apropiados
- Monitorear compliance scores regularmente
