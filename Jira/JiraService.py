from typing import List, Optional, Sequence
from Jira.JiraIssue import JiraIssue
from Jira.JiraIssueRepository import JiraIssueRepository
import os
import requests
import base64
import re


class JiraService:
    API_URL_GET_TASK: str
    API_URL_GET_TASKS: str
    API_KEY: str
    JIRA_BASE_ISSUE_URL: str
    JIRA_EMAIL: str
    URL_HEADERS: dict
    DEFAULT_ASSIGNEE = 'currentUser()'

    def __init__(self) -> None:
        self.setup()

    def setup(self) -> None:
        try:
            self.API_URL_GET_TASKS = os.getenv('JIRA_API_URL_GET_TASKS', '')
            self.API_URL_GET_TASK = os.getenv('JIRA_API_URL_GET_TASK', '')
            self.API_KEY = os.getenv('JIRA_API_KEY', '')
            self.JIRA_BASE_ISSUE_URL = os.getenv('JIRA_BASE_ISSUE_URL', '')
            self.JIRA_EMAIL = os.getenv('JIRA_EMAIL', '')
            if (self.JIRA_EMAIL and self.API_KEY):
                credentials_unencoded = ':'.join(
                    [self.JIRA_EMAIL, self.API_KEY])
                credentials = base64.b64encode(
                    credentials_unencoded.encode())
                self.URL_HEADERS = {}
                self.URL_HEADERS["Authorization"] = b"Basic " + credentials
            else:
                raise Exception(
                    "JIRA_EMAIL and/or API_KEY system variables not found")
        except Exception as e:
            raise JiraServiceError(f"Error during Jira service setup: {e}")

    def populate_issues_repository_from_API(self, repository: JiraIssueRepository, jira_issues_keys: List[str] = None) -> JiraIssueRepository:
        raw_issues_data: List[dict]
        try:
            if jira_issues_keys:
                raw_issues_data = [
                    self.get_raw_issue_data_by_key(key) for key in jira_issues_keys]
            else:
                raw_issues_data = self.get_raw_all_issues_data()
            repository.populate_from_raw_data(
                raw_issues_data, self.JIRA_BASE_ISSUE_URL)
            return repository
        except Exception as e:
            raise JiraServiceError(
                f'Error populating Jira issues repository from API: {e}')

    def get_raw_issue_data_by_key(self, key: str) -> dict:
        response = requests.get(str(self.API_URL_GET_TASK) + key,
                                headers=self.URL_HEADERS)
        if not response.ok:
            raise JiraServiceError(
                f"Error getting task data from Jira: {response.status_code}")
        return response.json()

    # TODO: projects, status
    def get_raw_all_issues_data(self, assignee=DEFAULT_ASSIGNEE, status=None, projects=None) -> List[dict]:
        jql = ""
        if assignee or status:
            jql = f'assignee = {assignee}'
            # tasks must be not done
            jql += ' AND statusCategory != Done'
        response = requests.get(str(self.API_URL_GET_TASKS),
                                params={
                                    "jql": jql if jql else None},
                                headers=self.URL_HEADERS)
        if not response.ok:
            raise JiraServiceError(
                f"Error getting all tasks data from Jira: {response.json()}")
        return response.json()['issues']

    def get_issues_keys_from_string(self, string: str) -> set[str]:
        key_regex = re.compile(r'[A-Z]{2,6}-[1-9][0-9]{0,4}')
        return set(key_regex.findall(string))


class JiraServiceError(ValueError):
    pass
