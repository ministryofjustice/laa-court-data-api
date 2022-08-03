from fastapi import APIRouter, Depends
from laa_court_data_api_app.config.app import AppSettings, get_app_settings
from laa_court_data_api_app.config.secure_headers import SecureJsonResponse
from laa_court_data_api_app.models.ping import Ping

router = APIRouter()


@router.get('/ping', response_model=Ping)
async def ping(settings: AppSettings = Depends(get_app_settings)):
    results = Ping(
        app_branch=settings.app_branch,
        build_date=settings.build_date,
        build_tag=settings.build_tag,
        commit_id=settings.commit_id
        )

    return SecureJsonResponse(status_code=200, content=results)
