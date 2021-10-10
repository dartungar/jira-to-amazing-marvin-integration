from typing import List
from Jira.JiraIssue import JiraIssue
from Settings import Settings
import os
import requests
import base64


class JiraService:
    settings: Settings
    API_KEY: str
    URL_HEADERS: dict

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

    def get_raw_issue_data_by_key(self, key: str) -> dict:
        '''get single issue data by its key'''
        response = requests.get(str(self.settings.JIRA_GET_TASK_URL) + key,
                                headers=self.URL_HEADERS)
        if not response.ok:
            raise JiraServiceError(
                f"Error getting task data from Jira: {response.status_code}")
        return response.json()

    def get_issues_from_jira(self, current_user_only=False) -> List[JiraIssue]:
        '''Fetch all available issues from Jira, with filters specified in settings.json'''
        data = self.get_raw_all_issues_data()
        issues = [self.jira_issue_from_raw_data(
            d, self.settings.JIRA_BROWSING_BASE_URL) for d in data]
        return issues

    # TODO: projects, status
    def get_raw_all_issues_data(self, current_user_only=False) -> List[dict]:
        '''Fetch raw data for all available issues from Jira, with filters specified in settings.json'''
        jql = self.construct_jql_query(current_user_only)
        response = requests.get(str(self.settings.JIRA_SEARCH_URL),
                                params={
                                    "jql": jql if jql else None},
                                headers=self.URL_HEADERS)
        if not response.ok:
            raise JiraServiceError(
                f"Error getting all tasks data from Jira: {response.json()}")
        return response.json()['issues']

    def construct_jql_query(self, current_user_only=False) -> str:
        '''construct JQL query using constraints from settings'''
        jql = ""
        conditions = ['statusCategory != Done AND assignee != EMPTY']
        if current_user_only and self.settings.JIRA_USER_LOGIN:
            # can't pass "@" into jira unescaped
            user_login_escaped = self.settings.JIRA_USER_LOGIN.replace(
                "@", "\\u0040")
            conditions.append(f'assignee = {user_login_escaped}')
        if self.settings.JIRA_PROJECTS:
            projects_string = ",".join(
                [f'"{p}"' for p in self.settings.JIRA_PROJECTS])
            conditions.append(f'project IN ({projects_string})')
        if self.settings.JIRA_EXCLUDED_PROJECTS:
            excluded_projects_string = ",".join(
                [f'"{ep}"' for ep in self.settings.JIRA_EXCLUDED_PROJECTS])
            conditions.append(f'project NOT IN ({excluded_projects_string})')
        # tasks must be not done
        jql = " AND ".join(conditions)
        print(jql)
        return jql

    def jira_issue_from_raw_data(self, raw_issue_data: dict, base_issue_url: str):
        return JiraIssue(
            key=raw_issue_data['key'],
            title=raw_issue_data['fields']['summary'],
            project=raw_issue_data['fields']['project']['name'],
            status=raw_issue_data['fields']['status']['name'],
            priority=raw_issue_data['fields']['priority']['name'],
            estimate=raw_issue_data['fields'].get(
                'timetracking').get('originalEstimateSeconds') if raw_issue_data['fields'].get(
                'timetracking') else None,
            link=base_issue_url +
            raw_issue_data['key'] if base_issue_url else '',
            assignee=raw_issue_data['fields']['assignee'].get('emailAddress')
        )


class JiraServiceError(ValueError):
    pass
