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
        self.project_repository = MarvinProjectsRepository()

    def sync(self) -> None:
        self.issues_repository = self.jira.populate_issues_repository_from_API(
            self.issues_repository)
        self.project_repository = self.marvin.populate_repository_from_API(
            self.project_repository)

        # list of projects that would be created
        new_projects = MarvinProjectsRepository()
        new_projects = [MarvinProject.from_jira_issue(
            issue) for issue in self.issues_repository.data]
        # remove projects that are already present in Marvin
        # match by title
        new_projects = [
            project for project in new_projects if not self.project_repository.exists_by_project(project)]
        for new_project in new_projects:
            self.create_project_in_marvin(new_project)

    def get_jira_issues_by_string_and_add_projects_to_marvin(self, string) -> None:
        issues_keys = self.jira.get_issues_keys_from_string(string)
        self.issues_repository = self.jira.populate_issues_repository_from_API(
            self.issues_repository, issues_keys)
        projects = [MarvinProject.from_jira_issue(
            issue) for issue in self.issues_repository.data]
        for project in projects:
            self.create_project_in_marvin(project)

    def create_project_in_marvin(self, project: MarvinProject) -> None:
        self.marvin.create_project_with_API(project)
