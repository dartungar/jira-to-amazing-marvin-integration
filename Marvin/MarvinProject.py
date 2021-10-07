# TODO: MarvinProject не должен зависеть от JiraTask
from typing import Optional
from Jira.JiraService import JiraService
from Settings import Settings
from Jira.JiraIssue import JiraIssue
import json
from dataclasses import dataclass
from typing import List


@dataclass
class MarvinProject:
    '''a representation of Marvin project'''
    title: str
    marvin_id: str
    jira_key: str
    parent_id: str
    note: str
    day: str
    time_estimate: str
    tags: List[str]

    settings: Settings = Settings()

    def __init__(self,
                 marvin_id: Optional[str],
                 title: str,
                 parentId: int = None,
                 note: str = None,
                 day: str = None,
                 estimate: int = None,
                 tags: list = settings.MARVIN_DEFAULT_TAGS) -> None:

        self.title = title
        self.marvin_id = marvin_id
        self.jira_key = JiraService.get_single_issue_key_from_string(title)
        self.parentId = parentId
        self.note = note
        self.day = day
        self.timeEstimate = estimate
        self.tags = tags

    def to_json(self) -> str:
        # add tags in title because labelIds param does not seem to work in API
        # also, tag names are much more convenient for simple usage
        tag_appendix = f' @{" @".join(self.tags)}' if self.tags else ''

        project_data = {
            'title': self.title + tag_appendix,
            'parentId': self.parentId,
            'note': self.note,
            'day': self.day,
            'timeEstimate': self.timeEstimate,
            'timeZoneOffset': self.settings.MARVIN_TIMEZONE_OFFSET_MINUTES
        }
        return json.dumps(project_data, ensure_ascii=False)
