from unittest.mock import patch, PropertyMock

from fastapi.testclient import TestClient

from laa_court_data_api_app.internal.oauth_client import OauthClient
from laa_court_data_api_app.main import app
from ..routers.fixtures import *

client = TestClient(app)


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_hearing_returns_ok(mock_settings, mock_cda_settings, override_get_cda_settings,
                            mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings
    response = client.get("/v2/hearing/00d0000c-00ff-00ec-b000-0000ac000000")

    assert response.status_code == 200
    assert mock_cda_client["pass_hearing_route"].called
    model = HearingResult(**response.json())
    assert model.hearing.jurisdiction_type == "test"


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_hearing_returns_bad_request(mock_settings, mock_cda_settings, override_get_cda_settings,
                                     mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings
    response = client.get("/v2/hearing/00d0000c-00ff-00ec-b000-0000ac000001")

    assert response.status_code == 400
    assert mock_cda_client["fail_hearing_route"].called
    assert response.content == b''


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_hearing_returns_not_found(mock_settings, mock_cda_settings, override_get_cda_settings,
                                   mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings
    response = client.get("/v2/hearing/00d0000c-00ff-00ec-b000-0000ac000002")

    assert response.status_code == 404
    assert mock_cda_client["notfound_hearing_route"].called
    assert response.content == b''


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_hearing_returns_server_error(mock_settings, mock_cda_settings, override_get_cda_settings,
                                      mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings
    response = client.get("/v2/hearing/00d0000c-00ff-00ec-b000-0000ac000003")

    assert response.status_code == 424
    assert mock_cda_client["exception_hearing_route"].called
    assert response.content == b''


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_hearing_returns_none(mock_settings, mock_cda_settings, override_get_cda_settings,
                              mock_cda_client):
    OauthClient().token = None
    mock_cda_settings.return_value = CdaSettings(cda_endpoint="http://failed-test-url/", cda_secret="12345",
                                                 cda_uid="12345")
    mock_settings.return_value = override_get_cda_settings
    response = client.get("/v2/hearing/00d0000c-00ff-00ec-b000-0000ac000003")

    assert response.status_code == 424
    assert response.content == b''
    assert mock_cda_client["failed_token_endpoint"].called
