from Marvin.MarvinTask import MarvinTask
from Settings import Settings
from typing import List
from Marvin.MarvinProject import MarvinProject
from Utils.async_requests import async_post
import os
import requests
from Utils.logger import logger

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

    async def create_project_with_api(self, project: MarvinProject) -> None:
        data = project.to_json()
        logger.info(f"creating project {project.title} in Marvin...")
        await async_post(self.settings.MARVIN_ADD_PROJECT_URL, headers=self.URL_HEADERS, data=data.encode('utf-8'))

    async def create_projects_with_api(self, projects: List[MarvinProject]) -> None:
        for project in projects:
            await self.create_project_with_api(project)

    async def get_projects_data_from_API(self) -> List[dict]:
        data: List[dict] = await async_post(
            self.settings.MARVIN_GET_ALL_PROJECTS_URL, headers=self.URL_HEADERS)
        
        return data

    async def create_task_with_api(self, task: MarvinTask) -> None:
        task_data = task.to_json()
        logger.info(f"creating task in marvin...")
        await async_post(self.settings.MARVIN_ADD_TASK_URL,
                                 headers=self.URL_HEADERS, data=task_data.encode('utf-8'))

    def ping_for_status_code(self) -> int:
        response = requests.post(self.settings.MARVIN_PING_URL,
                                 headers=self.URL_HEADERS)
        if not response.ok:
            raise MarvinApiException(
                f'Error pinging Marvin API: {response.status_code}')
        return response.status_code


class MarvinApiException(Exception):
    pass
