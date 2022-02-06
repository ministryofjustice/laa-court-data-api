import datetime as dt
import logging

import httpx
from fastapi import Depends

from ..config import court_data_adaptor as cda
from ..models.token_response import TokenResponse

logger = logging.getLogger(__name__)


class OauthClient:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.__instance = super(OauthClient, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        self.__token = None

    @property
    def token(self) -> TokenResponse:
        return self.__token

    @token.setter
    def token(self, value):
        self.__token = value

    async def retrieve_token(self, settings: cda.CdaSettings = Depends(cda.get_cda_settings)) -> TokenResponse:
        logger.debug("OAuth_Retrieving_token")
        if self.token is None or self.token_has_expired():
            logger.debug("Token_expired_or_missing")
            async with httpx.AsyncClient(base_url=settings.cda_endpoint) as client:
                response = await client.post("/oauth/token", data=self.generate_params(settings))
                if response.status_code == 200:
                    logger.debug("Token_Retrieved_From_Service")
                    token = TokenResponse(**response.json())
                else:
                    logger.debug("Unable_To_Retrieve_Token")
                    token = None
        return token

    def token_has_expired(self) -> bool:
        converted_expiry = dt.datetime(1970, 1, 1) + dt.timedelta(seconds=self.token.created_at)
        return converted_expiry + dt.timedelta(seconds=self.token.expires_in) < dt.datetime.utcnow()

    @staticmethod
    def generate_params(settings: cda.CdaSettings) -> dict[str, str]:
        return {
            'grant_type': 'client_credentials',
            'client_id': settings.cda_uid,
            'client_secret': settings.cda_secret
        }

    @staticmethod
    def generate_auth_header(token: TokenResponse) -> dict[str, str]:
        return {
            "Authorization": f"{token.token_type} {token.access_token}"
        }
