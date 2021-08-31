import sys
import os
import base64
import requests
import json

JIRA_BASE_URL = 'https://treolan.atlassian.net/rest/api/3/issue/'
JIRA_API_KEY = os.getenv('JIRA_API_KEY')
MARVIN_URL = 'https://serv.amazingmarvin.com/api/createProject'
MARVIN_API_KEY = os.getenv('MARVIN_API_KEY')

issue_key = sys.argv[1]
print(issue_key)
if issue_key == "":
    raise ValueError("must provide Jira task key")

credentials = "d.nikolayev@treolan.ru:" + JIRA_API_KEY
encoded_credentials = base64.b64encode(credentials.encode())

url = JIRA_BASE_URL + issue_key
headers = {
    "Authorization": f"Basic {encoded_credentials}"
}
res = requests.get(url, headers=headers)

if res.status_code != 200:
    raise Exception(f"Error getting issue data from Jira: {res.content}")

issue_data = res.content

project_data = {
    "title": f"{issue_data.key} -  {issue_data.summary}",
    "day": None,
    "timeZoneOffset": 180
}


if MARVIN_API_KEY == "":
    raise ValueError("MARVIN_API_KEY env variable not found or empty")

headers = {
    'X-API-TOKEN': MARVIN_API_KEY
}

res_post = requests.post(MARVIN_URL, headers=headers, data=project_data)

print(res_post.content)
