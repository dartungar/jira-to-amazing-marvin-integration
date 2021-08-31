class JiraTask:
    import os
    JIRA_BASE_TASK_URL: str = os.getenv('JIRA_BASE_TASK_URL')

    def __init__(self, key: str, title: str, status: str, assignee: str, estimate: str, priority: str, project: str, link: str) -> None:
        self.key: str = key
        self.title: str = title
        self.status: str = status
        self.assignee: str = assignee
        self.estimate: str = estimate
        self.link: str = link,
        self.priority: str = priority,
        self.project: str = project

    @classmethod
    def from_raw_jira_task_data(self, raw_task_data):
        return JiraTask(
            key=raw_task_data['key'],
            title=raw_task_data['fields']['summary'],
            project=raw_task_data['fields']['project']['name'],
            status=raw_task_data['fields']['status']['name'],
            priority=raw_task_data['fields']['priority']['name'],
            estimate=raw_task_data['fields']['timetracking']['originalEstimate'],
            link=self.JIRA_BASE_TASK_URL + raw_task_data['key'],
            assignee=raw_task_data['fields']['assignee']['emailAddress']
        )
