import os
from Jira.JiraIssue import JiraIssue
from Jira.JiraService import JiraService
import pytest


@pytest.fixture(scope='module')
def jira_service():
    jira = JiraService()
    print(os.getenv('JIRA_EMAIL'))

    return jira


@pytest.fixture(scope='module')
def test_issue_data(jira_service: JiraService) -> dict:
    return jira_service.get_raw_issue_data_by_key('BB-10300')


def test_setup(jira_service: JiraService):
    assert isinstance(jira_service.API_URL_GET_TASK, str)
    assert isinstance(jira_service.API_URL_GET_TASK, str)
    assert isinstance(jira_service.API_KEY, str)
    assert isinstance(jira_service.URL_HEADERS, dict)


def test_get_single_issue_data(jira_service: JiraService):
    data = jira_service.get_raw_issue_data_by_key('BB-10300')
    assert isinstance(data, dict)


def test_issue_data_shape(test_issue_data: dict):
    data = test_issue_data
    assert 'key' in data.keys()
    assert 'fields' in data.keys()
    assert 'summary' in data['fields'].keys()
    assert 'project' in data['fields'].keys()
    assert 'name' in data['fields']['project'].keys()
    assert 'status' in data['fields'].keys()
    assert 'name' in data['fields']['status'].keys()
    assert 'assignee' in data['fields'].keys()


def test_from_raw_data(test_issue_data: dict, jira_service: JiraService):
    issue = JiraIssue.from_raw_jira_issue_data(
        test_issue_data, jira_service.JIRA_BASE_ISSUE_URL)
    assert issue.key
    assert issue.title
    assert issue.status
    assert issue.assignee
    assert issue.link
    assert issue.priority
    assert issue.project
