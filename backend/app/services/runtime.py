import asyncio
import contextlib

from app.services.aircraft import AircraftService
from app.services.alerts import AlertService
from app.services.osint import OSINTService


class Runtime:
    def __init__(self) -> None:
        self.aircraft_service = AircraftService()
        self.alert_service = AlertService()
        self.osint_service = OSINTService()
        self._task: asyncio.Task | None = None

    async def start(self) -> None:
        await self.aircraft_service.refresh()
        geofences = self.osint_service.list_geofences()
        self.alert_service.evaluate_aircraft(self.aircraft_service.list_states(), geofences)
        self._task = asyncio.create_task(self._background_loop())

    async def stop(self) -> None:
        if self._task:
            self._task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._task

    async def _background_loop(self) -> None:
        geofences = self.osint_service.list_geofences()
        while True:
            await self.aircraft_service.refresh()
            self.alert_service.evaluate_aircraft(self.aircraft_service.list_states(), geofences)
            await asyncio.sleep(10)


runtime = Runtime()
