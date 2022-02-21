import logging
from typing import Optional
from uuid import UUID

from fastapi import APIRouter
from laa_court_data_api_app.internal import court_data_adaptor_client
from laa_court_data_api_app.models.prosecution_cases.prosecution_cases_results import ProsecutionCasesResults
from laa_court_data_api_app.models.defendants.defendants_response import DefendantsResponse

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get('/v2/defendant')
async def get_defendant(urn: Optional[str] = None,
                        name: Optional[str] = None,
                        dob: Optional[str] = None,
                        uuid: Optional[UUID] = None):
    logger.info('Calling GET Endpoint')

    if name and dob:
        logging.info(f"Defendants_Get_{name}_And_{dob}")
        cda_response = await court_data_adaptor_client.get("/api/internal/v2/prosecution_cases",
                                                           params={"filter[name]": name, "filter[date_of_birth]": dob})
    elif urn and uuid:
        logging.info(f"Defendants_Get_{urn}_And_{uuid}")
        cda_response = await court_data_adaptor_client.get(f"/api/internal/v2/prosecution_cases/{urn}/defendants/{uuid}")
        return cda_resonse.json()

    elif urn:
        logging.info(f"Defendants_Get_{urn}")
        cda_response = await court_data_adaptor_client.get("/api/internal/v2/prosecution_cases",
                                                           params={"filter[prosecution_case_reference]": urn})
    else:
        logger.error('Invalid_Search')
        return


    logger.info(f"Response_Returned_Status_Code_{cda_response.status_code}")

    if cda_response.status_code == 200:
        prosecution_case_results = ProsecutionCasesResults(**cda_response.json())
        results = [x.defendant_summaries for x in prosecution_case_results.results]
        defendant_summaries = defendant_summaries=[x for x in results]
        summaries = [item for sublist in defendant_summaries for item in sublist]
        return DefendantsResponse(defendant_summaries=summaries)
