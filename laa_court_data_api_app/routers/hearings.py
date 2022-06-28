import structlog
from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import Response

import laa_court_data_api_app.constants.endpoint_constants as endpoints
from laa_court_data_api_app.internal.court_data_adaptor_client import CourtDataAdaptorClient
from laa_court_data_api_app.models.hearing.internal.hearing_result import HearingResult as InternalHearingResult
from laa_court_data_api_app.models.hearing.external.hearing_result import HearingResult as ExternalHearingResult

logger = structlog.get_logger(__name__)
router = APIRouter()


@router.get("/v2/hearings/{hearing_id}", response_model=ExternalHearingResult, status_code=200)
async def get_hearing(hearing_id: UUID, date: str):
    logger.info("Hearing_Get", hearing_id=hearing_id, date=date)
    client = CourtDataAdaptorClient()
    cda_response = await client.get(f"{endpoints.HEARING_RESULTS_ENDPOINT}/{hearing_id}", params={'sitting_day': date})

    if cda_response is None:
        logger.error("Hearing_Results_Endpoint_Did_Not_Return", hearing_id=hearing_id)
        return Response(status_code=424)

    match cda_response.status_code:
        case 200:
            logger.info("Hearing_Results_Endpoint_Returned_Success")
            internal_result = InternalHearingResult(**cda_response.json())
            return ExternalHearingResult(**internal_result.dict())
        case 400:
            logger.warn("Hearing_Results_Endpoint_Validation_Failed")
            return Response(status_code=400)
        case 404:
            logger.info("Hearing_Results_Endpoint_Not_Found")
            return Response(status_code=404)
        case _:
            logger.error("Hearing_Results_Endpoint_Error_Returning", status_code=cda_response.status_code)
            return Response(status_code=424)
