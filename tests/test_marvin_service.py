from Settings import Settings
from typing import List
from Marvin.MarvinService import MarvinService
import pytest


@pytest.fixture(scope="module")
def marvin_service():
    return MarvinService(settings=Settings())


@pytest.fixture(scope="module")
def raw_projects_data(marvin_service: MarvinService):
    return marvin_service.get_projects_data_from_API()


def test_setup(marvin_service: MarvinService):
    assert marvin_service.URL_HEADERS


def test_ping(marvin_service: MarvinService):
    assert marvin_service.ping_for_status_code() == 200


def test_get_raw_projects_data(raw_projects_data: List[dict]):
    assert len(raw_projects_data) > 0
    sample_project_data = raw_projects_data[0]
    assert 'title' in sample_project_data.keys()
    assert 'type' in sample_project_data.keys()
