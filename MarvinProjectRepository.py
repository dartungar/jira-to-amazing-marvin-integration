from MarvinProject import MarvinProject
import json
from typing import List


class MarvinProjectsRepository:

    def __init__(self) -> None:
        self.repository: List[MarvinProject] = []

    def add(self, project: MarvinProject) -> None:
        self.repository.append(project)

    def populate_from_raw_data(self, raw_data: str) -> None:
        data = raw_data
        for entry in data:
            project = MarvinProject.from_object(entry)
            self.repository.append(project)

    def exists(self, key: str) -> bool:
        '''check if project with such issue key already exists'''
        for proj in self.repository:
            if key in proj.title:
                return True
        return False
