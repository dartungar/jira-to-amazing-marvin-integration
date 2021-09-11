from Settings import Settings
from typing import List
from Jira.JiraIssueRepository import JiraIssueRepository
from Jira.JiraService import JiraService
from Marvin.MarvinService import MarvinService
from Marvin.MarvinProjectRepository import MarvinProjectsRepository
from Marvin.MarvinProject import MarvinProject
import logging

logging.basicConfig(level=logging.INFO)


class Application:

    def __init__(self) -> None:
        self.settings = Settings()
        self.jira = JiraService(self.settings)
        self.issues_repository = JiraIssueRepository()
        self.marvin = MarvinService(self.settings)
        self.existing_projects_repository = MarvinProjectsRepository()
        # TODO: make into repository or refactor into single repo with statuses
        self.new_projects: List[MarvinProject] = []

    def sync(self) -> None:
        self.populate_issues_repository_from_jira()
        if not self.issues_repository.data:
            logging.info("found no issues in Jira.")
            return
        self.populate_existing_projects_repository()
        if not self.existing_projects_repository.data:
            logging.warning(
                "found no projects in Marvin. this might be not OK!")
            return
        logging.info(
            "checking if there are Jira issues without corresponding Marvin project...")
        # TODO: отрефакторить в отдельную функцию
        self.new_projects = [MarvinProject.from_jira_issue(
            issue) for issue in self.issues_repository.data if not self.existing_projects_repository.exists_with_key(issue.key)]
        if self.new_projects:
            self.create_multiple_projects_in_marvin(self.new_projects)
        else:
            logging.info("all Marvin projects are up to date.")

    def get_jira_issues_by_string_and_add_projects_to_marvin(self, string) -> None:
        issues_keys = self.jira.get_issues_keys_from_string(string)
        self.populate_issues_repository_from_jira(issues_keys=issues_keys)
        if not self.issues_repository.data:
            logging.info("found no issues in Jira.")
            return
        projects: MarvinProjectsRepository = MarvinProjectsRepository.populate_from_list_of_issues(
            self.issues_repository.data)
        if projects.data:
            self.create_multiple_projects_in_marvin(projects)
        else:
            logging.info("found no projects.")

    def populate_issues_repository_from_jira(self, issues_keys: List[str] = None) -> None:
        logging.info("getting issues data from Jira...")
        self.issues_repository = self.jira.populate_issues_repository_from_API(
            self.issues_repository, jira_issues_keys=issues_keys)

    def populate_existing_projects_repository(self) -> None:
        logging.info("getting projects data from Marvin...")
        self.existing_projects_repository = self.marvin.populate_repository_from_API(
            self.existing_projects_repository)

    def create_multiple_projects_in_marvin(self, projects: List[MarvinProject]) -> None:
        logging.info("creating projects in Marvin...")
        for project in projects:
            self.create_project_in_marvin(project)
        logging.info("done!")

    def create_project_in_marvin(self, project: MarvinProject) -> None:
        self.marvin.create_project_with_API(project)
