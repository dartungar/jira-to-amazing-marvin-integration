from Settings import Settings
from Marvin.MarvinProjectRepository import MarvinProjectsRepository
from Jira.JiraService import JiraService
from Application import Application
import pytest


@pytest.fixture(scope="module")
def application_object():
    return Application()


def test_application_init(application_object):
    assert isinstance(application_object.settings, Settings)
    assert isinstance(application_object.jira, JiraService)
    assert isinstance(
        application_object.projects_repository, MarvinProjectsRepository)
