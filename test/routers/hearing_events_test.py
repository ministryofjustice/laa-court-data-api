from unittest.mock import Mock, patch, PropertyMock

from fastapi.testclient import TestClient

from laa_court_data_api_app.config.court_data_adaptor import CdaSettings
from laa_court_data_api_app.internal.oauth_client import OauthClient
from laa_court_data_api_app.main import app
from laa_court_data_api_app.models.hearing_events.hearing_events_response import HearingEventsResponse

client = TestClient(app)


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_hearing_events_returns_ok(mock_settings, mock_cda_settings, override_get_cda_settings,
                                   mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings

    response = client.get("/v2/hearing_events/22d2222c-22ff-22ec-b222-2222ac222222?date=pass")

    assert response.status_code == 200
    assert mock_cda_client["pass_hearing_events_route"].called
    model = HearingEventsResponse(**response.json())
    assert model.hearing_id is None
    assert model.has_active_hearing is True
    assert len(model.events) == 0


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_hearing_events_returns_bad_request(mock_settings, mock_cda_settings, override_get_cda_settings,
                                            mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings
    response = client.get("/v2/hearing_events/22d2222c-22ff-22ec-b222-2222ac222222?date=fail")

    assert response.status_code == 400
    assert mock_cda_client["fail_hearing_events_route"].called
    assert response.content == b''


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_hearing_events_returns_not_found(mock_settings, mock_cda_settings, override_get_cda_settings,
                                          mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings
    response = client.get("/v2/hearing_events/22d2222c-22ff-22ec-b222-2222ac222222?date=notfound")

    assert response.status_code == 404
    assert mock_cda_client["notfound_hearing_events_uuid_route"].called
    assert response.content == b''


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_hearing_events_returns_server_error(mock_settings, mock_cda_settings, override_get_cda_settings,
                                             mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings
    response = client.get("/v2/hearing_events/22d2222c-22ff-22ec-b222-2222ac222222?date=exception")

    assert response.status_code == 424
    assert mock_cda_client["exception_hearing_events_uuid_route"].called
    assert response.content == b''


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_hearing_events_returns_none(mock_settings, mock_cda_settings, override_get_cda_settings,
                                     mock_cda_client):
    OauthClient().token = None
    mock_cda_settings.return_value = CdaSettings(cda_endpoint="https://failed-test-url/", cda_secret="12345",
                                                 cda_uid="12345")
    mock_settings.return_value = override_get_cda_settings
    response = client.get("/v2/hearing_events/22d2222c-22ff-22ec-b222-2222ac222222?date=pass")

    assert response.status_code == 424
    assert response.content == b''
    assert mock_cda_client["failed_token_endpoint"].called
