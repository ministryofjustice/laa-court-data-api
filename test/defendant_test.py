from fastapi.testclient import TestClient
from laa_court_data_api_app.routers.defendant import get_defendant_by_urn
from laa_court_data_api_app.main import app

client = TestClient(app)


def override_get_defendant():
    # Need to create model for defendant response
    return {
        "defendantData": "true"
    }


app.dependency_overrides[get_defendant_by_urn] = override_get_defendant


def test_get_defendant_by_urn_returns_200():
    # Will we have /defendant with different logic depending on params or add extra
    # path such as /defendant/by_urn
    response = client.get('/defendant?urn=TEST12345')
    assert response.status_code == 200


def test_get_defendant_by_urn_returns_correct_body():
    response = client.get('/defendant?urn=TEST12345')
    expected_result = {"urn": "TEST12345"}
    assert response.json() == expected_result
