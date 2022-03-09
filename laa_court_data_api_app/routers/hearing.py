import logging
from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import Response

from laa_court_data_api_app.internal.court_data_adaptor_client import CourtDataAdaptorClient
from laa_court_data_api_app.models.hearing.hearing_result import HearingResult

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/v2/hearing/{hearing_results_id}", response_model=HearingResult, status_code=200)
async def get_hearing(hearing_results_id: UUID):
    logger.info("Calling_Hearing_Get_Endpoint")
    logging.info(f"Hearing_Get_{hearing_results_id}")
    client = CourtDataAdaptorClient()
    cda_response = await client.get(f"/api/internal/v2/hearing_results/{hearing_results_id}")

    if cda_response is None:
        logging.error("Hearing_Results_Endpoint_Did_Not_Return")
        return Response(status_code=424)

    match cda_response.status_code:
        case 200:
            logging.info("Hearing_Results_Endpoint_Returned_Success")
            return HearingResult(**cda_response.json())
        case 400:
            logging.info("Hearing_Results_Endpoint_Validation_Failed")
            return Response(status_code=400)
        case 404:
            logging.info("Hearing_Results_Endpoint_Not_Found")
            return Response(status_code=404)
        case _:
            logging.info("Hearing_Results_Endpoint_Error_Returning")
            return Response(status_code=424)
