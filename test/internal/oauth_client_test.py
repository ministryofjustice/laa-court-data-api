import httpx
import respx
from laa_court_data_api_app.config.court_data_adaptor import CdaSettings
from laa_court_data_api_app.internal.oauth_client import OauthClient


@respx.mock(base_url="http://test-url/")
async def test_oauth_client_stores_value(respx_mock):
    respx_mock.post("/oauth/token").mock(return_value=httpx.Response(status_code=200,
                                                                     json={"access_token": "12345",
                                                                           "token_type": "Bearer",
                                                                           "expires_in": "300",
                                                                           "created_at": "1643981187"}))

    response = await OauthClient().retrieve_token(settings=get_cda_env_vars())

    assert response.access_token == "12345"
    assert response.token_type == "Bearer"
    assert response.expires_in == 300
    assert response.created_at == 1643981187


def get_cda_env_vars():
    return CdaSettings(cda_endpoint="http://test-url/", cda_uid="12345", cda_secret="123454321")
