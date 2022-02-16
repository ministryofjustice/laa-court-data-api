import datetime as dt

import pytest
import respx
from httpx import Response

from laa_court_data_api_app.config.court_data_adaptor import CdaSettings
from laa_court_data_api_app.models.prosecution_cases.prosecution_cases_results import ProsecutionCasesResults
from laa_court_data_api_app.models.token_response import TokenResponse


@pytest.fixture()
def override_get_cda_settings():
    return CdaSettings(cda_secret="12345", cda_uid="12345", cda_endpoint="http://test-url/")


@pytest.fixture()
def get_new_token_response():
    token = "12345"
    created_at = dt.datetime.utcnow() - dt.datetime(1970, 1, 1)
    return TokenResponse(access_token=token, token_type="Bearer", expires_in=300,
                         created_at=int(created_at.total_seconds()))


@pytest.fixture()
def mock_cda_client(get_new_token_response):
    with respx.mock(base_url="http://test-url/", assert_all_called=False) as respx_mock:
        get_route = respx_mock.post("/oauth/token", name="token_endpoint")
        get_route.return_value = Response(200, json=get_new_token_response.dict())
        pass_route = respx_mock.get("/api/internal/v2/prosecution_cases", name="pass_route")
        pass_route.return_value = Response(200, json=ProsecutionCasesResults(total_results=0, results=[]).dict())
        yield respx_mock
