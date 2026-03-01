import asyncio

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, status

from app.core.auth import authenticate_user, create_access_token, decode_token, require_roles
from app.models.schemas import Role, TokenRequest, TokenResponse, User
from app.services.runtime import runtime

router = APIRouter()


@router.post("/auth/token", response_model=TokenResponse)
async def issue_token(payload: TokenRequest) -> TokenResponse:
    user = authenticate_user(payload.username, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return TokenResponse(access_token=create_access_token(user.username, user.role))


@router.get("/aircraft", dependencies=[Depends(require_roles(Role.admin, Role.analyst, Role.observer))])
async def aircraft_states(limit: int = 500):
    return runtime.aircraft_service.list_states()[:limit]


@router.get("/aircraft/routes", dependencies=[Depends(require_roles(Role.admin, Role.analyst, Role.observer))])
async def aircraft_routes(icao24: str | None = None):
    return runtime.aircraft_service.get_routes(icao24)


@router.get("/heatmap", dependencies=[Depends(require_roles(Role.admin, Role.analyst, Role.observer))])
async def heatmap(precision: int = 1):
    return runtime.aircraft_service.build_heatmap(precision=precision)


@router.get("/analytics/traffic-density", dependencies=[Depends(require_roles(Role.admin, Role.analyst))])
async def traffic_density(top_n: int = 10):
    return runtime.aircraft_service.density_snapshot(top_n=top_n)


@router.get("/analytics/risk", dependencies=[Depends(require_roles(Role.admin, Role.analyst))])
async def risk_summary():
    return runtime.risk_service.assess(
        alerts_count=len(runtime.alert_service.list_alerts(limit=300)),
        defense_events=runtime.osint_service.list_defense_events(),
        sea_vessels=runtime.osint_service.list_sea_vessels(),
        land_events=runtime.osint_service.list_land_events(),
    )


@router.get("/cameras", dependencies=[Depends(require_roles(Role.admin, Role.analyst, Role.observer))])
async def cameras():
    return runtime.osint_service.list_cameras()


@router.get("/defense", dependencies=[Depends(require_roles(Role.admin, Role.analyst, Role.observer))])
async def defense_events():
    return runtime.osint_service.list_defense_events()


@router.get("/sea", dependencies=[Depends(require_roles(Role.admin, Role.analyst, Role.observer))])
async def sea_activity():
    return runtime.osint_service.list_sea_vessels()


@router.get("/land", dependencies=[Depends(require_roles(Role.admin, Role.analyst, Role.observer))])
async def land_activity():
    return runtime.osint_service.list_land_events()


@router.get("/geofences", dependencies=[Depends(require_roles(Role.admin, Role.analyst))])
async def geofences():
    return runtime.osint_service.list_geofences()


@router.get("/airspace/boundaries", dependencies=[Depends(require_roles(Role.admin, Role.analyst))])
async def airspace_boundaries():
    return runtime.osint_service.list_airspace_boundaries()


@router.get("/alerts", dependencies=[Depends(require_roles(Role.admin, Role.analyst))])
async def alerts(limit: int = 100):
    return runtime.alert_service.list_alerts(limit=limit)


@router.get("/layers", dependencies=[Depends(require_roles(Role.admin, Role.analyst, Role.observer))])
async def layers(user: Annotated[User, Depends(require_roles(Role.admin, Role.analyst, Role.observer))]):
    defaults = {
        "air": True,
        "land": user.role in {Role.admin, Role.analyst, Role.observer},
        "sea": user.role in {Role.admin, Role.analyst, Role.observer},
        "defense": user.role in {Role.admin, Role.analyst},
    }
    return {"role": user.role, "defaults": defaults}


@router.websocket("/ws/air")
async def ws_air(websocket: WebSocket):
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008)
        return

    try:
        decode_token(token)
    except HTTPException:
        await websocket.close(code=1008)
        return

    await websocket.accept()
    try:
        while True:
            payload = [s.model_dump(mode="json") for s in runtime.aircraft_service.list_states()]
            await websocket.send_json(payload)
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        return
