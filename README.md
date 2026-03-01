# Geospatial Intelligence Tracker

A deeper, operations-focused full-stack geospatial intelligence platform for multi-domain monitoring.

## Advanced capabilities

- Live ADS-B aircraft ingest with route history and heatmap bins.
- WebSocket air picture stream secured with JWT token query validation.
- OSINT feeds for defense, traffic cameras, land events, and sea-vessel activity.
- Geofence + airspace boundary APIs for overlay rendering.
- Alert intelligence engine with:
  - speed anomaly detection,
  - vertical-rate anomaly detection,
  - geofence entry detection,
  - cooldown suppression to reduce duplicate alert noise.
- Risk scoring endpoint combining air alerts + defense + land + sea indicators.
- Role-based access control (`admin`, `analyst`, `observer`).
- Multi-layer frontend dashboard for Air/Land/Sea/Defense.

## API additions

- `GET /api/sea`
- `GET /api/land`
- `GET /api/analytics/risk`
- `WS /api/ws/air?token=<jwt>`

## Run

```bash
docker compose up --build
```

## Notes

- Keep data sources public and legally accessible.
- Replace demo credentials and JWT secret before production deployment.
