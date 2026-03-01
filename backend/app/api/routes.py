from typing import Annotated

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from app.core.auth import authenticate_user, create_access_token, require_roles
from app.models.schemas import Role, TokenRequest, TokenResponse, User
from app.services.runtime import runtime

router = APIRouter()


@router.post("/auth/token", response_model=TokenResponse)
async def issue_token(payload: TokenRequest) -> TokenResponse:
    user = authenticate_user(payload.username, payload.password)
    if not user:
        from fastapi import HTTPException, status

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return TokenResponse(access_token=create_access_token(user.username, user.role))


@router.get("/aircraft", dependencies=[Depends(require_roles(Role.admin, Role.analyst, Role.observer))])
async def aircraft_states():
    return runtime.aircraft_service.list_states()


@router.get("/aircraft/routes", dependencies=[Depends(require_roles(Role.admin, Role.analyst, Role.observer))])
async def aircraft_routes(icao24: str | None = None):
    return runtime.aircraft_service.get_routes(icao24)


@router.get("/heatmap", dependencies=[Depends(require_roles(Role.admin, Role.analyst, Role.observer))])
async def heatmap():
    return runtime.aircraft_service.build_heatmap()


@router.get("/cameras", dependencies=[Depends(require_roles(Role.admin, Role.analyst, Role.observer))])
async def cameras():
    return runtime.osint_service.list_cameras()


@router.get("/defense", dependencies=[Depends(require_roles(Role.admin, Role.analyst, Role.observer))])
async def defense_events():
    return runtime.osint_service.list_defense_events()


@router.get("/geofences", dependencies=[Depends(require_roles(Role.admin, Role.analyst))])
async def geofences():
    return runtime.osint_service.list_geofences()


@router.get("/alerts", dependencies=[Depends(require_roles(Role.admin, Role.analyst))])
async def alerts():
    return runtime.alert_service.list_alerts()


@router.get("/layers", dependencies=[Depends(require_roles(Role.admin, Role.analyst, Role.observer))])
async def layers(user: Annotated[User, Depends(require_roles(Role.admin, Role.analyst, Role.observer))]):
    defaults = {
        "air": True,
        "land": user.role in {Role.admin, Role.analyst},
        "sea": user.role in {Role.admin, Role.analyst},
        "defense": user.role in {Role.admin, Role.analyst},
    }
    return {"role": user.role, "defaults": defaults}


@router.websocket("/ws/air")
async def ws_air(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.send_json([s.model_dump(mode="json") for s in runtime.aircraft_service.list_states()])
            await websocket.receive_text()
    except WebSocketDisconnect:
        return
