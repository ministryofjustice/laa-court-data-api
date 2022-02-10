from unittest.mock import PropertyMock, patch

from laa_court_data_api_app.internal.oauth_client import OauthClient
from test.internal.internal_fixtures import *


class TestOAuthClient:
    @patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
    @pytest.mark.respx(base_url="http://test-url/")
    async def test_retrieve_token_returns_correct_value(self, mock_settings, respx_mock, get_cda_env_vars):
        mock_settings.return_value = get_cda_env_vars
        respx_mock.post("/oauth/token").mock(return_value=httpx.Response(status_code=200,
                                                                         json={"access_token": "12345",
                                                                               "token_type": "Bearer",
                                                                               "expires_in": "300",
                                                                               "created_at": "1643981187"}))

        response = await OauthClient().retrieve_token()

        assert response.access_token == "12345"
        assert response.token_type == "Bearer"
        assert response.expires_in == 300
        assert response.created_at == 1643981187

    @patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
    @pytest.mark.respx(base_url="http://test-url/")
    async def test_retrieve_token_stores_token(self, mock_settings, respx_mock, get_cda_env_vars):
        mock_settings.return_value = get_cda_env_vars
        respx_mock.post("/oauth/token").mock(return_value=httpx.Response(status_code=200,
                                                                         json={"access_token": "12345",
                                                                               "token_type": "Bearer",
                                                                               "expires_in": "300",
                                                                               "created_at": "1643981187"}))

        await OauthClient().retrieve_token()

        assert OauthClient().token.access_token == "12345"
        assert OauthClient().token.token_type == "Bearer"
        assert OauthClient().token.expires_in == 300
        assert OauthClient().token.created_at == 1643981187

    @patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
    @pytest.mark.respx(base_url="http://test-url/")
    async def test_retrieve_token_calls_endpoint(self, mock_settings, respx_mock, get_cda_env_vars):
        mock_settings.return_value = get_cda_env_vars
        route = respx_mock.post("/oauth/token").mock(return_value=httpx.Response(status_code=200,
                                                                                 json={"access_token": "12345",
                                                                                       "token_type": "Bearer",
                                                                                       "expires_in": "300",
                                                                                       "created_at": "1643981187"}))

        await OauthClient().retrieve_token()

        assert route.called

    @patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
    @pytest.mark.respx(base_url="http://test-url/")
    async def test_retrieve_token_calls_property(self, mock_settings, respx_mock, get_cda_env_vars,
                                                 get_new_token_response):
        mock_settings.return_value = get_cda_env_vars
        route = respx_mock.post("/oauth/token").mock(return_value=httpx.Response(status_code=200,
                                                                                 json={"access_token": "12345",
                                                                                       "token_type": "Bearer",
                                                                                       "expires_in": "300",
                                                                                       "created_at": "1643981187"}))

        client = OauthClient()
        client.token = get_new_token_response
        response = await client.retrieve_token()

        assert route.call_count == 0
        assert response.access_token == client.token.access_token

    @patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
    @pytest.mark.respx(base_url="http://test-url/")
    async def test_retrieve_token_calls_property(self, mock_settings, respx_mock, get_cda_env_vars,
                                                 get_expired_token_response):
        mock_settings.return_value = get_cda_env_vars
        route = respx_mock.post("/oauth/token").mock(return_value=httpx.Response(status_code=200,
                                                                                 json={"access_token": "123456",
                                                                                       "token_type": "Bearer",
                                                                                       "expires_in": "300",
                                                                                       "created_at": "1643981187"}))

        client = OauthClient()
        client.token = get_expired_token_response
        response = await client.retrieve_token()

        assert route.call_count == 1
        assert response.access_token == "123456"

    @patch('laa_court_data_api_app.internal.oauth_client.OauthClient.settings', new_callable=PropertyMock)
    @pytest.mark.respx(base_url="http://test-url/")
    async def test_retrieve_token_calls_property(self, mock_settings, respx_mock, get_cda_env_vars):
        mock_settings.return_value = get_cda_env_vars
        respx_mock.post("/oauth/token").mock(return_value=httpx.Response(status_code=500))

        client = OauthClient()
        response = await client.retrieve_token()

        assert response is None

    # generate_params tests
    def test_params_generates_correctly(self, get_cda_env_vars):
        params = OauthClient.generate_params(get_cda_env_vars)

        assert "grant_type" in params
        assert "client_id" in params
        assert "client_secret" in params
        assert params["grant_type"] == "client_credentials"
        assert params["client_id"] == get_cda_env_vars.cda_uid
        assert params["client_secret"] == get_cda_env_vars.cda_secret

    def test_params_none_gives_error(self):
        with pytest.raises(AttributeError):
            OauthClient.generate_params(None)

    # generate_auth_header tests
    def test_auth_header_generates_correctly(self, get_expired_token_response):
        token = get_expired_token_response
        generated_header = OauthClient.generate_auth_header(token)

        assert "Authorization" in generated_header
        assert generated_header["Authorization"] == f"{token.token_type} {token.access_token}"

    def test_auth_header_none_gives_error(self):
        with pytest.raises(AttributeError):
            OauthClient.generate_auth_header(None)

    def test_auth_header_empty_gives_error(self):
        with pytest.raises(AttributeError):
            OauthClient.generate_auth_header(TokenResponse())
