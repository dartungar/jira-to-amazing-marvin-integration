

from typing import List
from Project.Project import Project


class ProjectRepository:
    '''Repository for Projects'''
    data: List[Project]

    def clear(self) -> None:
        self.data.clear()

    def add(self, project: Project) -> None:
        self.data.append(project)

    def get_by_key(self, jira_key: str) -> Project:
        try:
            return [p for p in self.data if p.project_key == jira_key][0]
        except IndexError:
            raise IndexError
