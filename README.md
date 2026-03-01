# Geospatial Intelligence Tracker

Full-stack reference platform for geospatial intelligence operations with real-time air tracking, traffic cameras, OSINT defense overlays, anomaly alerts, and role-based access control.

## Capabilities Delivered

- Real-time aircraft tracking via ADS-B (OpenSky API with resilient sample fallback)
- Live route trail support and heatmap bins for traffic density
- Interactive 3D map integration point for CesiumJS / Mapbox / Google Maps
- Public traffic camera dashboard for legally available links
- Public defense activity visualization from OSINT-safe sources
- Alerting for unusual movement patterns + geofence entry events
- Multi-layer toggles (`Air`, `Land`, `Sea`, `Defense`)
- JWT authentication + role-based permissions (`admin`, `analyst`, `observer`)

---

## Architecture

```text
frontend (React + Vite)
  ├─ Layer toggles
  ├─ Map viewport integration shell (Cesium/Mapbox)
  ├─ Alerts dashboard
  └─ Camera monitoring grid

backend (FastAPI)
  ├─ ADS-B ingest service (OpenSky)
  ├─ OSINT data service (cameras + defense events + geofences)
  ├─ Alert engine (speed anomaly + geofence hit)
  └─ RBAC + JWT auth
```

## Quick Start

### Option A: Docker Compose

```bash
docker compose up --build
```

- API: `http://localhost:8000`
- Frontend: `http://localhost:5173`

### Option B: Run services manually

Backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

---

## API Highlights

### Auth

`POST /api/auth/token`

```json
{
  "username": "analyst",
  "password": "analyst123"
}
```

### Data endpoints

- `GET /api/aircraft`
- `GET /api/aircraft/routes`
- `GET /api/heatmap`
- `GET /api/cameras`
- `GET /api/defense`
- `GET /api/geofences`
- `GET /api/alerts`
- `GET /api/layers`

Roles required are enforced in each route.

---

## Security + Legal Notes

- Use only legally accessible public feeds.
- This reference implementation intentionally avoids non-public military data sources.
- Replace demo credentials and JWT secret before any deployment.
- Add proper audit logging and SOC controls for production.

## Next Enhancements

- Replace placeholder map component with full Cesium globe + 3D tiles
- Add Kafka/Redis stream pipeline for high-volume telemetry
- Persist historical tracks (PostGIS + TimescaleDB)
- Integrate STANAG-style geospatial symbology and mission workspaces
