import structlog
from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import Response

from laa_court_data_api_app.internal.court_data_adaptor_client import CourtDataAdaptorClient
from laa_court_data_api_app.models.hearing.internal.hearing_result import HearingResult as InternalHearingResult
from laa_court_data_api_app.models.hearing.external.hearing_result import HearingResult as ExternalHearingResult

logger = structlog.get_logger(__name__)
router = APIRouter()


@router.get("/v2/hearing/{hearing_id}", response_model=ExternalHearingResult, status_code=200)
async def get_hearing(hearing_id: UUID):
    logger.info("Calling_Hearing_Get_Endpoint")
    logger.info(f"Hearing_Get_{hearing_id}")
    client = CourtDataAdaptorClient()
    cda_response = await client.get(f"/api/internal/v2/hearing_results/{hearing_id}")

    if cda_response is None:
        logger.error("Hearing_Results_Endpoint_Did_Not_Return")
        return Response(status_code=424)

    match cda_response.status_code:
        case 200:
            logger.info("Hearing_Results_Endpoint_Returned_Success")
            internal_result = InternalHearingResult(**cda_response.json())
            return ExternalHearingResult(**internal_result.dict())
        case 400:
            logger.info("Hearing_Results_Endpoint_Validation_Failed")
            return Response(status_code=400)
        case 404:
            logger.info("Hearing_Results_Endpoint_Not_Found")
            return Response(status_code=404)
        case _:
            logger.info("Hearing_Results_Endpoint_Error_Returning")
            return Response(status_code=424)
