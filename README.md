# Geospatial Intelligence Tracker

Advanced full-stack geospatial intelligence platform for multi-domain situational awareness. The project combines live ADS-B aviation telemetry, public traffic cameras, public OSINT defense activity, density analytics, geofencing alerts, and RBAC-secured APIs.

## What is implemented

- **Real-time aircraft tracking** from OpenSky ADS-B public states (with resilient fallback simulation data).
- **Live route history** per aircraft and periodic websocket push stream (`/api/ws/air`).
- **Traffic density analytics** and hotspot bins for heatmap rendering.
- **Public camera monitoring** from legal/public traffic feed directories.
- **Public defense activity overlay** from OSINT-safe, official/public sources.
- **Geofencing + airspace boundary overlays** via API structures.
- **Alerting engine** with anomaly detection:
  - speed envelope breaches,
  - unusual climb/descent rates,
  - geofence entry detection.
- **Role-based access control** (`admin`, `analyst`, `observer`) using JWT.
- **Multi-layer toggles** (`Air`, `Land`, `Sea`, `Defense`) in frontend state model.

---

## Architecture

```text
frontend (React + TypeScript + Vite)
  ├─ Authentication screen
  ├─ Operational KPI cards
  ├─ Layer toggles
  ├─ Map command viewport integration shell
  ├─ Live alert stream panel
  └─ Public traffic camera monitor panel

backend (FastAPI)
  ├─ Auth/RBAC module
  ├─ Aircraft ingest + route + heatmap service
  ├─ Alert intelligence service
  ├─ OSINT feeds service
  └─ Runtime scheduler for continuous refresh
```

---

## Run locally

### Docker compose

```bash
docker compose up --build
```

- API: `http://localhost:8000`
- Frontend: `http://localhost:5173`

### Manual

Backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

---

## API reference (high level)

### Authentication
- `POST /api/auth/token`

### Air picture
- `GET /api/aircraft`
- `GET /api/aircraft/routes`
- `GET /api/heatmap`
- `GET /api/analytics/traffic-density`
- `WS  /api/ws/air`

### OSINT overlays
- `GET /api/cameras`
- `GET /api/defense`
- `GET /api/geofences`
- `GET /api/airspace/boundaries`

### Alerts + layer control
- `GET /api/alerts`
- `GET /api/layers`

---

## Frontend map integration notes

`MapViewport` is an integration shell so you can plug in Cesium/Mapbox/Google layers directly:

- aircraft icon entities and heading vectors
- route polylines by `icao24`
- heatmap layer from `/api/heatmap`
- geofence polygons + airspace boundaries
- defense activity markers

---

## Security and legal guidance

- Use only lawful/public camera sources and official public notices.
- Do not ingest restricted military systems or classified data.
- Rotate demo secrets and credentials before any deployment.
- Add audit logs, SIEM forwarding, and policy controls for production.
