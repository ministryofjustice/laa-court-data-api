import logging
from typing import Optional

import httpx
from fastapi import Depends

from ..config.court_data_adaptor import CdaSettings
from ..internal.oauth_client import OauthClient

logger = logging.getLogger(__name__)


async def get(endpoint: str, params: Optional[dict[str, str]] = None, headers: Optional[dict[str, str]] = None,
              oauth_client: OauthClient = Depends(OauthClient), settings: CdaSettings = Depends(CdaSettings)):
    response = await __send_request(oauth_client, settings, method='GET', endpoint=endpoint, params=params,
                                    headers=headers)
    return response


async def post(endpoint: str, params: Optional[dict[str, str]] = None, headers: Optional[dict[str, str]] = None,
               body: Optional[any] = None, oauth_client: OauthClient = Depends(OauthClient),
               settings: CdaSettings = Depends(CdaSettings)):
    response = await __send_request(oauth_client, settings, method='POST', endpoint=endpoint, params=params,
                                    headers=headers, body=body)
    return response


async def patch(endpoint: str, params: Optional[dict[str, str]] = None, headers: Optional[dict[str, str]] = None,
                body: Optional[any] = None, oauth_client: OauthClient = Depends(OauthClient),
                settings: CdaSettings = Depends(CdaSettings)):
    response = await __send_request(oauth_client, settings, method='PATCH', endpoint=endpoint, params=params,
                                    headers=headers, body=body)
    return response


async def __send_request(oauth_client: OauthClient, settings: CdaSettings, method: str, endpoint: str,
                         params: Optional[dict[str, str]] = None,
                         headers: Optional[dict[str, str]] = None, body: Optional[any] = None):
    auth_token = await oauth_client.retrieve_token()
    if auth_token is None:
        return auth_token

    async with httpx.AsyncClient(base_url=settings.cda_endpoint, headers=OauthClient.generate_auth_header(auth_token)) \
            as client:
        try:
            request = client.build_request(method=method, url=endpoint, params=params, headers=headers, data=body)
            logger.info("Request_Made")
            response = await client.send(request)
            logger.info("Response_Returned", extra={'url': request.url, 'status': response.status_code})
            return response
        except(Exception) as e:
            logger.error("Get_Endpoint_Error", extra={'url': request.url})
            logger.error(e)
            return None
