import json
from typing import List, Optional
from Settings import Settings


class MarvinTask:
    '''A representation of Marvin task'''

    parent_id: Optional[str]
    title: str
    tags: List[str]
    day: str
    review_date: str
    settings: Settings

    def __init__(self, parent_id: str, title: str, settings: Settings,  day: str, review_date: str, tags: List[str] = []) -> None:
        self.parent_id = parent_id
        self.title = title
        self.tags = tags
        self.day = day,
        self.review_date = review_date
        self.settings = settings

    def to_json(self) -> str:
        tag_appendix = f' @{" @".join(self.tags)}' if self.tags else ''
        task_data = {
            'parentId': self.parent_id,
            'title': self.title + tag_appendix,
            #'day': self.day or None,
            'reviewDate': self.review_date or None
        }
        return json.dumps(task_data, ensure_ascii=False)
