# TODO: MarvinProject не должен зависеть от JiraTask
from typing import Optional
from Jira.JiraService import JiraService
from Settings import Settings
from Jira.JiraIssue import JiraIssue
from Utils.parsers import get_single_issue_key_from_string
import json
from typing import List


class MarvinProject:
    '''a representation of Marvin project'''
    title: str
    marvin_id: Optional[str]
    key: str
    parent_id: Optional[str]
    note: Optional[str]
    day: Optional[str]
    time_estimate: Optional[int]
    tags: List[str]
    _jira_issue: Optional[JiraIssue] = None

    settings: Settings = Settings()

    def __init__(self,
                 title: str,
                 marvin_id: Optional[str] = None,
                 parent_id: str = None,
                 note: str = None,
                 day: str = None,
                 estimate: int = None,
                 tags: list = settings.MARVIN_DEFAULT_TAGS) -> None:

        self.title = title
        self.marvin_id = marvin_id
        self.key = get_single_issue_key_from_string(title)
        self.parent_id = parent_id
        self.note = note
        self.day = day
        self.time_estimate = estimate
        self.tags = tags

    @property
    def jira_issue(self) -> JiraIssue:
        return self._jira_issue

    @jira_issue.setter
    def jira_issue(self, issue: JiraIssue) -> None:
        if self.key and issue.key != self.key:
            raise ProjectKeysMismatchException
        self._jira_issue = issue

    @property
    def needs_syncing(self) -> bool:
        return self.jira_issue and self.jira_issue.assignee == self.settings.JIRA_USER_LOGIN and not self.marvin_id

    @property
    def assignee_is_changed(self) -> bool:
        print(f"{self.key} - {self.jira_issue.assignee if self.jira_issue else 'No assignee'}")
        if self._jira_issue and self.marvin_id:
            return self._jira_issue.assignee != self.settings.JIRA_USER_LOGIN
        # if project has no associated Jira issue and no key, it does not have to have an assignee
        return False

    def to_json(self) -> str:
        # add tags in title because labelIds param does not seem to work in API
        # also, tag names are much more convenient for simple usage
        tag_appendix = f' @{" @".join(self.tags)}' if self.tags else ''

        project_data = {
            'title': self.title + tag_appendix,
            'parentId': self.parent_id,
            'note': self.note,
            'day': self.day,
            'timeEstimate': self.time_estimate,
            'timeZoneOffset': self.settings.MARVIN_TIMEZONE_OFFSET_MINUTES
        }
        return json.dumps(project_data, ensure_ascii=False)


class MarvinProjectException(Exception):
    pass


class ProjectKeysMismatchException(Exception):
    pass
