from typing import List
from Project.Project import Project
from Marvin.MarvinProject import MarvinProject
from Jira.JiraIssue import JiraIssue


class ProjectRepository:
    '''Repository for Projects'''
    data: List[Project]

    @property
    def projects_to_create_in_marvin(self) -> List[Project]:
        return [p for p in self.data if p.needs_creating_in_marvin]

    def clear(self) -> None:
        self.data.clear()

    def add(self, project: Project) -> None:
        self.data.append(project)

    def add_marvin_project(self, marvin_project: MarvinProject) -> None:
        '''Adds marvin project to existing Project or creates a new Project.'''
        project = self.get_by_key(marvin_project.jira_key)
        if not project:
            project = Project()
            project.marvin_project = marvin_project
        self.add(project)

    def add_jira_issue(self, issue: JiraIssue) -> None:
        '''Adds jira issue to existing Project or creates a new Project.'''
        project = self.get_by_key(issue.key)
        if not project:
            project = Project()
            project.jira_issue = issue
        self.add(project)

    def get_by_key(self, jira_key: str) -> Project:
        try:
            return [p for p in self.data if p.project_key == jira_key][0]
        except IndexError:
            return None

    
