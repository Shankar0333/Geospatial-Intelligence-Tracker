from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class LayerType(str, Enum):
    air = "air"
    land = "land"
    sea = "sea"
    defense = "defense"


class Role(str, Enum):
    admin = "admin"
    analyst = "analyst"
    observer = "observer"


class AircraftState(BaseModel):
    icao24: str
    callsign: str | None = None
    origin_country: str | None = None
    longitude: float
    latitude: float
    altitude_m: float | None = None
    velocity_ms: float | None = None
    heading_deg: float | None = None
    vertical_rate_ms: float | None = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class AircraftRoutePoint(BaseModel):
    icao24: str
    latitude: float
    longitude: float
    altitude_m: float | None = None
    observed_at: datetime


class HeatmapBin(BaseModel):
    latitude: float
    longitude: float
    count: int


class CameraFeed(BaseModel):
    id: str
    name: str
    region: str
    stream_url: str
    source: str
    status: str = "online"


class DefenseEvent(BaseModel):
    id: str
    category: str
    title: str
    description: str
    latitude: float
    longitude: float
    source_url: str
    occurred_at: datetime


class Geofence(BaseModel):
    id: str
    name: str
    geometry: dict[str, Any]
    alert_on_entry: bool = True
    alert_on_exit: bool = False


class Alert(BaseModel):
    id: str
    severity: str
    title: str
    detail: str
    entity_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class TokenRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class User(BaseModel):
    username: str
    role: Role
