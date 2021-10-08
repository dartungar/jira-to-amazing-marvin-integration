from Jira.JiraIssue import JiraIssue
from Marvin.MarvinProject import MarvinProject


class JiraToMarvinConverter:

    def __init__(self) -> None:
        pass

    @classmethod
    def marvin_project_from_jira_issue(self, issue: JiraIssue):
        try:
            project = MarvinProject(
                title=issue.key+' '+issue.title,
                note=issue.link[0],  # why do we have tuple here?
                estimate=issue.estimate or None,
            )
            project.jira_issue = issue
            return project
        except Exception as e:
            return JiraToMarvinTransformationException(e)

    def marvin_label_from_jira_issue_status(self, jira_status) -> str:
        pass

    def marvin_star_from_jira_priority(self, jira_priority) -> str:
        pass


class JiraToMarvinTransformationException(Exception):
    pass
