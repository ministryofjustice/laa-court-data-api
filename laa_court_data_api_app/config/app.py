from pydantic import BaseSettings
from functools import lru_cache


class AppSettings(BaseSettings):
    app_name: str

    class Config:
        env_file = "config/.env"
        env_file_encoding = 'utf-8'


@lru_cache()
def get_app_settings():
    return AppSettings()
