from typing import List, Optional, Sequence, Set
from Jira.JiraIssue import JiraIssue
from Jira.JiraIssueRepository import JiraIssueRepository
from Settings import Settings
import os
import requests
import base64
import re


class JiraService:
    settings: Settings
    API_KEY: str
    URL_HEADERS: dict

    @staticmethod
    def get_issues_keys_from_string(string: str) -> Set[str]:
        '''get a set of issue keys by parsing string'''
        key_regex = re.compile(r'[A-Z]{2,6}-[1-9][0-9]{0,4}')
        return set(key_regex.findall(string))

    @staticmethod
    def get_single_issue_key_from_string(string: str) -> str:
        key_regex = re.compile(r'[A-Z]{2,6}-[1-9][0-9]{0,4}')
        keys_found = key_regex.findall(string)
        return keys_found[0] if keys_found else None

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.setup()

    def setup(self) -> None:
        '''set up class variables'''
        try:
            self.API_KEY = os.getenv('JIRA_API_KEY', '')
            if (self.settings.JIRA_USER_LOGIN and self.API_KEY):
                credentials_unencoded = ':'.join(
                    [self.settings.JIRA_USER_LOGIN, self.API_KEY])
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
        '''get raw issues data & populate issues repository with issues created from raw data'''
        raw_issues_data: List[dict]
        try:
            if jira_issues_keys:
                raw_issues_data = [
                    self.get_raw_issue_data_by_key(key) for key in jira_issues_keys]
            else:
                raw_issues_data = self.get_raw_all_issues_data()
            repository.populate_from_raw_data(
                raw_issues_data, base_issue_url=self.settings.JIRA_BROWSING_BASE_URL)
            return repository
        except Exception as e:
            raise JiraServiceError(
                f'Error populating Jira issues repository from API: {e}')

    def get_raw_issue_data_by_key(self, key: str) -> dict:
        '''get single issue data by its key'''
        response = requests.get(str(self.settings.JIRA_GET_TASK_URL) + key,
                                headers=self.URL_HEADERS)
        if not response.ok:
            raise JiraServiceError(
                f"Error getting task data from Jira: {response.status_code}")
        return response.json()

    # TODO: projects, status
    def get_raw_all_issues_data(self) -> List[dict]:
        '''get all available issues from Jira, with filters specified in settings.json'''
        jql = self.construct_jql_query()
        response = requests.get(str(self.settings.JIRA_SEARCH_URL),
                                params={
                                    "jql": jql if jql else None},
                                headers=self.URL_HEADERS)
        if not response.ok:
            raise JiraServiceError(
                f"Error getting all tasks data from Jira: {response.json()}")
        return response.json()['issues']

    def construct_jql_query(self) -> str:
        '''construct JQL query using constraints from settings'''
        jql = ""
        if self.settings.JIRA_USER_LOGIN:
            # can't pass "@" into jira unescaped
            user_login_escaped = self.settings.JIRA_USER_LOGIN.replace(
                "@", "\\u0040")
            jql = f'assignee = {user_login_escaped}'
        if self.settings.JIRA_PROJECTS:
            projects_string = ",".join(
                [f'"{p}"' for p in self.settings.JIRA_PROJECTS])
            jql += f' AND project IN ({projects_string})'
        if self.settings.JIRA_EXCLUDED_PROJECTS:
            excluded_projects_string = ",".join(
                [f'"{ep}"' for ep in self.settings.JIRA_EXCLUDED_PROJECTS])
            jql += f' AND project NOT IN ({excluded_projects_string})'
        # tasks must be not done
        jql += ' AND statusCategory != Done'
        return jql


class JiraServiceError(ValueError):
    pass
