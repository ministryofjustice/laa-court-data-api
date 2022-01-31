from pydantic import BaseSettings


class AppSettings(BaseSettings):
    app_name: str

    class Config:
        env_file = "config/.env"
        env_file_encoding = 'utf-8'


def get_app_settings():
    return AppSettings()
