from unittest.mock import PropertyMock, patch, Mock

import pytest

from laa_court_data_api_app.internal.court_data_adaptor_client import CourtDataAdaptorClient
from laa_court_data_api_app.models.token_response import TokenResponse


def get_token_async():
    return TokenResponse(access_token="12345", token_type="Bearer", expires_in=300, created_at=1643981187)


test_codes = [(200, 200, get_token_async), (400, 400, get_token_async), (500, 500, get_token_async)]


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.config.court_data_adaptor.CdaSettings', new_callable=Mock)
@pytest.mark.parametrize("response_code,expected,token_function", test_codes)
async def test_get_request_returns_correctly(mock_settings, mock_cda_settings, mock_cda_client, mock_oauth_client,
                                             get_cda_env_vars, expected):
    mock_settings.return_value = get_cda_env_vars
    mock_cda_settings.return_value = get_cda_env_vars
    client = CourtDataAdaptorClient()
    response = await client.get("/get/")

    assert response.status_code == expected
    assert response.json() == []


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
@pytest.mark.parametrize("response_code,token_function", [(200, get_token_async)])
async def test_get_request_throws_exception(mock_settings, mock_cda_settings, mock_cda_client, mock_oauth_client,
                                            get_cda_env_vars):
    mock_settings.return_value = get_cda_env_vars
    mock_cda_settings.return_value = get_cda_env_vars
    client = CourtDataAdaptorClient()
    response = await client.get("/get/exception")

    assert response is None


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
@pytest.mark.parametrize("response_code,expected,token_function", test_codes)
async def test_post_request_returns_correctly(mock_settings, mock_cda_settings, mock_cda_client, mock_oauth_client,
                                              get_cda_env_vars, expected):
    mock_settings.return_value = get_cda_env_vars
    mock_cda_settings.return_value = get_cda_env_vars
    client = CourtDataAdaptorClient()
    response = await client.post("/post/")

    assert response.status_code == expected
    assert response.json() == []


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
@pytest.mark.parametrize("response_code,token_function", [(200, get_token_async)])
async def test_post_request_throws_exception(mock_settings, mock_cda_settings, mock_cda_client, mock_oauth_client,
                                             get_cda_env_vars):
    mock_settings.return_value = get_cda_env_vars
    mock_cda_settings.return_value = get_cda_env_vars
    client = CourtDataAdaptorClient()
    response = await client.get("/post/exception")

    assert response is None


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
@pytest.mark.parametrize("response_code,expected,token_function", test_codes)
async def test_patch_request_returns_correctly(mock_settings, mock_cda_settings, mock_cda_client, mock_oauth_client,
                                               get_cda_env_vars, expected):
    mock_settings.return_value = get_cda_env_vars
    mock_cda_settings.return_value = get_cda_env_vars
    client = CourtDataAdaptorClient()
    response = await client.patch("/patch/")

    assert response.status_code == expected
    assert response.json() == {}


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
@pytest.mark.parametrize("response_code,token_function", [(200, get_token_async)])
async def test_patch_request_throws_exception(mock_settings, mock_cda_settings, mock_cda_client, mock_oauth_client,
                                              get_cda_env_vars):
    mock_settings.return_value = get_cda_env_vars
    mock_cda_settings.return_value = get_cda_env_vars
    client = CourtDataAdaptorClient()
    response = await client.get("/patch/exception")

    assert response is None
