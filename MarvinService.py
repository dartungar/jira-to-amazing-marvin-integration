from MarvinProject import MarvinProject
import os
import requests


class MarvinService:

    MARVIN_ADD_PROJECT_URL = os.getenv('MARVIN_ADD_PROJECT_URL')
    MARVIN_API_KEY = os.getenv('MARVIN_API_KEY')
    URL_HEADERS = {
        'Content-Type': 'application/json',
        'X-API-Token': MARVIN_API_KEY
    }

    def create_project(self, project: MarvinProject) -> None:
        data = project.to_json()
        print(data)
        response = requests.post(
            self.MARVIN_ADD_PROJECT_URL, headers=self.URL_HEADERS, data=data.encode('utf-8'))
        if not response.ok:
            raise ValueError(
                f'Error adding project into Marvin: {response.status_code}')
