from Marvin.MarvinTask import MarvinTask
from Settings import Settings
from typing import List
from Marvin.MarvinProjectRepository import MarvinProjectsRepository
from Marvin.MarvinProject import MarvinProject, MarvinProjectStatuses
import os
import requests


class MarvinService:
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
            raise MarvinServiceError(f"Error during Marvin service setup: {e}")

    def create_project_with_API(self, project: MarvinProject) -> None:
        data = project.to_json()
        response = requests.post(
            self.settings.MARVIN_ADD_PROJECT_URL, headers=self.URL_HEADERS, data=data.encode('utf-8'))
        if not response.ok:
            raise MarvinServiceError(
                f'Error adding project into Marvin: {response.status_code}')

    def get_projects_data_from_API(self) -> List[dict]:
        response = requests.post(
            self.settings.MARVIN_GET_ALL_PROJECTS_URL, headers=self.URL_HEADERS)
        if not response.ok:
            raise MarvinServiceError(
                f'Error getting projects data from Marvin: {response.status_code}')

        return response.json()

    def populate_projects_repository_from_API(self, repository: MarvinProjectsRepository) -> MarvinProjectsRepository:
        try:
            data = self.get_projects_data_from_API()
            repository.populate_from_raw_data(data)
            repository.set_sync_status_to_all_projects(
                MarvinProjectStatuses.exists_only_in_marvin)
            return repository
        except Exception as e:  # TODO: catch specific error
            raise MarvinServiceError(
                f'Error populating Marvin projects repository from API: {e}')

    def create_task_with_api(self, task: MarvinTask) -> None:
        data = task.to_json()
        response = requests.post(self.settings.MARVIN_ADD_TASK_URL, headers=self.URL_HEADERS, data=data.encode('utf-8'))
        if not response.ok:
            raise MarvinServiceError(f'Error adding task into Marvin: {response.status_code}')


    def ping_for_status_code(self) -> int:
        response = requests.post(self.settings.MARVIN_PING_URL,
                                 headers=self.URL_HEADERS)
        if not response.ok:
            raise MarvinServiceError(
                f'Error pinging Marvin API: {response.status_code}')
        return response.status_code


class MarvinServiceError(ValueError):
    pass
