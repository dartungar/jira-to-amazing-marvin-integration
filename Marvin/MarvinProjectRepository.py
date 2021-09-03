from Marvin.MarvinProject import MarvinProject
from typing import List


class MarvinProjectsRepository:

    def __init__(self) -> None:
        self.data: List[MarvinProject] = []

    def add(self, project: MarvinProject) -> None:
        self.data.append(project)

    def populate_from_raw_data(self, raw_data: str) -> None:
        '''populate from an array of dicts'''
        for entry in raw_data:
            project = MarvinProject.from_object(entry)
            self.add(project)

    def exists_by_key(self, key: str) -> bool:
        '''check if project with such issue key already exists'''
        for proj in self.data:
            if key in proj.title:
                return True
        return False

    def exists_by_project(self, project: MarvinProject) -> bool:
        '''check if project with such title already exists'''
        for proj in self.data:
            if project.title == proj.title:
                return True
        return False
