from __future__ import annotations

from collections import deque
from datetime import datetime, timedelta
from statistics import mean

from app.models.schemas import Alert, AircraftState, Geofence


class AlertService:
    def __init__(self) -> None:
        self._alerts: deque[Alert] = deque(maxlen=2000)
        self._speed_history: dict[str, deque[float]] = {}
        self._last_fired: dict[str, datetime] = {}

    def _can_emit(self, alert_key: str, cooldown_s: int = 90) -> bool:
        now = datetime.utcnow()
        previous = self._last_fired.get(alert_key)
        if previous and now - previous < timedelta(seconds=cooldown_s):
            return False
        self._last_fired[alert_key] = now
        return True

    def evaluate_aircraft(self, states: list[AircraftState], geofences: list[Geofence]) -> list[Alert]:
        new_alerts: list[Alert] = []

        for state in states:
            if state.velocity_ms is not None:
                history = self._speed_history.setdefault(state.icao24, deque(maxlen=30))
                history.append(state.velocity_ms)
                baseline = mean(history) if len(history) > 1 else state.velocity_ms
                if len(history) > 8 and state.velocity_ms > baseline * 1.45 and self._can_emit(f"spd:{state.icao24}"):
                    new_alerts.append(
                        Alert(
                            id=f"spd-{state.icao24}-{int(datetime.utcnow().timestamp())}",
                            severity="medium",
                            title="Anomalous aircraft speed",
                            detail=f"{state.callsign or state.icao24} exceeded expected speed envelope",
                            entity_id=state.icao24,
                        )
                    )

            if state.vertical_rate_ms is not None and abs(state.vertical_rate_ms) > 20 and self._can_emit(f"vrt:{state.icao24}"):
                new_alerts.append(
                    Alert(
                        id=f"vrt-{state.icao24}-{int(datetime.utcnow().timestamp())}",
                        severity="medium",
                        title="Unusual climb/descent rate",
                        detail=f"{state.callsign or state.icao24} reported aggressive vertical rate",
                        entity_id=state.icao24,
                    )
                )

            for geofence in geofences:
                bbox = geofence.geometry.get("bbox")
                if not bbox or not geofence.alert_on_entry:
                    continue
                min_lon, min_lat, max_lon, max_lat = bbox
                inside = min_lat <= state.latitude <= max_lat and min_lon <= state.longitude <= max_lon
                if inside and self._can_emit(f"geo:{geofence.id}:{state.icao24}"):
                    new_alerts.append(
                        Alert(
                            id=f"geo-{geofence.id}-{state.icao24}-{int(datetime.utcnow().timestamp())}",
                            severity="high",
                            title="Geofence entry detected",
                            detail=f"{state.callsign or state.icao24} entered {geofence.name}",
                            entity_id=state.icao24,
                        )
                    )

        for alert in new_alerts:
            self._alerts.appendleft(alert)

        return new_alerts

    def list_alerts(self, limit: int = 100) -> list[Alert]:
        return list(self._alerts)[:limit]
