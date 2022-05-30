from uuid import UUID

import structlog
from fastapi import APIRouter
from fastapi.responses import Response

import laa_court_data_api_app.constants.endpoint_constants as endpoints
from laa_court_data_api_app.internal.court_data_adaptor_client import CourtDataAdaptorClient
from laa_court_data_api_app.models.defendants.defendant_summary import DefendantSummary
from laa_court_data_api_app.models.defendants.defendants_response import DefendantsResponse
from laa_court_data_api_app.models.prosecution_cases.prosecution_cases_results import ProsecutionCasesResults

logger = structlog.get_logger(__name__)

router = APIRouter()


@router.get('/v2/defendants', response_model=DefendantsResponse, status_code=200)
async def get_defendants(urn: str | None = None,
                         name: str | None = None,
                         dob: str | None = None,
                         uuid: UUID | None = None,
                         asn: str | None = None,
                         nino: str | None = None):
    client = CourtDataAdaptorClient()
    logger.info("Calling_Defendants_Get_Endpoint")

    if name and dob:
        cda_response = await client.get(endpoints.PROSECUTION_CASES_ENDPOINT,
                                        params={"filter[name]": name, "filter[date_of_birth]": dob})
    elif urn and uuid:
        cda_response = await client.get(f"{endpoints.PROSECUTION_CASES_ENDPOINT}/{urn}/defendants/{uuid}")
    elif urn:
        cda_response = await client.get(endpoints.PROSECUTION_CASES_ENDPOINT,
                                        params={"filter[prosecution_case_reference]": urn})
    elif asn:
        cda_response = await client.get(endpoints.PROSECUTION_CASES_ENDPOINT,
                                        params={"filter[arrest_summons_number]": asn})
    elif nino:
        cda_response = await client.get(endpoints.PROSECUTION_CASES_ENDPOINT,
                                        params={"filter[national_insurance_number]": nino})
    else:
        logger.error("Invalid_Defendant_Search")
        return Response(status_code=400)

    if cda_response is None:
        # Log will only output one of the parameters based on the call made
        logger.error("Prosecution_Case_Endpoint_Did_Not_Return",
                     urn=urn, name=name, uuid=uuid, asn=asn, nino=nino)
        return Response(status_code=424)

    logger.info("Defendants_Response_Returned_Status_Code", status_code=cda_response.status_code)

    match cda_response.status_code:
        case 200:
            if urn and uuid:
                defendant_summary = map_defendant_summary(DefendantSummary(**cda_response.json()), urn)
                summaries = [defendant_summary]
                logger.info("Defendants_To_Show", entries=len(summaries))
                return DefendantsResponse(defendant_summaries=summaries)
            summaries = map_defendants(ProsecutionCasesResults(**cda_response.json()))
            logger.info("Defendants_To_Show", entries=len(summaries))
            return DefendantsResponse(defendant_summaries=summaries)
        case 400:
            logger.warn("Prosecution_Case_Endpoint_Validation_Failed")
            return Response(status_code=400)
        case 404:
            logger.info("Prosecution_Case_Endpoint_Not_Found")
            return Response(status_code=404)
        case _:
            logger.error("Prosecution_Case_Endpoint_Error_Returning", status_code=cda_response.status_code)
            return Response(status_code=424)


def map_defendants(prosecution_case_results: ProsecutionCasesResults) -> list[DefendantSummary]:
    response_list = []
    for result in prosecution_case_results.results:
        for summary in result.defendant_summaries:
            mapped_model = map_defendant_summary(summary, result.prosecution_case_reference)
            response_list.append(mapped_model)

    return response_list


def map_defendant_summary(defendant_summary: DefendantSummary, prosecution_case_reference: str):
    mapped_model = DefendantSummary(**defendant_summary.dict())
    full_name = build_full_name(defendant_summary.first_name,
                                defendant_summary.middle_name,
                                defendant_summary.last_name)
    mapped_model.name = full_name
    mapped_model.prosecution_case_reference = prosecution_case_reference

    return mapped_model


def build_full_name(first_name: str, middle_name: str, last_name: str):
    out_str = ''
    if first_name:
        out_str += first_name
    if middle_name:
        out_str += f' {middle_name}'
    if last_name:
        out_str += f' {last_name}'

    return out_str
