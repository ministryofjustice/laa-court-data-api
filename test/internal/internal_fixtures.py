import datetime as dt

import httpx
import pytest
import respx
from httpx import Response

from laa_court_data_api_app.config.court_data_adaptor import CdaSettings
from laa_court_data_api_app.models.token_response import TokenResponse


@pytest.fixture(scope="module")
def get_cda_env_vars():
    return CdaSettings(cda_endpoint="http://test-url/", cda_uid="12345", cda_secret="123454321")


@pytest.fixture(scope="module")
def get_expired_token_response():
    return TokenResponse(access_token="12345", token_type="Bearer", expires_in=300, created_at=1643981187)


@pytest.fixture(scope="module")
def get_new_token_response():
    token = "12345"
    created_at = dt.datetime.utcnow() - dt.datetime(1970, 1, 1)
    return TokenResponse(access_token=token, token_type="Bearer", expires_in=300,
                         created_at=int(created_at.total_seconds()))


@pytest.fixture(scope="function")
def mock_cda_client(get_new_token_response, response_code):
    with respx.mock(base_url="http://test-url/", assert_all_called=False) as respx_mock:
        get_route = respx_mock.get("/get/", name="get_endpoint")
        get_route.return_value = Response(response_code, json=[])
        get_exception = respx_mock.get("/get/exception", name="get_exception_endpoint")
        get_exception.side_effect = Exception("Failed")
        post_route = respx_mock.post("/post/", name="post_endpoint")
        post_route.return_value = Response(response_code, json=[])
        post_exception = respx_mock.get("/post/exception", name="post_exception_endpoint")
        post_exception.side_effect = Exception("Failed")
        patch_route = respx_mock.patch("/patch/", name="patch_endpoint")
        patch_route.return_value = Response(response_code, json={})
        patch_exception = respx_mock.get("/patch/exception", name="patch_exception_endpoint")
        patch_exception.side_effect = Exception("Failed")
        yield respx_mock


@pytest.fixture()
def mock_oauth_client(respx_mock, token_function):
    respx_mock.post("/oauth/token").mock(return_value=httpx.Response(status_code=200,
                                                                     json=token_function().dict()))
