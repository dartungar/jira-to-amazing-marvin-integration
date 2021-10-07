from Marvin.MarvinTask import MarvinTask
from Project.ProjectService import ProjectService
from Settings import Settings
from typing import List
from Jira.JiraIssueRepository import JiraIssueRepository
from Jira.JiraService import JiraService
from Marvin.MarvinService import MarvinService
from Marvin.MarvinProjectRepository import MarvinProjectsRepository
from Marvin.MarvinProject import MarvinProject, MarvinProjectStatuses
import logging

logging.basicConfig(level=logging.INFO)


class Application:
    settings: Settings
    service: ProjectService

    def __init__(self) -> None:
        self.settings = Settings()
        self.service = ProjectService(self.settings)

    def sync(self) -> None:
        self.service.sync()


