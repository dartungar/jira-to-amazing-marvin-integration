from typing import List
from Jira.JiraIssue import JiraIssue
from Jira.JiraIssueRepository import JiraIssueRepository
import os
import requests
import base64
import re
import json


class JiraService:

    # config variables
    API_URL_GET_TASK: str = os.getenv('JIRA_API_URL_GET_TASK')
    API_URL_GET_TASKS: str = os.getenv('JIRA_API_URL_GET_TASKS')
    API_KEY: str = os.getenv('JIRA_API_KEY')
    JIRA_BASE_ISSUE_URL = os.getenv('JIRA_BASE_ISSUE_URL')
    credentials_unencoded = ':'.join(
        [os.getenv('JIRA_EMAIL'), API_KEY])
    CREDENTIALS: str = base64.b64encode(
        credentials_unencoded.encode())
    URL_HEADERS: object = {
        "Authorization": b"Basic " + CREDENTIALS}
    DEFAULT_ASSIGNEE = 'currentUser()'

    def populate_issues_repository_from_API(self, repository: JiraIssueRepository, jira_issues_keys: List[str] = None) -> JiraIssueRepository:
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

    def get_raw_issue_data_by_key(self, key: str) -> object:
        response = requests.get(self.API_URL_GET_TASK + key,
                                headers=self.URL_HEADERS)
        if not response.ok:
            raise JiraServiceError(
                f"Error getting task data from Jira: {response.code}")
        return response.json()

    # TODO: projects, status
    def get_raw_all_issues_data(self, assignee=DEFAULT_ASSIGNEE, status=None, projects=None) -> object:
        jql = ""
        if assignee or status:
            jql = f'assignee = {assignee}'
            # tasks must be not done
            jql += ' AND statusCategory != Done'
        response = requests.get(self.API_URL_GET_TASKS,
                                params={
                                    "jql": jql if jql else None},
                                headers=self.URL_HEADERS)
        if not response.ok:
            raise JiraServiceError(
                f"Error getting all tasks data from Jira: {response.json()}")
        return response.json()['issues']

    def get_issues_keys_from_string(self, string: str) -> set:
        key_regex = re.compile(r'[A-Z]{2,6}-[1-9][0-9]{0,4}')
        return set(key_regex.findall(string))


class JiraServiceError(ValueError):
    pass
