import json
from typing import List


class Settings:

    JIRA_USER_LOGIN: str
    JIRA_GET_TASK_URL: str
    JIRA_SEARCH_URL: str
    JIRA_BROWSING_BASE_URL: str
    JIRA_PROJECTS: List[str]
    JIRA_EXCLUDED_PROJECTS: List[str]

    MARVIN_ADD_PROJECT_URL: str
    MARVIN_GET_ALL_PROJECTS_URL: str
    MARVIN_PING_URL: str

    def __init__(self) -> None:
        settings = self.from_settings_json()
        self.JIRA_USER_LOGIN = settings['Jira']['USER_LOGIN']
        self.JIRA_GET_TASK_URL = settings['Jira']['GET_TASK_URL']
        self.JIRA_SEARCH_URL = settings['Jira']['SEARCH_URL']
        self.JIRA_BROWSING_BASE_URL = settings['Jira']['BROWSING_BASE_URL']
        self.JIRA_PROJECTS = settings['Jira']['PROJECTS']
        self.JIRA_EXCLUDED_PROJECTS = settings['Jira']['EXCLUDED_PROJECTS']
        self.MARVIN_ADD_PROJECT_URL = settings['Marvin']['ADD_PROJECT_URL']
        self.MARVIN_GET_ALL_PROJECTS_URL = settings['Marvin']['GET_ALL_PROJECTS_URL']
        self.MARVIN_PING_URL = settings['Marvin']['PING_URL']

    def from_settings_json(self) -> dict:
        with open('settings.json', 'r', encoding="utf8") as f:
            settings = json.load(f)
            return settings
