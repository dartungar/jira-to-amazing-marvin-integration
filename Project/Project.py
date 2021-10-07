from typing import Optional
from Jira.JiraIssue import JiraIssue
from Project.JiraToMarvinConverter import JiraToMarvinConverter
from Marvin.MarvinProject import MarvinProject
from Settings import Settings


class Project:
    '''Representation of a project, which can exist as Jira issue, Marvin project, or both.'''
    settings: Settings
    project_key: str
    _marvin_project: MarvinProject
    _jira_issue: JiraIssue

    @property
    def marvin_project(self) -> MarvinProject:
        return self._marvin_project

    @marvin_project.setter
    def marvin_project(self, project: MarvinProject) -> None:
        if not self.jira_issue or self.jira_issue and self.jira_issue.key == project.jira_key:
            self._marvin_project = project
            return
        raise ProjectKeysMismatchException

    @property
    def jira_issue(self) -> JiraIssue:
        return self._jira_issue    

    @jira_issue.setter
    def jira_issue(self, issue: JiraIssue) -> None:
        if not self.marvin_project or self.marvin_project and self.marvin_project.jira_key == issue.key:
            self._jira_issue = issue
            return
        raise ProjectKeysMismatchException

    @property
    def needs_creating_in_marvin(self) -> bool:
        '''If Project is complete and marvin project has no marvin ID,
        then Marvin project exists only in the application and needs to be created in Marvin.
        '''
        if self.is_complete and not self.marvin_project.marvin_id:
            return True
        return False

    @property
    def jira_and_marvin_keys_match(self) -> bool:
        if self.is_complete and self.marvin_project.jira_key == self.jira_issue.key:
            return True
        return False

    @property
    def is_complete(self) -> bool:
        if self._marvin_project and self._jira_issue:
            return True
        return False

    @property
    def assignee_is_not_myself(self) -> bool:
        if not self.jira_and_marvin_keys_match:
            raise ProjectKeysMismatchException
        if self._jira_issue.assignee != self.settings.JIRA_USER_LOGIN:
            return True
        return False

    def add_marvin_project_for_jira_issue(self) -> None:
        project = JiraToMarvinConverter.marvin_project_from_jira_issue(self.jira_issue)
        self.marvin_project = project



class ProjectException(Exception):
    pass

class ProjectKeysMismatchException(ProjectException):
    pass
