from Settings import Settings
from typing import List
from Jira.JiraIssueRepository import JiraIssueRepository
from Jira.JiraService import JiraService
from Marvin.MarvinService import MarvinService
from Marvin.MarvinProjectRepository import MarvinProjectsRepository
from Marvin.MarvinProject import MarvinProject, MarvinProjectStatuses
import logging

logging.basicConfig(level=logging.INFO)


class Application:

    def __init__(self) -> None:
        self.settings = Settings()
        self.jira = JiraService(self.settings)
        self.issues_repository = JiraIssueRepository()
        self.marvin = MarvinService(self.settings)
        self.projects_repository = MarvinProjectsRepository()

    def sync(self) -> None:
        '''get a list of issues from Jira, get a list of projects from Marvin,
        determine whether Jira issues need to be created as Marvin projects,
        and create Marvin projects if needed
        '''
        self.populate_issues_repository_from_jira()
        if not self.issues_repository.data:
            logging.info("found no issues in Jira.")
            return
        self.populate_projects_repository()
        if not self.projects_repository.data:
            logging.warning(
                "found no projects in Marvin. this might be not OK, check if Marvin API calls work!")
            return
        # add new projects from Jira issues
        self.projects_repository.add_multiple_from_jira_issues(
            self.issues_repository.data)
        self.projects_repository.set_sync_status_to_all_projects_if_not_defined(
            MarvinProjectStatuses.exists_only_in_jira)
        self.actualize_marvin_project_statuses()
        if self.projects_repository.not_synced_projects:
            self.create_multiple_projects_in_marvin(
                self.projects_repository.not_synced_projects)
        else:
            logging.info("all Marvin projects are up to date.")

    def get_jira_issues_by_string_and_add_projects_to_marvin(self, string) -> None:
        issues_keys = JiraService.get_issues_keys_from_string(string)
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

    def populate_projects_repository(self) -> None:
        logging.info("getting projects data from Marvin...")
        self.projects_repository = self.marvin.populate_repository_from_API(
            self.projects_repository)

    def actualize_marvin_project_statuses(self) -> None:
        '''set Marvin project synchronization status based on whether there is already a Jira issue with such a key'''
        logging.info("actualizing Marvin projects statuses...")
        print(f"issues keys: {self.issues_repository.issues_keys}")
        # TODO: переделать алгоритм расчета статуса, т.к сейчас
        # по всем задачам Jira создается проект Марвина
        # и он считается "синхронизированным" т.к есть в обоих списках
        for project in self.projects_repository.data:
            print(f"project key: {project.jira_key} {project.sync_status}")
            if project.jira_key in self.issues_repository.issues_keys:
                if project.sync_status == MarvinProjectStatuses.exists_only_in_marvin or project.sync_status == MarvinProjectStatuses.not_defined:
                    project.sync_status = MarvinProjectStatuses.synced
                if project.sync_status == MarvinProjectStatuses.exists_only_in_jira:
                    continue
            else:
                project.sync_status = MarvinProjectStatuses.exists_only_in_marvin

    def create_multiple_projects_in_marvin(self, projects: List[MarvinProject]) -> None:
        logging.info("creating projects in Marvin...")
        for project in projects:
            self.create_project_in_marvin(project)
        logging.info("done!")

    def create_project_in_marvin(self, project: MarvinProject) -> None:
        self.marvin.create_project_with_API(project)
