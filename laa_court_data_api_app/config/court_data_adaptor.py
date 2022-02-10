from pydantic import BaseSettings
from functools import lru_cache


class CdaSettings(BaseSettings):
    cda_endpoint: str
    cda_uid: str
    cda_secret: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_cda_settings():
    return CdaSettings()
