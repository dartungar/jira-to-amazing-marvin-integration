from Marvin.MarvinTask import MarvinTask
from Settings import Settings
from typing import List
from Marvin.MarvinProjectRepository import MarvinProjectsRepository
from Marvin.MarvinProject import MarvinProject, MarvinProjectStatuses
from Marvin.MarvinService import MarvinServiceException
import os
import requests


class MarvinApiService:
    settings: Settings
    MARVIN_API_KEY: str
    URL_HEADERS: dict

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.setup()

    def setup(self) -> None:
        try:
            self.MARVIN_API_KEY = os.getenv('MARVIN_API_KEY', '')
            self.URL_HEADERS = {
                'Content-Type': 'application/json',
                'X-API-Token': self.MARVIN_API_KEY
            }
        except Exception as e:
            raise MarvinApiException(f"Error during Marvin service setup: {e}")

    def create_project_with_API(self, project: MarvinProject) -> None:
        data = project.to_json()
        response = requests.post(
            self.settings.MARVIN_ADD_PROJECT_URL, headers=self.URL_HEADERS, data=data.encode('utf-8'))
        if not response.ok:
            raise MarvinApiException(
                f'Error adding project into Marvin: {response.status_code}')

    def create_projects_with_api(self, projects: List[MarvinProject]) -> None:
        for project in projects:
            self.create_project_with_API(project)

    def get_projects_data_from_API(self) -> List[dict]:
        response = requests.post(
            self.settings.MARVIN_GET_ALL_PROJECTS_URL, headers=self.URL_HEADERS)
        if not response.ok:
            raise MarvinApiException(
                f'Error getting projects data from Marvin: {response.status_code}')

        return response.json()

    def create_task_with_api(self, task: MarvinTask) -> None:
        data = task.to_json()
        response = requests.post(self.settings.MARVIN_ADD_TASK_URL,
                                 headers=self.URL_HEADERS, data=data.encode('utf-8'))
        if not response.ok:
            raise MarvinApiException(
                f'Error adding task into Marvin: {response.status_code}')

    def ping_for_status_code(self) -> int:
        response = requests.post(self.settings.MARVIN_PING_URL,
                                 headers=self.URL_HEADERS)
        if not response.ok:
            raise MarvinApiException(
                f'Error pinging Marvin API: {response.status_code}')
        return response.status_code


class MarvinApiException(MarvinServiceException):
    pass
