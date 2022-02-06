import logging
from typing import Optional
import httpx
from ..config import court_data_adaptor as cda
from ..internal.oauth_client import OauthClient

logger = logging.getLogger(__name__)


async def get(endpoint: str, params: Optional[dict[str, str]] = None, headers: Optional[dict[str, str]] = None):
    response = await __send_request(method='GET', endpoint=endpoint, params=params, headers=headers)
    return response


async def post(endpoint: str, params: Optional[dict[str, str]] = None, headers: Optional[dict[str, str]] = None,
               body: Optional[any] = None):
    response = await __send_request(method='POST', endpoint=endpoint, params=params, headers=headers, body=body)
    return response


async def patch(endpoint: str, params: Optional[dict[str, str]] = None, headers: Optional[dict[str, str]] = None,
                body: Optional[any] = None):
    response = await __send_request(method='PATCH', endpoint=endpoint, params=params, headers=headers, body=body)
    return response


async def __send_request(method: str, endpoint: str, params: Optional[dict[str, str]] = None,
                         headers: Optional[dict[str, str]] = None, body: Optional[any] = None):
    auth_token = await OauthClient().retrieve_token()
    if auth_token is None:
        return auth_token

    async with httpx.AsyncClient(base_url=cda.get_cda_settings().base_url,
                                 headers=OauthClient.generate_auth_header(auth_token)) as client:
        try:
            request = client.build_request(method=method, url=endpoint, params=params, headers=headers, data=body)
            logger.info("Request_Made")
            response = await client.send(request)
            logger.info("Response_Returned", extra={'url': request.url, 'status': response.status_code})
            return response
        except:
            logger.error("Get_Endpoint_Error", extra={'url': request.url})
            return None
