class JiraIssue:

    def __init__(self, key: str, title: str, status: str, assignee: str, estimate: int, priority: str, project: str, link: str) -> None:
        self.key: str = key
        self.title: str = title
        self.status: str = status
        self.assignee: str = assignee
        self.estimate: str = estimate * 1000 if estimate else None
        self.link: str = link,
        self.priority: str = priority,
        self.project: str = project

    @classmethod
    def from_raw_jira_issue_data(self, raw_issue_data: str, base_issue_url: str):
        return JiraIssue(
            key=raw_issue_data['key'],
            title=raw_issue_data['fields']['summary'],
            project=raw_issue_data['fields']['project']['name'],
            status=raw_issue_data['fields']['status']['name'],
            priority=raw_issue_data['fields']['priority']['name'],
            estimate=raw_issue_data['fields'].get(
                'timetracking').get('originalEstimateSeconds') if raw_issue_data['fields'].get(
                'timetracking') else None,
            link=base_issue_url +
            raw_issue_data['key'] if base_issue_url else '',
            assignee=raw_issue_data['fields']['assignee']['emailAddress']
        )
