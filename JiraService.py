import os
import requests
import base64
import re


class JiraService:

    # config variables
    BASE_API_URL: str = os.getenv('JIRA_BASE_API_URL')
    API_KEY: str = os.getenv('JIRA_API_KEY')
    credentials_unencoded = ':'.join(
        [os.getenv('JIRA_EMAIL'), API_KEY])
    CREDENTIALS: str = base64.b64encode(
        credentials_unencoded.encode())
    URL_HEADERS: object = {
        "Authorization": b"Basic " + CREDENTIALS}

    def get_raw_task_data(self, key: str) -> object:
        response = requests.get(self.BASE_API_URL + key,
                                headers=self.URL_HEADERS)
        if not response.ok:
            raise ValueError(f"Invalid response from Jira: {response.code}")
        return response.json()

    def get_task_keys_from_string(self, string: str) -> set:
        key_regex = re.compile(r'[A-Z]{2,6}-[1-9][0-9]{0,4}')
        return set(key_regex.findall(string))
