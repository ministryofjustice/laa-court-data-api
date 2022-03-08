import logging

from fastapi import APIRouter
from fastapi.responses import Response

from laa_court_data_api_app.internal.court_data_adaptor_client import CourtDataAdaptorClient
from laa_court_data_api_app.models.hearing.hearing_result import HearingResult

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/v2/hearing/{hearing_id}", status_code=200)
async def get_hearing(hearing_id: str):
    logger.info("Calling_Hearing_Get_Endpoint")
    logging.info(f"Hearing_Get_{hearing_id}")
    client = CourtDataAdaptorClient()
    cda_response = await client.get(f"/api/internal/v2/hearing_results/{hearing_id}")

    return HearingResult(**cda_response.json())
