from pydantic import BaseSettings
from functools import lru_cache
from typing import Optional


class AppSettings(BaseSettings):
    app_name: str = "Court Data API"
    commit_id: Optional[str]
    build_date: Optional[str]
    build_tag: Optional[str]
    app_branch: Optional[str]

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


@lru_cache()
def get_app_settings():
    return AppSettings()
