from datetime import datetime, timedelta

from app.models.schemas import AirspaceBoundary, CameraFeed, DefenseEvent, Geofence, LandEvent, SeaVessel


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
            CameraFeed(
                id="cam-caltrans-sf-3",
                name="Caltrans - US-101 @ San Francisco",
                region="California, US",
                stream_url="https://cwwp2.dot.ca.gov/vm/iframemap.htm",
                source="Caltrans",
            ),
        ]

    def list_sea_vessels(self) -> list[SeaVessel]:
        return [
            SeaVessel(
                id="sea-001",
                name="PACIFIC TRADER",
                vessel_type="Cargo",
                latitude=1.3,
                longitude=103.7,
                speed_knots=14.2,
                heading_deg=78,
                source="Public AIS Aggregator",
            ),
            SeaVessel(
                id="sea-002",
                name="ATLANTIC AURORA",
                vessel_type="Tanker",
                latitude=25.8,
                longitude=-80.1,
                speed_knots=11.6,
                heading_deg=22,
                source="Public AIS Aggregator",
            ),
        ]

    def list_land_events(self) -> list[LandEvent]:
        now = datetime.utcnow()
        return [
            LandEvent(
                id="land-001",
                title="Highway convoy restriction advisory",
                category="Logistics",
                latitude=34.04,
                longitude=-118.27,
                source_url="https://dot.ca.gov",
                occurred_at=now - timedelta(hours=3),
            ),
            LandEvent(
                id="land-002",
                title="Rail corridor maintenance closure",
                category="Infrastructure",
                latitude=51.51,
                longitude=-0.12,
                source_url="https://tfl.gov.uk",
                occurred_at=now - timedelta(hours=2),
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
            DefenseEvent(
                id="def-003",
                category="Ground",
                title="Defense logistics convoy drill notice",
                description="Movement announcement surfaced through official regional bulletin.",
                latitude=51.34,
                longitude=-0.41,
                source_url="https://www.gov.uk/government/organisations/ministry-of-defence",
                occurred_at=now - timedelta(hours=1),
            ),
        ]

    def list_geofences(self) -> list[Geofence]:
        return [
            Geofence(id="geo-jfk", name="JFK Class B Airspace", geometry={"bbox": [-74.3, 40.3, -72.9, 41.0]}, alert_on_entry=True),
            Geofence(id="geo-lhr", name="Heathrow CTR", geometry={"bbox": [-0.9, 51.2, 0.2, 51.7]}, alert_on_entry=True),
            Geofence(id="geo-sin", name="Singapore FIR Segment", geometry={"bbox": [103.2, 1.0, 104.4, 1.9]}, alert_on_entry=True),
        ]

    def list_airspace_boundaries(self) -> list[AirspaceBoundary]:
        return [
            AirspaceBoundary(
                id="asp-jfk-b",
                name="JFK Terminal Zone",
                boundary_type="controlled",
                coordinates=[[-74.3, 40.3], [-72.9, 40.3], [-72.9, 41.0], [-74.3, 41.0], [-74.3, 40.3]],
            ),
            AirspaceBoundary(
                id="asp-lhr-ctr",
                name="London Heathrow CTR",
                boundary_type="controlled",
                coordinates=[[-0.9, 51.2], [0.2, 51.2], [0.2, 51.7], [-0.9, 51.7], [-0.9, 51.2]],
            ),
        ]
