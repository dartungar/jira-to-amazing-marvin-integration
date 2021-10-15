from Marvin.MarvinProjectRepository import MarvinProjectsRepository
from Marvin.MarvinProject import MarvinProject
from Marvin.JiraToMarvinConverter import JiraToMarvinConverter
from Jira.JiraIssue import JiraIssue
from Utils.parsers import get_single_issue_key_from_string
from typing import List

class MarvinProjectService:
    projects: MarvinProjectsRepository

    def __init__(self) -> None:
        self.projects = MarvinProjectsRepository()

    def populate_from_raw_data(self, raw_data: List[dict]) -> None:
        '''populate from an array of dicts'''
        self.clear()
        self.add_multiple_from_raw_data(raw_data)

    def populate_from_list_of_issues(self, issues: List[JiraIssue]) -> None:
        '''populate from an array of JiraIssue objects'''
        self.clear()
        self.add_multiple_from_jira_issues(issues)

    def add_multiple_from_raw_data(self, raw_data: List[dict]) -> None:
        for entry in raw_data:
            self.add_from_object(entry)

    def add_multiple_from_jira_issues(self, issues: List[JiraIssue]) -> None:
        for i in issues:
            self.add_from_jira_issue(i)

    def add_from_jira_issue(self, issue: JiraIssue) -> None:
        try:
            project_for_jira_issue = [
                p for p in self.projects.data if p.key == issue.key][0]
            project_for_jira_issue.jira_issue = issue
        except IndexError:
            new_project = JiraToMarvinConverter.marvin_project_from_jira_issue(
                issue)
            self.projects.add(new_project)

    def add_from_object(self, obj: dict):
        project = MarvinProject(
            marvin_id=obj['_id'],
            title=obj['title'],
            key=get_single_issue_key_from_string(obj['title']),
            parent_id=obj['parentId'],
            tags=obj.get('labelIds') or []
        )
        self.projects.add(project)

    def clear(self) -> None:
        self.projects.clear()


    @property
    def project_jira_keys(self) -> List[str]:
        return [p.key for p in self.projects.data if p.key]

    @property
    def not_synced_projects(self) -> List[MarvinProject]:
        return [p for p in self.projects.data if p.needs_syncing]

    @property
    def synced_projects(self) -> List[MarvinProject]:
        return [p for p in self.projects.data if p.jira_issue and p.marvin_id]

    @property
    def sync_not_needed_projects(self) -> List[MarvinProject]:
        return [p for p in self.projects.data if not p.jira_issue and p.marvin_id]

    @property
    def projects_with_changed_assignees(self) -> List[MarvinProject]:
        return [p for p in self.projects.data if p.marvin_id and p.assignee_is_changed]


