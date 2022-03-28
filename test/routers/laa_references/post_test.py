import uuid
from unittest.mock import patch, PropertyMock

from fastapi.testclient import TestClient

from laa_court_data_api_app.internal.oauth_client import OauthClient
from laa_court_data_api_app.main import app

from ..fixtures import *

client = TestClient(app)


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_laa_references_post_returns_accepted(mock_settings, mock_cda_settings, override_get_cda_settings,
                                              mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings

    response = client.post("/v2/laa_references",
                           data=LaaReferencesPost(user_name="pass-u", maat_reference=1234567).json())

    assert response.status_code == 202
    assert response.content == b''
    assert mock_cda_client["laa_references_post_pass_route"].called


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_laa_references_post_returns_bad_request(mock_settings, mock_cda_settings, override_get_cda_settings,
                                                 mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings

    response = client.post("/v2/laa_references",
                           data=LaaReferencesPost(user_name="fail-u", maat_reference=1234567).json())

    assert response.status_code == 400
    assert mock_cda_client["laa_references_post_fail_route"].called
    assert response.content == b'{"errors":{"maat_reference":["3141592 has no common platform data created against Maat application."]}}'


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_laa_references_post_returns_not_found(mock_settings, mock_cda_settings, override_get_cda_settings,
                                               mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings

    response = client.post("/v2/laa_references",
                           data=LaaReferencesPost(user_name="notfound-u", maat_reference=1234567).json())

    assert response.status_code == 404
    assert response.content == b''
    assert mock_cda_client["laa_references_post_not_found_route"].called


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_laa_references_post_returns_unprocessable_entity(mock_settings, mock_cda_settings, override_get_cda_settings,
                                                          mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings

    response = client.post("/v2/laa_references",
                           data=LaaReferencesPost(user_name="unprocessable-u", maat_reference=1234567).json())

    assert response.status_code == 422
    assert mock_cda_client["laa_references_post_unprocessable_entity_route"].called
    assert response.content == b'{"errors":{"maat_reference":["3141592 has no common platform data created against Maat application."]}}'


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_laa_references_post_returns_server_error(mock_settings, mock_cda_settings, override_get_cda_settings,
                                                  mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings

    response = client.post("/v2/laa_references",
                           data=LaaReferencesPost(user_name="servererror-u", maat_reference=1234567).json())

    assert response.status_code == 424
    assert response.content == b''
    assert mock_cda_client["laa_references_post_server_error_route"].called


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_laa_references_post_returns_none(mock_settings, mock_cda_settings, override_get_cda_settings,
                                          mock_cda_client):
    OauthClient().token = None
    mock_cda_settings.return_value = CdaSettings(cda_endpoint="http://failed-test-url/", cda_secret="12345",
                                                 cda_uid="12345")
    mock_settings.return_value = override_get_cda_settings

    response = client.post("/v2/laa_references",
                           data=LaaReferencesPost(user_name="test-u", maat_reference=1234567).json())

    assert response.status_code == 424
    assert response.content == b''
    assert mock_cda_client["failed_token_endpoint"].called
