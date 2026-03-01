from __future__ import annotations

import random
from collections import defaultdict
from datetime import datetime

import httpx

from app.core.config import settings
from app.models.schemas import AircraftRoutePoint, AircraftState, HeatmapBin, TrafficDensitySnapshot


class AircraftService:
    def __init__(self) -> None:
        self._states: dict[str, AircraftState] = {}
        self._routes: dict[str, list[AircraftRoutePoint]] = defaultdict(list)

    async def refresh(self) -> None:
        rows = await self._fetch_opensky_rows()
        if not rows:
            rows = self._generate_sample_rows()

        for row in rows:
            state = AircraftState(
                icao24=row[0],
                callsign=(row[1] or "").strip() or None,
                origin_country=row[2],
                longitude=row[5],
                latitude=row[6],
                altitude_m=row[7],
                velocity_ms=row[9],
                heading_deg=row[10],
                vertical_rate_ms=row[11],
            )
            self._states[state.icao24] = state
            self._routes[state.icao24].append(
                AircraftRoutePoint(
                    icao24=state.icao24,
                    latitude=state.latitude,
                    longitude=state.longitude,
                    altitude_m=state.altitude_m,
                    observed_at=datetime.utcnow(),
                )
            )
            self._routes[state.icao24] = self._routes[state.icao24][-120:]

    async def _fetch_opensky_rows(self) -> list[list] | None:
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                response = await client.get(settings.opensky_url)
                response.raise_for_status()
                data = response.json()
                states = data.get("states") or []
                return [s for s in states if s[5] is not None and s[6] is not None]
        except Exception:
            return None

    def _generate_sample_rows(self) -> list[list]:
        base = [
            ["abc123", "GEO101", "US", None, None, -73.78, 40.64, 8900, False, 225, 80, 4, None, 9000, None, False, 0],
            ["def456", "GEO202", "UK", None, None, 2.55, 49.01, 10200, False, 240, 110, -2, None, 10300, None, False, 0],
            ["ghi789", "GEO303", "JP", None, None, 139.77, 35.55, 7600, False, 210, 35, 0, None, 7600, None, False, 0],
            ["mno321", "GEO404", "DE", None, None, 13.41, 52.52, 11200, False, 258, 265, 2, None, 11300, None, False, 0],
        ]
        for row in base:
            row[5] += random.uniform(-0.7, 0.7)
            row[6] += random.uniform(-0.7, 0.7)
            row[10] = (row[10] + random.uniform(-10, 10)) % 360
            row[9] = max(90, row[9] + random.uniform(-20, 20))
        return base

    def list_states(self) -> list[AircraftState]:
        return sorted(self._states.values(), key=lambda s: s.updated_at, reverse=True)

    def get_routes(self, icao24: str | None = None) -> dict[str, list[AircraftRoutePoint]]:
        if icao24:
            return {icao24: self._routes.get(icao24, [])}
        return self._routes

    def build_heatmap(self, precision: int = 1) -> list[HeatmapBin]:
        bins: dict[tuple[float, float], int] = defaultdict(int)
        for state in self._states.values():
            lat = round(state.latitude, precision)
            lon = round(state.longitude, precision)
            bins[(lat, lon)] += 1
        return sorted(
            [HeatmapBin(latitude=lat, longitude=lon, count=count) for (lat, lon), count in bins.items()],
            key=lambda h: h.count,
            reverse=True,
        )

    def density_snapshot(self, top_n: int = 10) -> TrafficDensitySnapshot:
        heatmap = self.build_heatmap()
        return TrafficDensitySnapshot(total_aircraft=len(self._states), hotspots=heatmap[:top_n])
