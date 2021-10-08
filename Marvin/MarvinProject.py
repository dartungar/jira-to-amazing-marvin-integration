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
    _jira_issue: JiraIssue

    settings: Settings = Settings()

    def __init__(self,
                 marvin_id: Optional[str],
                 title: str,
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
    def jira_issue(self) -> None:
        return self._jira_issue

    @jira_issue.setter
    def jira_issue(self, issue: JiraIssue) -> None:
        if self.key and issue.key != self.key:
            raise ProjectKeysMismatchException
        self._jira_issue = issue

    @property
    def current_user_is_assignee_in_jira(self) -> bool:
        return self._jira_issue.assignee == self.settings.JIRA_USER_LOGIN

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


class ProjectKeysMismatchException(Exception):
    pass
