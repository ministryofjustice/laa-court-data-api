import logging
from fastapi import APIRouter
from laa_court_data_api_app.internal import court_data_adaptor_client
from laa_court_data_api_app.models.prosecution_cases.prosecution_cases_results import ProsecutionCasesResults

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
        defendants = prosecution_case_results.results[0].defendant_summaries
        return defendants

@router.get('/defendant')
async def get_defendant(urn: str | None):
    logger.debug('Calling GET Endpoint')
    results = {"defendantData": "true"}
    return results
