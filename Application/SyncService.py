from Marvin.MarvinProjectRepository import MarvinProjectsRepository
from Settings import Settings
from Marvin.MarvinApiService import MarvinApiService
from Marvin.MarvinProject import MarvinProject
from Marvin.MarvinTask import MarvinTask
from Jira.JiraService import JiraService
import logging

logging.basicConfig(level=logging.INFO)


class SyncService:
    settings: Settings
    project_repository: MarvinProjectsRepository
    marvin_api_service: MarvinApiService
    jira_service: JiraService

    def __init__(self) -> None:
        self.settings = Settings()
        self.project_repository = MarvinProjectsRepository()
        self.marvin_api_service = MarvinApiService(self.settings)
        self.jira_service = JiraService(self.settings)

    def sync(self) -> None:
        logging.info("starting sync...")
        self.populate_project_repository()
        projects_to_create = self.project_repository.not_synced_projects
        self.marvin_api_service.create_projects_with_api(projects_to_create)
        logging.info("done syncing.")

    def create_remider_tasks_for_projects_with_changed_assignees(self) -> None:
        logging.info("starting creating reminder tasks for projects with changed assignees...")
        self.populate_project_repository()
        projects_to_create_tasks_for = self.project_repository.projects_with_changed_assignees
        if projects_to_create_tasks_for:
            for project in projects_to_create_tasks_for:
                self.create_task_in_marvin_for_project(project)
            logging.info(f"created reminder tasks for {len(projects_to_create_tasks_for)} projects.")
            return
        logging.info("found no projects with changed assignees.")

    def populate_project_repository(self) -> None:
        logging.info("populating project repository from Marvin & Jira...")
        self.project_repository.clear()
        self.get_and_add_projects_from_marvin()
        self.get_and_add_issues_from_jira()
        logging.info("done populating project repository.")

    def get_and_add_projects_from_marvin(self) -> None:
        '''Fetches projects from Marvin and adds to the repository.'''
        logging.info("fetching projects from Marvin and adding to the repository...")
        try:
            data = self.marvin_api_service.get_projects_data_from_API()
            self.project_repository.populate_from_raw_data(data)
            logging.info(f"fetched {len(data)} projects from Marvin.")
        except Exception as e:  # TODO: catch specific error
            raise MainServiceException(
                f'Error populating Marvin projects repository from API: {e}')

    def get_and_add_issues_from_jira(self, current_user_only=False) -> None:
        '''Fetches issues data from Jira and adds to the repository.'''
        logging.info("fetching issues from Jira and adding to the repository...")
        try:
            issues = self.jira_service.get_issues_from_jira(current_user_only)
            self.project_repository.add_multiple_from_jira_issues(issues)
            logging.info(f"fetched {len(issues)} issues from Jira.")
        except Exception as e:
            raise MainServiceException(e)

    def create_task_in_marvin_for_project(self, project: MarvinProject) -> None:
        logging.info("creating task in Marvin...")
        task = MarvinTask(project.marvin_id,
                          "Контроль по задаче в Jira", self.settings)
        self.marvin_api_service.create_task_with_api(task)


class MainServiceException(ValueError):
    pass
