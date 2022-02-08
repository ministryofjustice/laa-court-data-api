from unittest.mock import Mock

from laa_court_data_api_app.internal import court_data_adaptor_client
from test.internal.internal_fixtures import *


async def get_token():
    return TokenResponse(access_token="12345", token_type="Bearer", expires_in=300, created_at=1643981187)


async def test_get_request_returns_correctly(mock_cda_client, get_cda_env_vars):
    oauth_client = Mock()
    oauth_client.retrieve_token.side_effect = get_token

    response = await court_data_adaptor_client.get("/get/", oauth_client=oauth_client, settings=get_cda_env_vars)

    assert response.status_code == 200
    assert response.json() == []


async def test_post_request_returns_correctly(mock_cda_client, get_cda_env_vars):
    oauth_client = Mock()
    oauth_client.retrieve_token.side_effect = get_token

    response = await court_data_adaptor_client.post("/post/", oauth_client=oauth_client, settings=get_cda_env_vars)

    assert response.status_code == 200
    assert response.json() == []


async def test_patch_request_returns_correctly(mock_cda_client, get_cda_env_vars):
    oauth_client = Mock()
    oauth_client.retrieve_token.side_effect = get_token

    response = await court_data_adaptor_client.patch("/patch/", oauth_client=oauth_client, settings=get_cda_env_vars)

    assert response.status_code == 200
    assert response.json() == {}
