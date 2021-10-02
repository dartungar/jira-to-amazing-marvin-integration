from typing import List
from Jira.JiraIssue import JiraIssue


class JiraIssueRepository:

    def __init__(self) -> None:
        self.data: List[JiraIssue] = []

    @property
    def issues_keys(self):
        return [issue.key for issue in self.data]

    def add(self, issue: JiraIssue) -> None:
        self.data.append(issue)

    def populate_from_raw_data(self, raw_data: List, base_issue_url) -> None:
        for raw_issue in raw_data:
            self.add(JiraIssue.from_raw_jira_issue_data(
                raw_issue, base_issue_url))
