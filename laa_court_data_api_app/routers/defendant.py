import logging
from fastapi import APIRouter

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get('/defendant')
async def get_defendant(urn: str | None):
    logger.debug('Calling GET Endpoint')
    results = {"defendantData": "true"}
    return results
