from Settings import Settings
from typing import List
from Marvin.MarvinApiService import MarvinApiService
import pytest
import asyncio


@pytest.fixture(scope="module")
def marvin_service():
    return MarvinApiService(settings=Settings())


@pytest.fixture(scope="module")
def raw_projects_data(marvin_service: MarvinApiService):
    data = asyncio.run(marvin_service.get_projects_data_from_API())
    return data


def test_setup(marvin_service: MarvinApiService):
    assert marvin_service.URL_HEADERS


def test_ping(marvin_service: MarvinApiService):
    status_code = asyncio.run(marvin_service.ping_for_status_code())
    assert status_code == 200


def test_get_raw_projects_data(raw_projects_data: List[dict]):
    assert len(raw_projects_data) > 0
    sample_project_data = raw_projects_data[0]
    assert 'title' in sample_project_data.keys()
    assert 'type' in sample_project_data.keys()
