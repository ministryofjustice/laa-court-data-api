import structlog
from typing import Optional

import httpx

from asgi_correlation_id.context import correlation_id
from laa_court_data_api_app.config.court_data_adaptor import get_cda_settings, CdaSettings
from ..internal.oauth_client import OauthClient
from circuitbreaker import circuit

logger = structlog.get_logger(__name__)
http_client = httpx.AsyncClient(timeout=60.0)


class CourtDataAdaptorClient:
    @property
    def settings(self) -> CdaSettings:
        return get_cda_settings()

    async def get(self, endpoint: str, params: Optional[dict[str, str]] = None,
                  headers: Optional[dict[str, any]] = None):
        headers = self.__setup_default_headers(headers, {"X-Request-Id": correlation_id.get() or ''})

        response = await self.__send_request(method='GET', endpoint=endpoint, params=params, headers=headers)
        return response

    async def post(self, endpoint: str, params: Optional[dict[str, str]] = None,
                   headers: Optional[dict[str, any]] = None,
                   body: Optional[any] = None):
        headers = self.__setup_default_headers(headers, {"Content-Type": "application/json",
                                                         "X-Request-Id": correlation_id.get() or ''})

        if body is not None:
            body = body.json()

        response = await self.__send_request(method='POST', endpoint=endpoint, params=params, headers=headers,
                                             body=body)
        return response

    async def patch(self, endpoint: str, params: Optional[dict[str, str]] = None,
                    headers: Optional[dict[str, any]] = None,
                    body: Optional[any] = None):
        headers = self.__setup_default_headers(headers, {"Content-Type": "application/json",
                                                         "X-Request-Id": correlation_id.get() or ''})

        if body is not None:
            body = body.json()

        response = await self.__send_request(method='PATCH', endpoint=endpoint, params=params, headers=headers,
                                             body=body)
        return response

    async def __send_request(self, method: str, endpoint: str,
                             params: Optional[dict[str, str]] = None,
                             headers: Optional[dict[str, any]] = None, body: Optional[any] = None):
        oauth_client = OauthClient()
        token = await oauth_client.retrieve_token()
        if token is None:
            return token

        return await self.__call_endpoint(oauth_client, token, method, endpoint, params, headers, body)

    @circuit()
    async def __call_endpoint(self, oauth_client: OauthClient, token, method: str, endpoint: str,
                              params: Optional[dict[str, str]] = None,
                              headers: Optional[dict[str, any]] = None, body: Optional[any] = None):
        http_client.base_url = self.settings.cda_endpoint
        http_client.headers = oauth_client.generate_auth_header(token)
        try:
            request = http_client.build_request(method=method, url=endpoint, params=params, headers=headers,
                                                content=body)
            logger.info('CDA_Request_Made', endpoint=request.url)
            response = await http_client.send(request)
            logger.info('CDA_Response_Returned', endpoint=request.url, status_code=response.status_code)
            return response
        except (Exception) as e:
            logger.error('CDA_Endpoint_Error', endpoint=request.url, exception=e)
            return None

    @staticmethod
    def __setup_default_headers(headers: dict, default_headers: dict):
        if headers is None:
            headers = {}

        headers.update(default_headers)

        return headers
