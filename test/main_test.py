from fastapi.testclient import TestClient
from laa_court_data_api_app.main import app
from laa_court_data_api_app.routers.something import router
from laa_court_data_api_app.config.app import get_app_settings
import os

client = TestClient(app)


def test_root_returns_200():
    response = client.get('/')
    assert response.status_code == 200

def test_root_returns_correct_body():
    response = client.get('/')
    assert response.json() == {'Status': 'Working'}

def test_ping_returns_200():
    response = client.get('/ping')
    assert response.status_code == 200

def test_ping_returns_correct_body():
    get_app_settings.cache_clear()
    os.environ["COMMIT_ID"] = '123456'
    os.environ["BUILD_DATE"] = '02022022'
    os.environ["BUILD_TAG"] = 'test'
    os.environ["APP_BRANCH"] = 'test_branch'
    settings = get_app_settings()

    response = client.get('/ping')
    expected_result = {'app_branch': 'test_branch',
               'build_date': '02022022',
               'build_tag': 'test',
               'commit_id': '123456'}
    assert response.json() == expected_result
