import logging

from fastapi import APIRouter
from fastapi.responses import Response

from laa_court_data_api_app.internal.court_data_adaptor_client import CourtDataAdaptorClient
from laa_court_data_api_app.models.hearing_summaries.defendants import Defendants
from laa_court_data_api_app.models.hearing_summaries.hearing_summaries_response import HearingSummariesResponse
from laa_court_data_api_app.models.hearing_summaries.hearing_summary import HearingSummary
from laa_court_data_api_app.models.prosecution_cases.prosecution_cases import ProsecutionCases
from laa_court_data_api_app.models.prosecution_cases.prosecution_cases_results import ProsecutionCasesResults

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/v2/hearingsummaries/{urn}", response_model=HearingSummariesResponse, status_code=200)
async def get_hearing_summaries(urn: str):
    logger.info("Calling_Hearing_Summaries_Get_Endpoint")
    logging.info(f"Hearing_Summaries_Get_{urn}")
    client = CourtDataAdaptorClient()
    cda_response = await client.get("/api/internal/v2/prosecution_cases",
                                    params={"filter[prosecution_case_reference]": urn})

    if cda_response is None:
        logging.error("Prosecution_Case_Endpoint_Did_Not_Return")
        return Response(status_code=424)

    match cda_response.status_code:
        case 200:
            logging.info("Prosecution_Case_Endpoint_Returned_Success")
            prosecution_case_results = ProsecutionCasesResults(**cda_response.json())
            summaries = map_hearing_summaries(prosecution_case_results.results)
            logging.info(f"Hearing_Summaries_To_Show: {summaries.count}")
            return HearingSummariesResponse(hearing_summaries=summaries)
        case 400:
            logging.info("Prosecution_Case_Endpoint_Validation_Failed")
            return Response(status_code=400)
        case 404:
            logging.info("Prosecution_Case_Endpoint_Not_Found")
            return Response(status_code=404)
        case _:
            logging.error("Prosecution_Case_Endpoint_Error_Returning")
            return Response(status_code=424)

def map_hearing_summaries(prosecution_case_results: list[ProsecutionCases]):
    hearing_summaries = []
    for result in prosecution_case_results:
        for summary in result.hearing_summaries:
            return_summary = HearingSummary(**summary.dict())
            for defendant in summary.defendant_ids:
                defendant_result = filter(lambda defendants: str(defendants.id) == defendant, result.defendant_summaries)
                for defendant_obj in list(defendant_result):
                    if defendant_obj is not None:
                        new_def = Defendants(**defendant_obj.dict())
                        return_summary.defendants.append(new_def)

            hearing_summaries.append(return_summary)

    return hearing_summaries
