from Settings import Settings
from Application.SyncService import SyncService


class Application:
    service: SyncService

    def __init__(self) -> None:
        self.settings = Settings()
        self.service = SyncService()

    async def sync(self) -> None:
        await self.service.sync()

    async def update_projects(self) -> None:
        await self.service.create_remider_tasks_for_projects()

