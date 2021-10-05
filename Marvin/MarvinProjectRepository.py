from Jira.JiraIssue import JiraIssue
from Marvin.MarvinProject import MarvinProject, MarvinProjectStatuses
from typing import List


class MarvinProjectsRepository:

    def __init__(self) -> None:
        self.data: List[MarvinProject] = []

    @property
    def project_jira_keys(self) -> List[str]:
        return [p.jira_key for p in self.data if p.jira_key]

    @property
    def not_synced_projects(self) -> List[MarvinProject]:
        return [p for p in self.data if p.sync_status == MarvinProjectStatuses.exists_only_in_jira]

    @property
    def synced_projects(self) -> List[MarvinProject]:
        return [p for p in self.data if p.sync_status == MarvinProjectStatuses.synced]

    @property
    def sync_not_needed_projects(self) -> List[MarvinProject]:
        return [p for p in self.data if p.sync_status == MarvinProjectStatuses.exists_only_in_marvin]

    def populate_from_raw_data(self, raw_data: List[dict]) -> None:
        '''populate from an array of dicts'''
        self.clear()
        self.add_multiple_from_raw_data(raw_data)

    def populate_from_list_of_issues(self, issues: List[JiraIssue], sync_status: int) -> None:
        '''populate from an array of JiraIssue objects'''
        self.clear()
        self.add_multiple_from_jira_issues(issues, sync_status)

    def exists_with_key(self, key: str) -> bool:
        '''check if project with such issue key already exists'''
        return any([proj.jira_key == key for proj in self.data])

    def exists_with_project(self, project: MarvinProject) -> bool:
        '''check if project with such title already exists'''
        return any([proj.title == project.title for proj in self.data])

    def set_sync_status_to_all_projects(self, status: int) -> None:
        for project in self.data:
            project.sync_status = status

    def set_sync_status_to_all_projects_if_not_defined(self, status: int) -> None:
        for project in self.data:
            if project.sync_status == MarvinProjectStatuses.not_defined:
                project.sync_status = status

    def clear(self) -> None:
        self.data.clear()

    def add(self, project: MarvinProject) -> None:
        self.data.append(project)

    def get_by_jira_key(self, jira_key: str) -> MarvinProject:
        try:
            return [p for p in self.data if p.jira_key == jira_key][0]
        except IndexError:
            raise IndexError

    def add_multiple_from_raw_data(self, raw_data: List[dict]) -> None:
        for entry in raw_data:
            project = MarvinProject.from_object(entry)
            self.add(project)

    def add_multiple_from_jira_issues(self, issues: List[JiraIssue], sync_status: int) -> None:
        for issue in issues:
            if issue.key not in self.project_jira_keys:
                project = MarvinProject.from_jira_issue(issue)
                project.sync_status = sync_status
                self.add(project)
