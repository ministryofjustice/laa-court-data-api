import os
import logging
from fastapi import APIRouter
from laa_court_data_api_app.config.app import get_app_settings

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get('/ping')
async def ping():
    logger.debug('Calling GET Endpoint')
    settings = get_app_settings()
    results = {'app_branch': settings.app_branch,
               'build_date': settings.build_date,
               'build_tag': settings.build_tag,
               'commit_id': settings.commit_id}
    return results
