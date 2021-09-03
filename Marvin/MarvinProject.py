# TODO: MarvinProject не должен зависеть от JiraTask
from Jira.JiraIssue import JiraIssue
from JiraToMarvinConverter import JiraToMarvinConverter
import json


class MarvinProject:
    converter = JiraToMarvinConverter()
    # difference between GMT+0 and your timezone
    TIMEZONE_OFFSET_MINUTES = 180  # GMT+3
    DEFAULT_TAGS = ["upcoming"]

    def __init__(self, title: str, parentId: int = None, note: str = None, day: str = None, estimate: int = None, tags: list = None) -> None:
        self.title = title
        self.parentId = parentId
        self.note = note
        self.day = day
        self.timeEstimate = estimate
        self.timeZoneOffset = self.TIMEZONE_OFFSET_MINUTES
        self.tags = tags if tags else self.DEFAULT_TAGS

    @classmethod
    def from_jira_issue(self, jira_issue: JiraIssue):
        return MarvinProject(
            title=jira_issue.key+' '+jira_issue.title,
            note=jira_issue.link[0],  # why do we have tuple here?
            estimate=jira_issue.estimate or None
        )

    @classmethod
    def from_object(self, obj: object):
        return MarvinProject(
            title=obj['title'],
            parentId=obj['parentId'],
            tags=obj.get('labelIds')
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
            'timeZoneOffset': self.timeZoneOffset
        }
        return json.dumps(project_data, ensure_ascii=False)
