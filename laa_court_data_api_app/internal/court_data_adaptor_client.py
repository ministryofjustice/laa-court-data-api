import logging
from typing import Optional

import httpx

from laa_court_data_api_app.config.court_data_adaptor import get_cda_settings, CdaSettings
from ..internal.oauth_client import OauthClient

logger = logging.getLogger(__name__)


class CourtDataAdaptorClient:
    @property
    def settings(self) -> CdaSettings:
        return get_cda_settings()

    async def get(self, endpoint: str, params: Optional[dict[str, str]] = None,
                  headers: Optional[dict[str, any]] = None):
        response = await self.__send_request(method='GET', endpoint=endpoint, params=params, headers=headers)
        return response

    async def post(self, endpoint: str, params: Optional[dict[str, str]] = None,
                   headers: Optional[dict[str, any]] = None,
                   body: Optional[any] = None):
        if headers is None:
            headers = {}
        headers.update({"Content-Type": "application/json"})
        response = await self.__send_request(method='POST', endpoint=endpoint, params=params, headers=headers,
                                             body=body.json())
        return response

    async def patch(self, endpoint: str, params: Optional[dict[str, str]] = None,
                    headers: Optional[dict[str, any]] = None,
                    body: Optional[any] = None):
        if headers is None:
            headers = {}
        headers.update({"Content-Type": "application/json"})
        response = await self.__send_request(method='PATCH', endpoint=endpoint, params=params, headers=headers,
                                             body=body.json())
        return response

    async def __send_request(self, method: str, endpoint: str,
                             params: Optional[dict[str, str]] = None,
                             headers: Optional[dict[str, any]] = None, body: Optional[any] = None):
        oauth_client = OauthClient()
        token = await oauth_client.retrieve_token()
        if token is None:
            return token

        async with httpx.AsyncClient(base_url=self.settings.cda_endpoint,
                                     headers=oauth_client.generate_auth_header(token)) \
                as client:
            try:
                request = client.build_request(method=method, url=endpoint, params=params, headers=headers,
                                               content=body)
                logger.info("Request_Made")
                response = await client.send(request)
                logger.info("Response_Returned", extra={'url': request.url, 'status': response.status_code})
                return response
            except(Exception) as e:
                logger.error("Get_Endpoint_Error", extra={'url': request.url})
                logger.error(e)
                return None
