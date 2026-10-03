# API Specification — Mumbai Local Train Delay Tracker

Base URL: `https://mumbai-local-delay-tracker.vercel.app/api`

## Endpoints

### 1. Get All Lines Status
- **URL:** `/status`
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

### 2. Get Station-Specific Delays
- **URL:** `/station/{station_code}`
- **Method:** `GET`
- **Description:** Retrieves live train arrival/departure delay logs for a specific railway station.

### 3. Submit Crowd-Sourced Delay Report
- **URL:** `/report`
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
