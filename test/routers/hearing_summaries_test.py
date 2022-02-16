from unittest.mock import patch, PropertyMock

from fastapi.testclient import TestClient

from laa_court_data_api_app.main import app
from ..routers.fixtures import *

client = TestClient(app)


@patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
@patch('laa_court_data_api_app.internal.court_data_adaptor_client.CourtDataAdaptorClient.settings',
       new_callable=PropertyMock)
async def test_hearing_summaries_returns_ok(mock_settings, mock_cda_settings, override_get_cda_settings, mock_cda_client):
    mock_settings.return_value = override_get_cda_settings
    mock_cda_settings.return_value = override_get_cda_settings
    response = client.get("/v2/hearingsummaries/pass")

    assert response.status_code == 200
    assert mock_cda_client["pass_route"].called
