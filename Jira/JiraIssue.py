from typing import Optional
from dataclasses import dataclass


@dataclass(init=True)
class JiraIssue:
    key: str
    title: str
    status: str
    assignee: str
    estimate: Optional[int]
    link: str
    priority: str
    project: str
    has_subtasks: bool

    def __init__(self, key: str, title: str, status: str, assignee: str, estimate: int, priority: str, project: str, link: str, has_subtasks: bool) -> None:
        self.key = key
        self.title = title
        self.status = status
        self.assignee = assignee
        self.estimate = estimate * 1000 if estimate else None
        self.link = link,
        self.priority = priority,
        self.project = project,
        self.has_subtasks = has_subtasks
