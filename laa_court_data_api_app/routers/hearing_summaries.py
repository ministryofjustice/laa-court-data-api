import logging

from fastapi import APIRouter

from laa_court_data_api_app.internal.court_data_adaptor_client import CourtDataAdaptorClient
from laa_court_data_api_app.models.hearing_summaries.hearing_summaries_response import HearingSummariesResponse
from laa_court_data_api_app.models.prosecution_cases.prosecution_cases_results import ProsecutionCasesResults

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/v2/hearingsummaries/{urn}", response_model=HearingSummariesResponse)
async def get_hearing_summaries(urn: str):
    logging.info(f"Hearing_Summaries_Get_{urn}")
    client = CourtDataAdaptorClient()
    cda_response = await client.get("/api/internal/v2/prosecution_cases",
                                    params={"filter[prosecution_case_reference]": urn})

    logging.info(f"Response_Returned_Status_Code_{cda_response.status_code}")

    if cda_response.status_code == 200:
        prosecution_case_results = ProsecutionCasesResults(**cda_response.json())
        hearing_summaries = [x.hearing_summaries for x in prosecution_case_results.results]
        summaries = [item for sublist in hearing_summaries for item in sublist]
        return HearingSummariesResponse(hearing_summaries=summaries)
