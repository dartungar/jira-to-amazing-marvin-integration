from typing import List
from Jira.JiraIssue import JiraIssue
from Jira.Jql.JqlBuilderBase import JqlBuilderBase
from Settings import Settings
import os
import base64

from Utils.async_requests import async_get


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
                self.URL_HEADERS["Authorization"] = (b"Basic " + credentials).decode("utf-8")
            else:
                raise Exception(
                    "JIRA_USER_LOGIN and/or API_KEY system variables not found")
        except Exception as e:
            raise JiraServiceError(f"Error during Jira service setup: {e}")

    async def get_raw_issue_data_by_key(self, key: str) -> dict:
        '''get single issue data by its key'''
        data = await async_get(str(self.settings.JIRA_GET_TASK_URL) + key,
                                headers=self.URL_HEADERS)
        return data
    
    async def get_issues_from_jira(self, current_user_only=False) -> List[JiraIssue]:
        '''Fetch all available issues from Jira, with filters specified in settings.json'''
        data = await self.get_raw_all_issues_data()
        issues = [self.jira_issue_from_raw_data(
            d, self.settings.JIRA_BROWSING_BASE_URL) for d in data]
        return issues

    # TODO: projects, status
    async def get_raw_all_issues_data(self, current_user_only=False, get_done=False) -> List[dict]:
        '''Fetch raw data for all available issues from Jira, with filters specified in settings.json'''
        jql = self.construct_jql_query(current_user_only, get_done)
        data = await async_get(str(self.settings.JIRA_SEARCH_URL),
                                params={
                                    "jql": jql if jql else None},
                                headers=self.URL_HEADERS)
        return data['issues']

    def construct_jql_query(self, current_user_only=False, get_done=False) -> str:
        '''construct JQL query using constraints from settings'''
        jql = JqlBuilderBase()
        jql.with_assignee_not_empty()
        if not get_done and self.settings.JIRA_STATUS_CATEGORIES_ACTIVE:
            jql.with_status_categories(self.settings.JIRA_STATUS_CATEGORIES_ACTIVE)
        if current_user_only and self.settings.JIRA_USER_LOGIN:
            jql.with_assignees([self.settings.JIRA_USER_LOGIN])
        if self.settings.JIRA_PROJECTS:
            jql.with_projects(self.settings.JIRA_PROJECTS)
        if self.settings.JIRA_EXCLUDED_PROJECTS:
            jql.exclude_projects(self.settings.JIRA_EXCLUDED_PROJECTS)
        return str(jql)

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
            assignee=raw_issue_data['fields']['assignee'].get('emailAddress'),
            has_subtasks=True if raw_issue_data['fields'].get('subtasks') else False
        )


class JiraServiceError(ValueError):
    pass
