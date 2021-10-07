from Project.ProjectRepository import ProjectRepository
from Marvin.MarvinService import MarvinService
from Jira.JiraService import JiraService
from Settings import Settings

class ProjectService:
    '''A service for working with Projects, which can exist as Jira issue, Marvin project, or both.'''
    _repository: ProjectRepository
    _marvin: MarvinService
    _jira: JiraService

    def __init__(self, settings: Settings) -> None:
        self._repository = ProjectRepository()
        self._marvin = MarvinService(settings)
        self._jira = JiraService(settings)

    # TODO
    def sync(self) -> None:
        pass
    
    # TODO
    def check_assignees_for_existing_marvin_projects(self) -> None:
        pass

    

    

    