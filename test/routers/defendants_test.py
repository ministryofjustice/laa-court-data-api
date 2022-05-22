from unittest.mock import patch, PropertyMock

from fastapi.testclient import TestClient

from laa_court_data_api_app.internal.oauth_client import OauthClient
from laa_court_data_api_app.main import app
from laa_court_data_api_app.models.defendants.defendants_response import DefendantsResponse
from ..routers.fixtures import *

client = TestClient(app)


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_invalid_search_returns_not_found(mock_settings, mock_cda_settings,
                                          override_get_cda_settings, mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings
    response = client.get("/v2/defendants?invalid_route")

    assert response.status_code == 400
    assert response.content == b''


# Search defendant by name and date of birth

@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_defendants_by_name_dob_returns_ok(mock_settings, mock_cda_settings, override_get_cda_settings,
                                           mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings
    response = client.get("/v2/defendants?name=pass&dob=pass")

    assert response.status_code == 200
    assert mock_cda_client["pass_name_dob_route"].called
    model = DefendantsResponse(**response.json())
    assert len(model.defendant_summaries) == 1


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_defendants_by_name_dob_returns_bad_request(mock_settings, mock_cda_settings, override_get_cda_settings,
                                                    mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings
    response = client.get("/v2/defendants?name=fail&dob=fail")

    assert response.status_code == 400
    assert mock_cda_client["fail_name_dob_route"].called
    assert response.content == b''


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_defendants_by_name_dob_returns_not_found(mock_settings, mock_cda_settings, override_get_cda_settings,
                                                  mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings
    response = client.get("/v2/defendants?name=notfound&dob=notfound")

    assert response.status_code == 404
    assert mock_cda_client["notfound_name_dob_route"].called
    assert response.content == b''


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_defendants_by_name_dob_returns_server_error(mock_settings, mock_cda_settings, override_get_cda_settings,
                                                     mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings
    response = client.get("/v2/defendants?name=exception&dob=exception")

    assert response.status_code == 424
    assert mock_cda_client["exception_name_dob_route"].called
    assert response.content == b''


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_defendants_by_name_dob_returns_none(mock_settings, mock_cda_settings, override_get_cda_settings,
                                             mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = CdaSettings(cda_endpoint="https://failed-test-url/", cda_secret="12345",
                                                 cda_uid="12345")
    response = client.get("/v2/defendants?name=exception&dob=exception")

    assert response.status_code == 424
    assert response.content == b''
    assert mock_cda_client["failed_token_endpoint"].called


# Search defendant by urn and uuid

@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_defendants_by_urn_uuid_returns_ok(mock_settings, mock_cda_settings, override_get_cda_settings,
                                           mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings
    response = client.get("/v2/defendants?urn=pass&uuid=22d2222c-22ff-22ec-b222-2222ac222222")

    assert response.status_code == 200
    assert mock_cda_client["pass_urn_uuid_route"].called
    model = DefendantsResponse(**response.json())
    assert len(model.defendant_summaries) == 1


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_defendants_by_urn_uuid_returns_bad_request(mock_settings, mock_cda_settings, override_get_cda_settings,
                                                    mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings
    response = client.get("/v2/defendants?urn=fail&uuid=22d2222c-22ff-22ec-b222-2222ac222222")

    assert response.status_code == 400
    assert mock_cda_client["fail_urn_uuid_route"].called
    assert response.content == b''


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_defendants_by_urn_uuid_returns_not_found(mock_settings, mock_cda_settings, override_get_cda_settings,
                                                  mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings
    response = client.get("/v2/defendants?urn=404&uuid=22d2222c-22ff-22ec-b222-2222ac222222")

    assert response.status_code == 404
    assert mock_cda_client["notfound_urn_uuid_route"].called
    assert response.content == b''


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_defendants_by_urn_uuid_returns_server_error(mock_settings, mock_cda_settings, override_get_cda_settings,
                                                     mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings
    response = client.get("/v2/defendants?urn=error&uuid=22d2222c-22ff-22ec-b222-2222ac222222")

    assert response.status_code == 424
    assert mock_cda_client["exception_urn_uuid_route"].called
    assert response.content == b''


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_defendants_by_urn_uuid_returns_none(mock_settings, mock_cda_settings, override_get_cda_settings,
                                             mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = CdaSettings(cda_endpoint="https://failed-test-url/", cda_secret="12345",
                                                 cda_uid="12345")
    response = client.get("/v2/defendants?urn=exception&uuid=22d2222c-22ff-22ec-b222-2222ac222222")

    assert response.status_code == 424
    assert response.content == b''
    assert mock_cda_client["failed_token_endpoint"].called


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_defendants_by_urn_uuid_returns_unprocessable_error(mock_settings, mock_cda_settings, override_get_cda_settings,
                                                            mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings
    response = client.get("/v2/defendants?urn=exception&uuid=invalid")

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "value is not a valid uuid"


# Search defendant by urn

@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_defendants_by_urn_returns_ok(mock_settings, mock_cda_settings, override_get_cda_settings,
                                      mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings
    response = client.get("/v2/defendants?urn=pass")

    assert response.status_code == 200
    assert mock_cda_client["pass_route"].called
    model = DefendantsResponse(**response.json())
    assert len(model.defendant_summaries) == 1


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_defendants_by_urn_returns_bad_request(mock_settings, mock_cda_settings, override_get_cda_settings,
                                               mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings
    response = client.get("/v2/defendants?urn=fail")

    assert response.status_code == 400
    assert mock_cda_client["fail_route"].called
    assert response.content == b''


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_defendants_by_urn_returns_not_found(mock_settings, mock_cda_settings, override_get_cda_settings,
                                             mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings
    response = client.get("/v2/defendants?urn=notfound")

    assert response.status_code == 404
    assert mock_cda_client["notfound_route"].called
    assert response.content == b''


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_defendants_by_urn_returns_server_error(mock_settings, mock_cda_settings, override_get_cda_settings,
                                                mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings
    response = client.get("/v2/defendants?urn=exception")

    assert response.status_code == 424
    assert mock_cda_client["exception_route"].called
    assert response.content == b''


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_defendants_by_urn_returns_none(mock_settings, mock_cda_settings, override_get_cda_settings,
                                        mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = CdaSettings(cda_endpoint="https://failed-test-url/", cda_secret="12345",
                                                 cda_uid="12345")
    response = client.get("/v2/defendants?urn=exception")

    assert response.status_code == 424
    assert response.content == b''
    assert mock_cda_client["failed_token_endpoint"].called


# Search defendant by asn

@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_defendants_by_asn_returns_ok(mock_settings, mock_cda_settings, override_get_cda_settings,
                                      mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings
    response = client.get("/v2/defendants?asn=pass")

    assert response.status_code == 200
    assert mock_cda_client["pass_asn_route"].called
    model = DefendantsResponse(**response.json())
    assert len(model.defendant_summaries) == 1


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_defendants_by_asn_returns_bad_request(mock_settings, mock_cda_settings, override_get_cda_settings,
                                               mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings
    response = client.get("/v2/defendants?asn=fail")

    assert response.status_code == 400
    assert mock_cda_client["fail_asn_route"].called
    assert response.content == b''


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_defendants_by_asn_returns_not_found(mock_settings, mock_cda_settings, override_get_cda_settings,
                                             mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings
    response = client.get("/v2/defendants?asn=notfound")

    assert response.status_code == 404
    assert mock_cda_client["notfound_asn_route"].called
    assert response.content == b''


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_defendants_by_asn_returns_server_error(mock_settings, mock_cda_settings, override_get_cda_settings,
                                                mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings
    response = client.get("/v2/defendants?asn=exception")

    assert response.status_code == 424
    assert mock_cda_client["exception_asn_route"].called
    assert response.content == b''


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_defendants_by_asn_returns_none(mock_settings, mock_cda_settings, override_get_cda_settings,
                                        mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = CdaSettings(cda_endpoint="https://failed-test-url/", cda_secret="12345",
                                                 cda_uid="12345")
    response = client.get("/v2/defendants?asn=exception")

    assert response.status_code == 424
    assert response.content == b''
    assert mock_cda_client["failed_token_endpoint"].called


# Search defendant by nino

@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_defendants_by_nino_returns_ok(mock_settings, mock_cda_settings, override_get_cda_settings,
                                       mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings
    response = client.get("/v2/defendants?nino=pass")

    assert response.status_code == 200
    assert mock_cda_client["pass_nino_route"].called
    model = DefendantsResponse(**response.json())
    assert len(model.defendant_summaries) == 1


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_defendants_by_nino_returns_bad_request(mock_settings, mock_cda_settings, override_get_cda_settings,
                                                mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings
    response = client.get("/v2/defendants?nino=fail")

    assert response.status_code == 400
    assert mock_cda_client["fail_nino_route"].called
    assert response.content == b''


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_defendants_by_nino_returns_not_found(mock_settings, mock_cda_settings, override_get_cda_settings,
                                              mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings
    response = client.get("/v2/defendants?nino=notfound")

    assert response.status_code == 404
    assert mock_cda_client["notfound_nino_route"].called
    assert response.content == b''


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_defendants_by_nino_returns_server_error(mock_settings, mock_cda_settings, override_get_cda_settings,
                                                 mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings
    response = client.get("/v2/defendants?nino=exception")

    assert response.status_code == 424
    assert mock_cda_client["exception_nino_route"].called
    assert response.content == b''


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_defendants_by_nino_returns_none(mock_settings, mock_cda_settings, override_get_cda_settings,
                                         mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = CdaSettings(cda_endpoint="https://failed-test-url/", cda_secret="12345",
                                                 cda_uid="12345")
    response = client.get("/v2/defendants?nino=exception")

    assert response.status_code == 424
    assert response.content == b''
    assert mock_cda_client["failed_token_endpoint"].called
