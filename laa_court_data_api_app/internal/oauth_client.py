import datetime as dt
import structlog

import httpx

from ..config.court_data_adaptor import CdaSettings, get_cda_settings
from ..models.token_response import TokenResponse

logger = structlog.get_logger(__name__)


class OauthClient:
    __instance = None
    __token = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(OauthClient, cls).__new__(cls)
        return cls.__instance

    @property
    def token(self) -> TokenResponse:
        return self.__token

    @token.setter
    def token(self, value):
        self.__token = value

    @property
    def settings(self) -> CdaSettings:
        return get_cda_settings()

    async def retrieve_token(self) -> TokenResponse:
        logger.debug("OAuth_Retrieving_token")
        if self.token is None or self.token_has_expired():
            logger.debug("Token_expired_or_missing")
            async with httpx.AsyncClient(base_url=self.settings.cda_endpoint) as client:
                response = await client.post("/oauth/token", data=self.generate_params(self.settings))
                if response.status_code == 200:
                    logger.debug("Token_Retrieved_From_Service")
                    self.token = TokenResponse(**response.json())
                else:
                    logger.debug("Unable_To_Retrieve_Token")
                    self.token = None
        return self.token

    def token_has_expired(self) -> bool:
        converted_expiry = dt.datetime(1970, 1, 1) + dt.timedelta(seconds=self.token.created_at)
        return converted_expiry + dt.timedelta(seconds=self.token.expires_in) < dt.datetime.utcnow()

    @staticmethod
    def generate_params(settings: CdaSettings) -> dict[str, str]:
        try:
            return {
                'grant_type': 'client_credentials',
                'client_id': settings.cda_uid,
                'client_secret': settings.cda_secret
            }
        except AttributeError as e:
            logger.error("Error_Generating_OAuth_Parameters", exception=e)
            raise e

    @staticmethod
    def generate_auth_header(token: TokenResponse) -> dict[str, str]:
        try:
            if token.access_token is None:
                raise AttributeError("token.access_token is not found")
            return {
                "Authorization": f"{token.token_type} {token.access_token}"
            }
        except AttributeError as e:
            logger.error("Error_Generating_Header", exception=e)
            raise e
