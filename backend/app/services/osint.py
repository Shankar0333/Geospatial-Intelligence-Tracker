from datetime import datetime, timedelta

from app.models.schemas import CameraFeed, DefenseEvent, Geofence


class OSINTService:
    def list_cameras(self) -> list[CameraFeed]:
        return [
            CameraFeed(
                id="cam-nyc-dot-1",
                name="NYC DOT - Times Square",
                region="New York, US",
                stream_url="https://webcams.nyctmc.org/multiview2.php?cam=1",
                source="NYC DOT",
            ),
            CameraFeed(
                id="cam-london-tfl-12",
                name="TfL Traffic Cam - Victoria",
                region="London, UK",
                stream_url="https://trafficcameras.uk/city/london/",
                source="Transport for London",
            ),
        ]

    def list_defense_events(self) -> list[DefenseEvent]:
        now = datetime.utcnow()
        return [
            DefenseEvent(
                id="def-001",
                category="Naval",
                title="Publicly announced joint naval exercise",
                description="Maritime drill sourced from official ministry press release.",
                latitude=20.5,
                longitude=118.3,
                source_url="https://www.navy.mil/",
                occurred_at=now - timedelta(hours=5),
            ),
            DefenseEvent(
                id="def-002",
                category="Air Defense",
                title="NOTAM-linked training corridor activation",
                description="Temporary restricted airspace published through civil NOTAM feed.",
                latitude=36.2,
                longitude=-115.1,
                source_url="https://www.faa.gov/air_traffic/publications/notices",
                occurred_at=now - timedelta(hours=2),
            ),
        ]

    def list_geofences(self) -> list[Geofence]:
        return [
            Geofence(
                id="geo-jfk",
                name="JFK Class B Airspace",
                geometry={"bbox": [-74.3, 40.3, -72.9, 41.0]},
                alert_on_entry=True,
            ),
            Geofence(
                id="geo-lhr",
                name="Heathrow CTR",
                geometry={"bbox": [-0.9, 51.2, 0.2, 51.7]},
                alert_on_entry=True,
            ),
        ]
