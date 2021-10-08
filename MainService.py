from Marvin.MarvinProjectRepository import MarvinProjectsRepository
from Settings import Settings
from Marvin.MarvinApiService import MarvinApiService
from Marvin.MarvinProject import MarvinProject
from Marvin.MarvinTask import MarvinTask
from Jira.JiraService import JiraService


class MainService:
    settings: Settings
    project_repository: MarvinProjectsRepository
    marvin_api_service: MarvinApiService
    jira_service: JiraService

    def __init__(self) -> None:
        self.settings = Settings()
        self.marvin_api_service = MarvinApiService(self.settings)
        self.jira_service = JiraService(self.settings)

    def sync(self) -> None:
        self.populate_project_repository()
        projects_to_create = self.project_repository.not_synced_projects
        self.marvin_api_service.create_projects_with_api(projects_to_create)

    def create_remider_tasks_for_projects_with_changed_issue_assignees(self) -> None:
        self.populate_project_repository()
        for project in self.project_repository.projects_with_changed_assignees:
            self.create_task_in_marvin_for_project(project)

    def populate_project_repository(self) -> None:
        self.project_repository.clear()
        self.get_and_add_projects_from_marvin()
        self.get_and_add_issues_from_jira()

    def get_and_add_projects_from_marvin(self) -> None:
        '''Fetches projects from Marvin and adds to the repository.'''
        try:
            data = self.marvin_api_service.get_projects_data_from_API()
            self.project_repository.repository.populate_from_raw_data(data)
        except Exception as e:  # TODO: catch specific error
            raise MainServiceException(
                f'Error populating Marvin projects repository from API: {e}')

    def get_and_add_issues_from_jira(self) -> None:
        '''Fetches issues data from Jira and adds to the repository.'''
        try:
            issues = self.jira_service.get_issues_from_jira()
            self.project_repository.add_multiple_from_jira_issues(issues)
        except Exception as e:
            raise MainServiceException(e)

    def create_task_in_marvin_for_project(self, project: MarvinProject) -> None:
        task = MarvinTask(project.marvin_id,
                          "Контроль по задаче в Jira", self.settings)
        self.marvin_api_service.create_task_with_api(task)


class MainServiceException(ValueError):
    pass
