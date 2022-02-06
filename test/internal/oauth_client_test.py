import httpx
import pytest

from laa_court_data_api_app.config.court_data_adaptor import CdaSettings
from laa_court_data_api_app.internal.oauth_client import OauthClient
from laa_court_data_api_app.models.token_response import TokenResponse


@pytest.fixture(scope="module")
def get_cda_env_vars():
    return CdaSettings(cda_endpoint="http://test-url/", cda_uid="12345", cda_secret="123454321")


@pytest.fixture(scope="module")
def get_standard_token_response():
    return TokenResponse(access_token="12345", token_type="Bearer", expires_in=300, created_at=1643981187)


class TestOAuthClient:
    @pytest.mark.mock(base_url="http://test-url/")
    async def test_stores_value(self, respx_mock, get_cda_env_vars):
        respx_mock.post("/oauth/token").mock(return_value=httpx.Response(status_code=200,
                                                                         json={"access_token": "12345",
                                                                               "token_type": "Bearer",
                                                                               "expires_in": "300",
                                                                               "created_at": "1643981187"}))

        response = await OauthClient().retrieve_token(settings=get_cda_env_vars)

        assert response.access_token == "12345"
        assert response.token_type == "Bearer"
        assert response.expires_in == 300
        assert response.created_at == 1643981187

    # generate_auth_header tests
    def test_generates_correctly(self, get_standard_token_response):
        token = get_standard_token_response
        generated_header = OauthClient.generate_auth_header(token)

        assert "Authorization" in generated_header
        assert generated_header["Authorization"] == f"{token.token_type} {token.access_token}"

    def test_none_gives_error(self):
        with pytest.raises(Exception):
            generated_header = OauthClient.generate_auth_header(None)