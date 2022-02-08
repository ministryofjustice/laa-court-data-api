from laa_court_data_api_app.internal import court_data_adaptor_client
from test.internal.internal_fixtures import *


async def test_get_request_returns_correctly(mock_cda_client, mock_oauth_client, get_cda_env_vars):
    response = await court_data_adaptor_client.get("/get/", oauth_client=mock_oauth_client, settings=get_cda_env_vars)

    assert response.status_code == 200
    assert response.json() == []


async def test_post_request_returns_correctly(mock_cda_client, mock_oauth_client, get_cda_env_vars):
    response = await court_data_adaptor_client.post("/post/", oauth_client=mock_oauth_client, settings=get_cda_env_vars)

    assert response.status_code == 200
    assert response.json() == []


async def test_patch_request_returns_correctly(mock_cda_client, mock_oauth_client, get_cda_env_vars):
    response = await court_data_adaptor_client.patch("/patch/", oauth_client=mock_oauth_client, settings=get_cda_env_vars)

    assert response.status_code == 200
    assert response.json() == {}
