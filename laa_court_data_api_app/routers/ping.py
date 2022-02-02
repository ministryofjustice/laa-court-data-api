import os
import logging
from fastapi import APIRouter

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get('/ping')
async def ping():
    logger.debug('Calling GET Ping Endpoint')
    results = {'app_branch': os.getenv('APP_BRANCH'),
               'build_date': os.getenv('BUILD_DATE'),
               'build_tag': os.getenv('BUILD_TAG'),
               'commit_id': os.getenv('COMMIT_ID')}
    return results
