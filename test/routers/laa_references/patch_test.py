from unittest.mock import patch, PropertyMock
import uuid

from fastapi.testclient import TestClient

from laa_court_data_api_app.config.court_data_adaptor import CdaSettings
from laa_court_data_api_app.internal.oauth_client import OauthClient
from laa_court_data_api_app.main import app
from laa_court_data_api_app.models.laa_references.external.request.laa_references_patch_request import \
    LaaReferencesPatchRequest

client = TestClient(app)

LAA_REFERENCES_ENDPOINT = '/v2/laa_references'
JSON_CONTENT_TYPE = 'application/json'


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_laa_references_patch_returns_accepted(mock_settings, mock_cda_settings, override_get_cda_settings,
                                               mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings

    response = client.patch(f"{LAA_REFERENCES_ENDPOINT}/22d2222c-22ff-22ec-b222-2222ac222222/",
                            headers={"Content-Type": JSON_CONTENT_TYPE},
                            data=LaaReferencesPatchRequest(
                                defendant_id=uuid.UUID("22d2222c-22ff-22ec-b222-2222ac222222")
                            ).json())

    assert response.status_code == 202
    assert response.content == b''
    assert mock_cda_client["laa_references_patch_pass_route"].called


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_laa_references_patch_returns_bad_request(mock_settings, mock_cda_settings, override_get_cda_settings,
                                                  mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings

    response = client.patch(f"{LAA_REFERENCES_ENDPOINT}/22d2222c-22ff-22ec-b222-2222ac222223/",
                            headers={"Content-Type": JSON_CONTENT_TYPE},
                            data=LaaReferencesPatchRequest(
                                defendant_id=uuid.UUID("22d2222c-22ff-22ec-b222-2222ac222223")
                            ).json())

    assert response.status_code == 400
    assert mock_cda_client["laa_references_patch_fail_route"].called
    assert response.content == b'{"errors": {"unlink_other_reason_text": ["must be absent"]}}'


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_laa_references_patch_returns_not_found(mock_settings, mock_cda_settings, override_get_cda_settings,
                                                mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings

    response = client.patch(f"{LAA_REFERENCES_ENDPOINT}/22d2222c-22ff-22ec-b222-2222ac222224/",
                            headers={"Content-Type": JSON_CONTENT_TYPE},
                            data=LaaReferencesPatchRequest(
                                defendant_id=uuid.UUID("22d2222c-22ff-22ec-b222-2222ac222224")
                            ).json())

    assert response.status_code == 404
    assert response.content == b''
    assert mock_cda_client["laa_references_patch_not_found_route"].called


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_laa_references_patch_returns_unprocessable_entity(mock_settings, mock_cda_settings, override_get_cda_settings,
                                                           mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings

    response = client.patch(f"{LAA_REFERENCES_ENDPOINT}/22d2222c-22ff-22ec-b222-2222ac222225/",
                            headers={"Content-Type": JSON_CONTENT_TYPE},
                            data=LaaReferencesPatchRequest(
                                defendant_id=uuid.UUID("22d2222c-22ff-22ec-b222-2222ac222225")
                            ).json())

    assert response.status_code == 422
    assert mock_cda_client["laa_references_patch_unprocessable_entity_route"].called
    assert response.content == \
           b'{"errors": {"maat_reference": ["3141592 has no common platform data created against Maat application."]}}'


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_laa_references_patch_returns_server_error(mock_settings, mock_cda_settings, override_get_cda_settings,
                                                   mock_cda_client):
    OauthClient().token = None
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings

    response = client.patch(f"{LAA_REFERENCES_ENDPOINT}/22d2222c-22ff-22ec-b222-2222ac222226/",
                            headers={"Content-Type": JSON_CONTENT_TYPE},
                            data=LaaReferencesPatchRequest(
                                defendant_id=uuid.UUID("22d2222c-22ff-22ec-b222-2222ac222226")
                            ).json())

    assert response.status_code == 424
    assert response.content == b''
    assert mock_cda_client["laa_references_patch_server_error_route"].called


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
def test_laa_references_patch_returns_none(mock_settings, mock_cda_settings, override_get_cda_settings,
                                           mock_cda_client):
    OauthClient().token = None
    mock_cda_settings.return_value = CdaSettings(cda_endpoint="https://failed-test-url/", cda_secret="12345",
                                                 cda_uid="12345")
    mock_settings.return_value = override_get_cda_settings

    response = client.patch("/v2/laa_references/22d2222c-22ff-22ec-b222-2222ac222222/",
                            headers={"Content-Type": JSON_CONTENT_TYPE},
                            data=LaaReferencesPatchRequest(
                                defendant_id=uuid.UUID("22d2222c-22ff-22ec-b222-2222ac222222")
                            ).json())

    assert response.status_code == 424
    assert response.content == b''
    assert mock_cda_client["failed_token_endpoint"].called


def test_laa_references_patch_mismatch_defendantid_returns_bad_request():
    response = client.patch(
        f"{LAA_REFERENCES_ENDPOINT}/22d2222c-22ff-22ec-b222-2222ac222222/",
        headers={"Content-Type": JSON_CONTENT_TYPE},
        data=LaaReferencesPatchRequest(
            defendant_id=uuid.UUID("12d2222c-22ff-22ec-b222-2222ac222222")
        ).json()
    )

    assert response.status_code == 400
    assert response.content == b'{"errors": {"defendant_id": ["mismatch in ids given"]}}'
