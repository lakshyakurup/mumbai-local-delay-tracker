# API Specification — Mumbai Local Train Delay Tracker

Base URL: `https://<render-service>/api/v2`

Authentication: read endpoints are public behind CORS. The scraper trigger accepts `Authorization: Bearer <SCRAPER_TOKEN>` when `SCRAPER_TOKEN` is configured.

## Endpoints

### 1. Get All Lines Status
- **URL:** `/lines/status`
- **Method:** `GET`
- **Description:** Returns the real-time operational status, average delay in minutes, and major disruptions for Central, Western, and Harbour lines.
- **Response Example:**
```json
{
  "timestamp": "2026-10-03T10:30:00Z",
  "lines": [
    {"name": "Central", "status": "Delayed", "avg_delay_mins": 15, "disruption": "Signal failure near Kalyan"},
    {"name": "Western", "status": "Running Smooth", "avg_delay_mins": 3, "disruption": null},
    {"name": "Harbour", "status": "Moderate Delays", "avg_delay_mins": 8, "disruption": "Track maintenance"}
  ]
}
```

### 2. Get Delay Records
- **URL:** `/delays?line=central&hours=24&limit=100`
- **Method:** `GET`
- **Response:** `DelayRecord[]` with `line`, `station`, `direction`, `delay_minutes`, `severity`, `source`, and `recorded_at`.

### 3. Create or Delete Delay Record
- **POST:** `/delays` with `{line, station, direction, delay_minutes, announcement?, source?}`.
- **DELETE:** `/delays/{record_id}`.

### 4. Get Station-Specific Delays
- **URL:** `/lines/{line}/stations`
- **Method:** `GET`
- **Description:** Retrieves live train arrival/departure delay logs for a specific railway station.

### 5. Statistical Aggregation
- **URL:** `/stats/summary?hours=24` and `/stats/trends?days=7`
- **Method:** `GET`
- **Description:** Returns network average, per-line averages, peak hour, and daily trend buckets.

### 6. Scraper Trigger
- **URL:** `/scraper/run`
- **Method:** `POST`
- **Description:** Fetches the configured source, parses valid line updates, persists records, and refreshes line statuses.

### 7. Submit Crowd-Sourced Delay Report
- **URL:** `/delays`
- **Method:** `POST`
- **Payload:**
```json
{
  "line": "Western",
  "station": "Andheri",
  "delay_minutes": 12,
  "description": "Slow movement towards Churchgate"
}
```

### Health and observability
- `GET /health` probes database connectivity and returns `ok` or `degraded`.
- `GET /metrics` exposes Prometheus HTTP metrics.
- Responses are rate limited using `RATE_LIMIT` (default `120/minute`).
