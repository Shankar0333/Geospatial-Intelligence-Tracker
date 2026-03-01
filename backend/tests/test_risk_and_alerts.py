import unittest

from app.models.schemas import AircraftState, Geofence
from app.services.alerts import AlertService
from app.services.risk import RiskService


class AlertServiceTests(unittest.TestCase):
    def test_geofence_alert_emits(self):
        svc = AlertService()
        states = [
            AircraftState(
                icao24="abc123",
                latitude=40.7,
                longitude=-73.9,
                velocity_ms=250,
                vertical_rate_ms=0,
            )
        ]
        geofences = [Geofence(id="g1", name="Test", geometry={"bbox": [-74.5, 40.0, -73.0, 41.0]}, alert_on_entry=True)]
        alerts = svc.evaluate_aircraft(states, geofences)
        self.assertTrue(any(a.title == "Geofence entry detected" for a in alerts))


class RiskServiceTests(unittest.TestCase):
    def test_risk_high_when_many_alerts(self):
        svc = RiskService()
        risk = svc.assess(alerts_count=30, defense_events=[object(), object()], sea_vessels=[object(), object()], land_events=[object(), object()])
        self.assertIn(risk.level, {"medium", "high"})
        self.assertGreaterEqual(risk.overall_score, 40)


if __name__ == "__main__":
    unittest.main()
