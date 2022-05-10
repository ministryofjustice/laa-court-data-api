import structlog

from fastapi import APIRouter
from fastapi.responses import Response

from laa_court_data_api_app.internal.court_data_adaptor_client import CourtDataAdaptorClient
from laa_court_data_api_app.models.hearing_summaries.defendants import Defendants
from laa_court_data_api_app.models.hearing_summaries.hearing_summaries_response import HearingSummariesResponse
from laa_court_data_api_app.models.hearing_summaries.hearing_summary import HearingSummary
from laa_court_data_api_app.models.prosecution_cases.defendant_summary import DefendantSummary
from laa_court_data_api_app.models.prosecution_cases.prosecution_cases import ProsecutionCases
from laa_court_data_api_app.models.prosecution_cases.prosecution_cases_results import ProsecutionCasesResults

logger = structlog.get_logger(__name__)
router = APIRouter()


@router.get("/v2/hearingsummaries/{urn}", response_model=HearingSummariesResponse, status_code=200)
async def get_hearing_summaries(urn: str):
    logger.info("Hearing_Summaries_Get", urn=urn)
    client = CourtDataAdaptorClient()
    cda_response = await client.get("/api/internal/v2/prosecution_cases",
                                    params={"filter[prosecution_case_reference]": urn})

    if cda_response is None:
        logger.error("Prosecution_Case_Endpoint_Did_Not_Return", urn=urn)
        return Response(status_code=424)

    match cda_response.status_code:
        case 200:
            logger.info("Prosecution_Case_Endpoint_Returned_Success")
            prosecution_case_results = ProsecutionCasesResults(**cda_response.json())
            summaries = map_hearing_summaries(prosecution_case_results.results)
            logger.info("Hearing_Summaries_To_Show", count=len(summaries))
            return HearingSummariesResponse(prosecution_case_reference=urn,
                                            hearing_summaries=summaries,
                                            overall_defendants=map_defendant_list(prosecution_case_results.results))
        case 400:
            logger.warn("Prosecution_Case_Endpoint_Validation_Failed")
            return Response(status_code=400)
        case 404:
            logger.info("Prosecution_Case_Endpoint_Not_Found")
            return Response(status_code=404)
        case _:
            logger.error("Prosecution_Case_Endpoint_Error_Returning", status_code=cda_response.status_code)
            return Response(status_code=424)


def map_defendant_list(prosecution_case_results: list[ProsecutionCases]):
    defendant_list = []
    for result in prosecution_case_results:
        for defendant in result.defendant_summaries:
            defendant_list.extend(map_defendants_from_guids([str(defendant.id)], result.defendant_summaries))

    return defendant_list


def map_hearing_summaries(prosecution_case_results: list[ProsecutionCases]):
    hearing_summaries = []
    for result in prosecution_case_results:
        for summary in result.hearing_summaries:
            return_summary = HearingSummary(**summary.dict())
            return_summary.defendants = map_defendants_from_guids(summary.defendant_ids, result.defendant_summaries)

            hearing_summaries.append(return_summary)

    return hearing_summaries


def map_defendants_from_guids(defendant_ids: list[str], defendant_summaries: list[DefendantSummary]):
    defendant_list = []
    for defendant_id in defendant_ids:
        filtered_defendant_summaries = filter(lambda defendants: str(defendants.id) == defendant_id,
                                              defendant_summaries)
        for defendant_obj in list(filtered_defendant_summaries):
            if defendant_obj is not None:
                new_def = Defendants(**defendant_obj.dict())
                defendant_list.append(new_def)
                if defendant_obj.offence_summaries is not None and len(defendant_obj.offence_summaries) > 0:
                    new_def.maat_reference = defendant_obj.offence_summaries[0].laa_application.reference

    return defendant_list
