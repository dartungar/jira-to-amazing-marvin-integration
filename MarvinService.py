from MarvinProjectRepository import MarvinProjectsRepository
from MarvinProject import MarvinProject
import os
import requests


class MarvinService:

    MARVIN_ADD_PROJECT_URL = os.getenv('MARVIN_ADD_PROJECT_URL')
    MARVIN_GET_PROJECTS_URL = os.getenv('MARVIN_GET_PROJECTS_URL')
    MARVIN_API_KEY = os.getenv('MARVIN_API_KEY')
    URL_HEADERS = {
        'Content-Type': 'application/json',
        'X-API-Token': MARVIN_API_KEY
    }

    def __init__(self) -> None:
        self.projects_repository = MarvinProjectsRepository()

    def create_project_with_API(self, project: MarvinProject) -> None:
        data = project.to_json()
        print(data)
        response = requests.post(
            self.MARVIN_ADD_PROJECT_URL, headers=self.URL_HEADERS, data=data.encode('utf-8'))
        if not response.ok:
            raise MarvinServiceError(
                f'Error adding project into Marvin: {response.status_code}')

    def get_projects_data_from_API(self) -> str:
        response = requests.post(
            self.MARVIN_GET_PROJECTS_URL, headers=self.URL_HEADERS)
        if not response.ok:
            raise MarvinServiceError(
                f'Error getting projects data from Marvin: {response.status_code}')

        return response.json()

    def populate_repository_from_API(self) -> None:
        data = self.get_projects_data_from_API()
        try:
            self.projects_repository.populate_from_raw_data(data)
        except Exception as e:  # TODO: catch specific error
            raise MarvinServiceError(
                f'Error populating Marvin projects repository: {e}')


class MarvinServiceError(ValueError):
    pass
