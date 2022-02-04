from fastapi import Depends
from fastapi.testclient import TestClient
from laa_court_data_api_app.config.app import get_app_settings
from laa_court_data_api_app.main import app
from laa_court_data_api_app.routers.ping import router
import os

client = TestClient(app)


class OverrideAppSettings:
    commit_id = '123456'
    build_date = '02022022'
    build_tag = 'test'
    app_branch = 'test_branch'


def override_get_app_settings():
    return OverrideAppSettings


app.dependency_overrides[get_app_settings] = override_get_app_settings


def test_ping_returns_200():
    response = client.get('/ping')
    assert response.status_code == 200


def test_ping_returns_correct_body():
    response = client.get('/ping')
    expected_result = {'app_branch': 'test_branch',
                       'build_date': '02022022',
                       'build_tag': 'test',
                       'commit_id': '123456'}
    assert response.json() == expected_result
