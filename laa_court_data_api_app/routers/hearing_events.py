import structlog
from uuid import UUID

from fastapi import APIRouter, Query
from fastapi.responses import Response

from laa_court_data_api_app.internal.court_data_adaptor_client import CourtDataAdaptorClient
from laa_court_data_api_app.models.hearing_events.hearing_events_response import HearingEventsResponse
from laa_court_data_api_app.models.hearing_events.hearing_events_result import HearingEventsResult

logger = structlog.get_logger(__name__)
router = APIRouter()


@router.get("/v2/hearing_events/{hearing_id}", response_model=HearingEventsResponse, status_code=200)
async def get_hearing_events(hearing_id: UUID, date: str = Query(None, example="2001-01-20")):
    logger.info("Hearing_Events_Get", hearing_id=hearing_id, hearing_date=date)
    client = CourtDataAdaptorClient()
    cda_response = await client.get(f'/api/internal/v2/hearings/{hearing_id}/event_log/{date}')

    if cda_response is None:
        logger.error("Hearing_Events_Endpoint_Did_Not_Return")
        return Response(status_code=424)

    match cda_response.status_code:
        case 200:
            logger.info("Hearing_Events_Endpoint_Returned_Success")
            hearing_events_result = HearingEventsResult(**cda_response.json())
            return HearingEventsResponse(**hearing_events_result.dict())
        case 400:
            logger.warn("Hearing_Events_Endpoint_Validation_Failed")
            return Response(status_code=400)
        case 404:
            logger.info("Hearing_Events_Endpoint_Not_Found")
            return Response(status_code=404)
        case _:
            logger.error("Hearing_Events_Endpoint_Error_Returning", status_code=cda_response.status_code)
            return Response(status_code=424)
