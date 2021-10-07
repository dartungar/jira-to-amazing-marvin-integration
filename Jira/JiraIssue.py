from typing import Optional
from dataclasses import dataclass

@dataclass
class JiraIssue:
    key: str
    title: str
    status: str
    assignee: str
    estimate: int
    link: str
    priority: str
    project: str

    def __init__(self, key: str, title: str, status: str, assignee: str, estimate: int, priority: str, project: str, link: str) -> None:
        self.key: str = key
        self.title: str = title
        self.status: str = status
        self.assignee: str = assignee
        self.estimate: int = estimate * 1000 if estimate else None
        self.link: str = link,
        self.priority: str = priority,
        self.project: str = project


