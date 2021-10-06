from typing import Optional
from Jira.JiraIssue import JiraIssue
from Marvin.MarvinProject import MarvinProject
from Settings import Settings


class Project:
    '''Representation of a project, which can exist as Jira issue, Marvin project, or both.'''
    settings: Settings
    project_key: str
    _marvin_project: Optional[MarvinProject]
    _jira_issue: Optional[JiraIssue]

    @property
    def assignee_is_not_myself(self) -> bool:
        if self._marvin_project and self._jira_issue and self._marvin_project.jira_key != self._jira_issue.key:
            raise ProjectException(
                "Jira key must be similar in Jira issue and Marvin project")
        if self._jira_issue.assignee != self.settings.JIRA_USER_LOGIN:
            return True
        return False


class ProjectException(Exception):
    pass
