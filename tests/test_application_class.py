from Marvin.MarvinProjectRepository import MarvinProjectsRepository
from Jira.JiraIssueRepository import JiraIssueRepository
from Marvin.MarvinService import MarvinService
from Jira.JiraService import JiraService
from Application import Application
import pytest


@pytest.fixture(scope="module")
def application_object():
    return Application()


def test_application_init(application_object):
    assert isinstance(application_object.jira, JiraService)
    assert isinstance(application_object.marvin, MarvinService)
    assert isinstance(application_object.issues_repository,
                      JiraIssueRepository)
    assert isinstance(
        application_object.existing_projects_repository, MarvinProjectsRepository)
