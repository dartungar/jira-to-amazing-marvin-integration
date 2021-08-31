# Jira to Amazing Marvin

Get tasks (issues) from Jira and add them into Amazing Marvin as projects.

Requires .env file with variables:
JIRA_BASE_API_URL - base URL for getting issue data, i.e https://yourcompany.atlassian.net/rest/api/3/issue/
JIRA_API_KEY
JIRA_BASE_TASK_URL - base URL for building link to task, i.e https://yourcompany.atlassian.net/browse/
JIRA_EMAIL - your Jira account e-mail, used to recognize you as assignee
MARVIN_ADD_PROJECT_URL - Marvin API endpoing for adding tasks, currently https://serv.amazingmarvin.com/api/addProject
MARVIN_API_KEY
