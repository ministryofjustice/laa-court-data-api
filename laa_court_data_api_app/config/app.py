from pydantic import BaseSettings
from functools import lru_cache


class AppSettings(BaseSettings):
    app_name: str = "LAA Court Data API"
    app_repo: str = "https://www.github.com/ministryofjustice/laa-court-data-api"
    contact_email: str = "assessaclaim@digital.justice.gov.uk"
    contact_team: str = "Assess a Claim"
    commit_id: str | None
    build_date: str | None
    build_tag: str | None
    app_branch: str | None
    sentry_dsn: str | None

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


@lru_cache()
def get_app_settings():
    return AppSettings()
