from __future__ import annotations

from collections import deque
from datetime import datetime
from statistics import mean

from app.models.schemas import Alert, AircraftState, Geofence


class AlertService:
    def __init__(self) -> None:
        self._alerts: deque[Alert] = deque(maxlen=1000)
        self._speed_history: dict[str, deque[float]] = {}

    def evaluate_aircraft(self, states: list[AircraftState], geofences: list[Geofence]) -> list[Alert]:
        new_alerts: list[Alert] = []

        for state in states:
            if state.velocity_ms is not None:
                history = self._speed_history.setdefault(state.icao24, deque(maxlen=25))
                history.append(state.velocity_ms)
                if len(history) > 8 and state.velocity_ms > mean(history) * 1.5:
                    new_alerts.append(
                        Alert(
                            id=f"spd-{state.icao24}-{int(datetime.utcnow().timestamp())}",
                            severity="medium",
                            title="Anomalous aircraft speed",
                            detail=f"{state.callsign or state.icao24} exceeded expected speed envelope",
                            entity_id=state.icao24,
                        )
                    )

            for geofence in geofences:
                bbox = geofence.geometry.get("bbox")
                if not bbox:
                    continue
                min_lon, min_lat, max_lon, max_lat = bbox
                if min_lat <= state.latitude <= max_lat and min_lon <= state.longitude <= max_lon:
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

    def list_alerts(self) -> list[Alert]:
        return list(self._alerts)
