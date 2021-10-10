from Settings import Settings
from Application.SyncService import SyncService
import logging

logging.basicConfig(level=logging.INFO)


class Application:
    service: SyncService

    def __init__(self) -> None:
        self.settings = Settings()
        self.service = SyncService()

    def sync(self) -> None:
        self.service.sync()

    def check_assignees(self) -> None:
        self.service.create_remider_tasks_for_projects_with_changed_assignees()

