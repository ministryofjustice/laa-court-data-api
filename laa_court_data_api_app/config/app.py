from pydantic import BaseSettings
from functools import lru_cache
from typing import Optional


class AppSettings(BaseSettings):
    app_name: str = "LAA Court Data API"
    app_repo: str = "https://www.github.com/ministryofjustice/laa-court-data-api"
    contact_email: str = "assessaclaim@digital.justice.gov.uk"
    contact_team: str = "Assess a Claim"
    commit_id: Optional[str] = None
    build_date: Optional[str] = None
    build_tag: Optional[str] = None
    app_branch: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


@lru_cache()
def get_app_settings():
    return AppSettings()
