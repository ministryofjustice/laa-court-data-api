import logging
from uuid import UUID

from fastapi import APIRouter, Query
from fastapi.responses import Response

from laa_court_data_api_app.internal.court_data_adaptor_client import CourtDataAdaptorClient
from laa_court_data_api_app.models.hearing_events.hearing_events_response import HearingEventsResponse
from laa_court_data_api_app.models.hearing_events.hearing_events_result import HearingEventsResult

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/v2/hearing_events/{hearing_id}", response_model=HearingEventsResponse, status_code=200)
async def get_hearing_events(hearing_id: UUID, date: str = Query(None, example="2001-01-20")):
    logger.info("Calling_Hearing_Events_Get_Endpoint")
    logging.info(f"Hearing_Events_Get_{hearing_id}_{date}")
    client = CourtDataAdaptorClient()
    cda_response = await client.get(f'/api/internal/v2/hearings/{hearing_id}/event_log/{date}')

    if cda_response is None:
        logging.error("Hearing_Events_Endpoint_Did_Not_Return")
        return Response(status_code=424)

    match cda_response.status_code:
        case 200:
            logging.info("Hearing_Events_Endpoint_Returned_Success")
            hearing_events_result = HearingEventsResult(**cda_response.json())
            return HearingEventsResponse(**hearing_events_result.dict())
        case 400:
            logging.info("Hearing_Events_Endpoint_Validation_Failed")
            return Response(status_code=400)
        case 404:
            logging.info("Hearing_Events_Endpoint_Not_Found")
            return Response(status_code=404)
        case _:
            logging.info("Hearing_Events_Endpoint_Error_Returning")
            return Response(status_code=424)
