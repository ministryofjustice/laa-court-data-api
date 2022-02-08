from laa_court_data_api_app.internal import court_data_adaptor_client
from test.internal.internal_fixtures import *


async def get_token_async():
    return TokenResponse(access_token="12345", token_type="Bearer", expires_in=300, created_at=1643981187)


async def get_none_token():
    return None


test_codes = [(200, 200, get_token_async), (400, 400, get_token_async), (500, 500, get_token_async)]


@pytest.mark.parametrize("response_code,expected,token_function", test_codes)
async def test_get_request_returns_correctly(mock_cda_client, mock_oauth_client, get_cda_env_vars, expected):
    response = await court_data_adaptor_client.get("/get/", oauth_client=mock_oauth_client, settings=get_cda_env_vars)

    assert response.status_code == expected
    assert response.json() == []


@pytest.mark.parametrize("response_code,token_function", [(200, get_none_token)])
async def test_get_request_no_token(mock_cda_client, mock_oauth_client, get_cda_env_vars):
    response = await court_data_adaptor_client.get("/get/", oauth_client=mock_oauth_client, settings=get_cda_env_vars)

    assert response is None


@pytest.mark.parametrize("response_code,token_function", [(200, get_token_async)])
async def test_get_request_throws_exception(mock_cda_client, mock_oauth_client, get_cda_env_vars):
    response = await court_data_adaptor_client.get("/get/exception", oauth_client=mock_oauth_client,
                                                   settings=get_cda_env_vars)

    assert response is None


@pytest.mark.parametrize("response_code,expected,token_function", test_codes)
async def test_post_request_returns_correctly(mock_cda_client, mock_oauth_client, get_cda_env_vars, expected):
    response = await court_data_adaptor_client.post("/post/", oauth_client=mock_oauth_client, settings=get_cda_env_vars)

    assert response.status_code == expected
    assert response.json() == []


@pytest.mark.parametrize("response_code,token_function", [(200, get_none_token)])
async def test_post_request_no_token(mock_cda_client, mock_oauth_client, get_cda_env_vars):
    response = await court_data_adaptor_client.post("/post/", oauth_client=mock_oauth_client, settings=get_cda_env_vars)

    assert response is None


@pytest.mark.parametrize("response_code,token_function", [(200, get_token_async)])
async def test_post_request_throws_exception(mock_cda_client, mock_oauth_client, get_cda_env_vars):
    response = await court_data_adaptor_client.get("/post/exception", oauth_client=mock_oauth_client,
                                                   settings=get_cda_env_vars)

    assert response is None


@pytest.mark.parametrize("response_code,expected,token_function", test_codes)
async def test_patch_request_returns_correctly(mock_cda_client, mock_oauth_client, get_cda_env_vars, expected):
    response = await court_data_adaptor_client.patch("/patch/", oauth_client=mock_oauth_client,
                                                     settings=get_cda_env_vars)

    assert response.status_code == expected
    assert response.json() == {}


@pytest.mark.parametrize("response_code,token_function", [(200, get_none_token)])
async def test_patch_request_no_token(mock_cda_client, mock_oauth_client, get_cda_env_vars):
    response = await court_data_adaptor_client.patch("/patch/", oauth_client=mock_oauth_client,
                                                     settings=get_cda_env_vars)

    assert response is None


@pytest.mark.parametrize("response_code,token_function", [(200, get_token_async)])
async def test_patch_request_throws_exception(mock_cda_client, mock_oauth_client, get_cda_env_vars):
    response = await court_data_adaptor_client.get("/patch/exception", oauth_client=mock_oauth_client,
                                                   settings=get_cda_env_vars)

    assert response is None
