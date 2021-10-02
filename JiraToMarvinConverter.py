from Jira.JiraIssue import JiraIssue
import Marvin


class JiraToMarvinConverter:

    def __init__(self) -> None:
        pass

    def marvin_project_from_jira_issue(self, issue: JiraIssue):
        from Marvin.MarvinProject import MarvinProject
        return MarvinProject(
            title=issue.key+' '+issue.title,
            note=issue.link[0],  # why do we have tuple here?
            estimate=issue.estimate or None,
        )

    def marvin_label_from_jira_issue_status(self, jira_status) -> str:
        pass

    def marvin_star_from_jira_priority(self, jira_priority) -> str:
        pass
