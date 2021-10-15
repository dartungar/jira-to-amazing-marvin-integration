from Jira.JiraIssue import JiraIssue
from Marvin.MarvinProject import MarvinProject
from typing import List
from Marvin.JiraToMarvinConverter import JiraToMarvinConverter


class MarvinProjectsRepository:

    def __init__(self) -> None:
        self.data: List[MarvinProject] = []

    def add(self, project: MarvinProject) -> None:
        self.data.append(project)

    def clear(self) -> None:
        self.data.clear()

    def get_by_jira_key(self, jira_key: str) -> MarvinProject:
        try:
            return [p for p in self.data if p.key == jira_key][0]
        except IndexError:
            raise IndexError


