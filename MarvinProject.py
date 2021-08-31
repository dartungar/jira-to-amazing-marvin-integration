from JiraTask import JiraTask
from JiraToMarvinConverter import JiraToMarvinConverter
import json


class MarvinProject:
    converter = JiraToMarvinConverter()
    TIMEZONE_OFFSET = 180  # разница в часовых поясах с GMT+00, в минутах
    DEFAULT_TAGS = ["upcoming"]

    def __init__(self, title: str, parentId: int = None, note: str = None, day: str = None, estimate: int = None, tags: list = None) -> None:
        self.title = title
        self.parentId = parentId
        self.note = note
        self.day = day
        self.timeEstimate = estimate
        self.timeZoneOffset = self.TIMEZONE_OFFSET
        self.tags = tags if tags else self.DEFAULT_TAGS

    @classmethod
    def from_jira_task(self, jiraTask: JiraTask):
        return MarvinProject(
            title=jiraTask.key+' '+jiraTask.title,
            note=jiraTask.link[0],  # why do we have tuple here?
            estimate=None
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
        tag_appendix = f' @{" @".join(self.tags)}'
        # add estimate in title because format for adding in title matches jira's
        estimate_appendix = f' ~{self.timeEstimate}'

        project_data = {
            'title': self.title + tag_appendix + estimate_appendix,
            'parentId': self.parentId,
            'note': self.note,
            # 'labelIds': self.tagIds, # does not seem to work in API
            'day': self.day,
            # 'timeEstimate': self.timeEstimate,
            'timeZoneOffset': self.timeZoneOffset
        }
        return json.dumps(project_data, ensure_ascii=False)
