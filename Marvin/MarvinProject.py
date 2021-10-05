# TODO: MarvinProject не должен зависеть от JiraTask
from typing import Optional
from Jira.JiraService import JiraService
from Settings import Settings
from Jira.JiraIssue import JiraIssue
import json


class MarvinProjectStatuses:
    '''possible statuses of Jira-Marvin synchronization '''
    synced = 0
    exists_only_in_marvin = 1
    exists_only_in_jira = 2
    not_defined = 3


class MarvinProject:
    '''a representation of Marvin project'''
    from JiraToMarvinConverter import JiraToMarvinConverter

    settings: Settings = Settings()
    converter = JiraToMarvinConverter()

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
        self.sync_status = MarvinProjectStatuses.not_defined

    @classmethod
    def from_jira_issue(self, jira_issue: JiraIssue):
        return self.converter.marvin_project_from_jira_issue(jira_issue)

    @classmethod
    def from_object(self, obj: dict):
        return MarvinProject(
            marvin_id=obj['_id'],
            title=obj['title'],
            parentId=obj['parentId'],
            tags=obj.get('labelIds') or []
        )

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
