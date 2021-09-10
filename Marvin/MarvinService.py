from typing import List
from Marvin.MarvinProjectRepository import MarvinProjectsRepository
from Marvin.MarvinProject import MarvinProject
import os
import requests


class MarvinService:
    MARVIN_ADD_PROJECT_URL: str
    MARVIN_GET_PROJECTS_URL: str
    MARVIN_PING_URL: str
    MARVIN_API_KEY: str
    URL_HEADERS: dict
    projects_repository: MarvinProjectsRepository = MarvinProjectsRepository()

    def __init__(self) -> None:
        self.setup()

    def setup(self) -> None:
        try:
            self.MARVIN_ADD_PROJECT_URL = os.getenv(
                'MARVIN_ADD_PROJECT_URL', '')
            self.MARVIN_GET_PROJECTS_URL = os.getenv(
                'MARVIN_GET_PROJECTS_URL', '')
            self.MARVIN_PING_URL = os.getenv('MARVIN_PING_URL', '')
            self.MARVIN_API_KEY = os.getenv('MARVIN_API_KEY', '')

            self.URL_HEADERS = {
                'Content-Type': 'application/json',
                'X-API-Token': self.MARVIN_API_KEY
            }
        except Exception as e:
            raise MarvinServiceError(f"Error during Marvin service setup: {e}")

    def create_project_with_API(self, project: MarvinProject) -> None:
        data = project.to_json()
        print(data)
        response = requests.post(
            self.MARVIN_ADD_PROJECT_URL, headers=self.URL_HEADERS, data=data.encode('utf-8'))
        if not response.ok:
            raise MarvinServiceError(
                f'Error adding project into Marvin: {response.status_code}')

    def get_projects_data_from_API(self) -> List[dict]:
        response = requests.post(
            self.MARVIN_GET_PROJECTS_URL, headers=self.URL_HEADERS)
        if not response.ok:
            raise MarvinServiceError(
                f'Error getting projects data from Marvin: {response.status_code}')

        return response.json()

    def populate_repository_from_API(self, repository: MarvinProjectsRepository) -> MarvinProjectsRepository:

        try:
            data = self.get_projects_data_from_API()
            repository.populate_from_raw_data(data)
            return repository
        except Exception as e:  # TODO: catch specific error
            raise MarvinServiceError(
                f'Error populating Marvin projects repository from API: {e}')

    def ping_for_status_code(self) -> int:
        response = requests.post(self.MARVIN_PING_URL,
                                 headers=self.URL_HEADERS)
        if not response.ok:
            raise MarvinServiceError(
                f'Error pinging Marvin API: {response.status_code}')
        return response.status_code


class MarvinServiceError(ValueError):
    pass
