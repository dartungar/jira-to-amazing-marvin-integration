from typing import List
from Jira.JiraIssueRepository import JiraIssueRepository
from Jira.JiraService import JiraService
from Marvin.MarvinService import MarvinService
from Marvin.MarvinProjectRepository import MarvinProjectsRepository
from Marvin.MarvinProject import MarvinProject


class Application:

    def __init__(self) -> None:
        self.jira = JiraService()
        self.issues_repository = JiraIssueRepository()
        self.marvin = MarvinService()
        self.existing_projects_repository = MarvinProjectsRepository()
        self.new_projects_repository = MarvinProjectsRepository()

    def sync(self) -> None:
        self.populate_issues_repository_from_jira()
        self.populate_existing_projects_repository()
        # list of projects that would be created
        self.new_projects_repository = [MarvinProject.from_jira_issue(
            issue) for issue in self.issues_repository.data if not self.existing_projects_repository.exists_with_key(issue.key)]
        self.create_multiple_projects_in_marvin(self.new_projects_repository)

    def get_jira_issues_by_string_and_add_projects_to_marvin(self, string) -> None:
        issues_keys = self.jira.get_issues_keys_from_string(string)
        self.populate_issues_repository_from_jira(issues_keys=issues_keys)
        projects = MarvinProjectsRepository.populate_from_list_of_issues(
            self.issues_repository.data)
        self.create_multiple_projects_in_marvin(projects)

    def populate_issues_repository_from_jira(self, issues_keys: List[str] = None) -> None:
        self.issues_repository = self.jira.populate_issues_repository_from_API(
            self.issues_repository, jira_issues_keys=issues_keys)

    def populate_existing_projects_repository(self) -> None:
        self.existing_projects_repository = self.marvin.populate_repository_from_API(
            self.existing_projects_repository)

    def create_multiple_projects_in_marvin(self, projects: List[MarvinProject]) -> None:
        for project in projects:
            self.create_project_in_marvin(project)

    def create_project_in_marvin(self, project: MarvinProject) -> None:
        self.marvin.create_project_with_API(project)
