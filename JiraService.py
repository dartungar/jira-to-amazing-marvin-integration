import os
import requests
import base64
import re
import json


class JiraService:

    # config variables
    API_URL_GET_TASK: str = os.getenv('JIRA_API_URL_GET_TASK')
    API_URL_GET_TASKS: str = os.getenv('JIRA_API_URL_GET_TASKS')
    API_KEY: str = os.getenv('JIRA_API_KEY')
    credentials_unencoded = ':'.join(
        [os.getenv('JIRA_EMAIL'), API_KEY])
    CREDENTIALS: str = base64.b64encode(
        credentials_unencoded.encode())
    URL_HEADERS: object = {
        "Authorization": b"Basic " + CREDENTIALS}
    DEFAULT_ASSIGNEE = 'currentUser()'

    def get_raw_task_data(self, key: str) -> object:
        response = requests.get(self.BASE_API_URL + key,
                                headers=self.URL_HEADERS)
        if not response.ok:
            raise JiraServiceError(
                f"Error getting task data from Jira: {response.code}")
        return json.loads(response.json())

    def get_task_keys_from_string(self, string: str) -> set:
        key_regex = re.compile(r'[A-Z]{2,6}-[1-9][0-9]{0,4}')
        return set(key_regex.findall(string))

    # TODO: projects, status
    def get_raw_tasks_data(self, assignee=DEFAULT_ASSIGNEE, status=None, projects=None) -> object:
        jql = ""
        if assignee or status:
            jql = f'assignee = {assignee}'
            # tasks must be not done
            jql += ' AND statusCategory != Done'
        response = requests.get(self.API_URL_GET_TASKS,
                                params={
                                    "jql": jql if jql else None},
                                headers=self.URL_HEADERS)
        if not response.ok:
            raise JiraServiceError(
                f"Error getting all tasks data from Jira: {response.json()}")
        return response.json()


class JiraServiceError(ValueError):
    pass
