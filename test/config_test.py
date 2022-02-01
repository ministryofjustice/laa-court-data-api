from laa_court_data_api_app.config.app import get_app_settings
import os


def test_app_settings_returns_properties():
    get_app_settings.cache_clear()
    settings = get_app_settings()
    assert hasattr(settings, "app_name")
    assert hasattr(settings, "commit_id")
    assert hasattr(settings, "build_date")
    assert hasattr(settings, "build_tag")
    assert hasattr(settings, "app_branch")


def test_environment_variable_passes_to_app_settings():
    get_app_settings.cache_clear()
    os.environ["APP_NAME"] = "Test App"
    settings = get_app_settings()
    assert settings.app_name == "Test App"
