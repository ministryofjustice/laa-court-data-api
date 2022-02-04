import datetime as dt
from fastapi import Depends
import httpx
from ..config import court_data_adaptor as cda
from ..models.token_response import TokenResponse
import logging

logger = logging.getLogger(__name__)


class OauthClient:
    def __init__(self):
        self.__token = None

    @property
    def token(self) -> TokenResponse:
        return self.__token

    @token.setter
    def token(self, value):
        self.__token = value

    @classmethod
    async def retrieve_token(cls, settings: cda.CdaSettings = Depends(cda.get_cda_settings)) -> TokenResponse:
        logger.debug("OAuth_Retrieving_token")
        if cls.token is None or cls.__token_has_expired():
            logger.debug("Token_expired_or_missing")
            async with httpx.AsyncClient(base_url=settings.cda_endpoint) as client:
                response = await client.post("/oauth/token", data=cls.__generate_params(settings))
                if response.status_code == 200:
                    logger.debug("Token_Retrieved_From_Service")
                    token = TokenResponse(**response.json())
                else:
                    logger.debug("Unable_To_Retrieve_Token")
                    token = None
        return token

    @classmethod
    def generate_auth_header(cls, token: TokenResponse) -> dict[str, str]:
        return {
            "Authorization": f"{token.token_type} {token.access_token}"
        }

    @classmethod
    def __token_has_expired(cls) -> bool:
        converted_expiry = dt.datetime(1970, 1, 1) + dt.timedelta(seconds=cls.token.created_at)
        return converted_expiry + dt.timedelta(seconds=cls.token.expires_in) < dt.datetime.utcnow()

    @classmethod
    def __generate_params(cls, settings: cda.CdaSettings) -> dict[str, str]:
        return {
            'grant_type': 'client_credentials',
            'client_id': settings.cda_uid,
            'client_secret': settings.cda_secret
        }
