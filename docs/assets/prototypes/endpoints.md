## 🔌📑 Especificación detallada de Endpoints REST

*(Propuesta de contrato API v1 — backend Flask/FastAPI/Django REST)*

> Base URL: https://preventia.cfernandom.dev/api/v1
>
>
> **Formato estándar de respuesta**:
>
> ```json
> {
>   "status": "success",
>   "data": { … },
>   "meta": { "page": 1, "page_size": 20, "total": 234 }
> }
>
> ```
>

| # | Recurso | Método | Endpoint | Parámetros de consulta (query) | Descripción | Ejemplo de respuesta `data` |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Noticias (lista) | **GET** | `/news` | `page`, `page_size`, `country`, `language`, `topic`, `date_from`, `date_to`, `search` | Lista paginada de noticias procesadas. | `[ { "id": "abc123", "title": "...", "country": "CO", "language": "ES", "date": "2025-06-10", "topic": "Prevención", "tone": "Neutral" } ]` |
| 2 | Noticia (detalle) | **GET** | `/news/{id}` | – | Devuelve metadatos + resumen IA + enlace original. | `{ "id": "abc123", "summary": "...", "url": "https://..." }` |
| 3 | KPIs semanales | **GET** | `/stats/summary` | `week` | KPIs agregados de una semana (noticias totales, países, tonos). | `{ "week": 24, "total": 134, "countries": 11, "tones": { "positive": 28, ... } }` |
| 4 | Temas | **GET** | `/stats/topics` | `country`, `language`, `date_from`, `date_to` | Conteo por tema. | `{ "Prevención": 40, "Tratamiento": 34, ... }` |
| 5 | Tono | **GET** | `/stats/tones` | `country`, `language`, `date_from`, `date_to` | Distribución tonal (positivo, neutral, negativo). | `{
"status": "success",
"data": {
"positive": 40,
"neutral": 72,
"negative": 20
}
}` |
| 6 | Evolución tonal | **GET** | `/stats/tones/timeline` | `country`, `language`, `weeks=12` | Series de tiempo. | `{ "labels": [20,21,…], "positive": [25,26,…] }` |
| 7 | Cobertura geográfica | **GET** | `/stats/geo` | `date_from`, `date_to`, `topic` | Datos por país para el mapa. | `[{"country":"US","total":120,"tone":"Neutral","language":"EN"}]` |
| 8 | Descargar CSV | **GET** | `/export/news.csv` | mismos filtros de `/news` | Descarga CSV filtrado. | *Archivo* |
| 9 | Descargar XLSX | **GET** | `/export/news.xlsx` | mismos filtros de `/news` | Descarga Excel filtrado. | *Archivo* |
| 10 | Gráfico PNG | **GET** | `/export/charts/{chart_id}.png` | mismos filtros de sección | Devuelve imagen estática del gráfico. | *Content-Type: image/png* |
| 11 | Gráfico SVG | **GET** | `/export/charts/{chart_id}.svg` | – | Igual que 10 pero vectorial. | *Content-Type: image/svg+xml* |
| 12 | Generar PDF | **POST** | `/export/report` | Body JSON con `filters`, `include_ai_summaries: bool` | Crea informe; devuelve URL o blob. | `{ "report_id":"rpt789", "download_url":"/exports/rpt789.pdf" }` |
| 13 | Historial de exportaciones | **GET** | `/user/exports` | `limit=20` | Últimas descargas del usuario autenticado. | `[ { "file":"Informe_Sem24.pdf", "created_at":"..." } ]` |
| 14 | Autenticación | **POST** | `/auth/login` | Body `{ email, password }` | Devuelve JWT. | `{ "access_token":"...", "expires_in":3600 }` |
| 15 | Refresh token | **POST** | `/auth/refresh` | Header `Authorization: Bearer` | Renueva token. | `{ "access_token":"..." }` |

---

### 🔖 Convenciones y notas

- **Paginación**: `page` (1-n), `page_size` (10-100).
- **Filtros de fecha** en formato ISO `YYYY-MM-DD`.
- **Lenguaje**: `language=ES|EN` (códigos ISO-2).
- **Tono** se entrega en tres valores: `positive`, `neutral`, `negative`.
- Respuestas de error siguen formato:

    ```json
    { "status":"error", "message":"Descripción", "code":400 }

    ```


---

### 📌 Ejemplo de flujo Frontend → Backend

1. **DashboardHome** monta → `GET /stats/summary?week=24`
2. Usuario filtra idioma “ES” en Explorador Temático → `GET /stats/topics?language=ES&date_from=2025-06-01`
3. Al abrir mapa → `GET /stats/geo?date_from=2025-06-09&topic=Prevención`
4. Al hacer clic en “CSV” → `GET /export/news.csv?country=CO&language=ES`
5. Usuario genera PDF → `POST /export/report` con body:

    ```json
    {
      "filters": { "country":"CO", "language":"ES", "date_from":"2025-06-09" },
      "include_ai_summaries": true
    }

    ```


---
