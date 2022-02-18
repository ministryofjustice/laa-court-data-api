import logging
from fastapi import APIRouter
from laa_court_data_api_app.internal import court_data_adaptor_client
from laa_court_data_api_app.models.prosecution_cases.prosecution_cases_results import ProsecutionCasesResults
from laa_court_data_api_app.models.defendants.defendants_response import DefendantsResponse

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get('/v2/defendant/{urn}')
async def get_defendant(urn: str):
    logger.info('Calling GET Endpoint')
    cda_response = await court_data_adaptor_client.get("/api/internal/v2/prosecution_cases",
                                                       params={"filter[prosecution_case_reference]": urn})

    logger.info(f"Response_Returned_Status_Code_{cda_response.status_code}")

    if cda_response.status_code == 200:
        prosecution_case_results = ProsecutionCasesResults(**cda_response.json())
        results = [x.defendant_summaries for x in prosecution_case_results.results]
        defendant_summaries = defendant_summaries=[x for x in results]
        summaries = [item for sublist in defendant_summaries for item in sublist]
        return DefendantsResponse(defendant_summaries=summaries)
