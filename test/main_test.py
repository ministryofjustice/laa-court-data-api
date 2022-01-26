from fastapi.testclient import TestClient

from laa_court_data_api_app.main import app

client = TestClient(app)


def test_root_returns_200():
    response = client.get('/')
    assert response.status_code == 200


def test_root_returns_correct_body():
    response = client.get('/')
    assert response.json() == {'Status': 'Working'}
