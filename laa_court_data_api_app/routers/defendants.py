import structlog
from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import Response

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
        logger.info("Defendants_Get_Name_And_Dob_Filtered")
        cda_response = await client.get("/api/internal/v2/prosecution_cases",
                                        params={"filter[name]": name, "filter[date_of_birth]": dob})
    elif urn and uuid:
        logger.info(f"Defendants_Get_Urn_And_Uuid_{urn}_{uuid}")
        cda_response = await client.get(f"/api/internal/v2/prosecution_cases/{urn}/defendants/{uuid}")
    elif urn:
        logger.info(f"Defendants_Get_Urn_{urn}")
        cda_response = await client.get("/api/internal/v2/prosecution_cases",
                                        params={"filter[prosecution_case_reference]": urn})
    elif asn:
        logger.info(f"Defendants_Get_Asn_{asn}")
        cda_response = await client.get("/api/internal/v2/prosecution_cases",
                                        params={"filter[arrest_summons_number]": asn})
    elif nino:
        logger.info(f"Defendants_Get_Nino_{nino}")
        cda_response = await client.get("/api/internal/v2/prosecution_cases",
                                        params={"filter[national_insurance_number]": nino})
    else:
        logger.error("Invalid_Defendant_Search")
        return Response(status_code=400)

    if cda_response is None:
        logger.error("Prosecution_Case_Endpoint_Did_Not_Return")
        return Response(status_code=424)

    logger.info(f"Defendants_Response_Returned_Status_Code_{cda_response.status_code}")

    match cda_response.status_code:
        case 200:
            if urn and uuid:
                summaries = [cda_response.json()]
                logger.info("Defendants_To_Show", entries=len(summaries))
                return DefendantsResponse(defendant_summaries=summaries)
            summaries = map_defendants(ProsecutionCasesResults(**cda_response.json()))
            logger.info("Defendants_To_Show", entries=len(summaries))
            return DefendantsResponse(defendant_summaries=summaries)
        case 400:
            logger.info("Prosecution_Case_Endpoint_Validation_Failed")
            return Response(status_code=400)
        case 404:
            logger.info("Prosecution_Case_Endpoint_Not_Found")
            return Response(status_code=404)
        case _:
            logger.error("Prosecution_Case_Endpoint_Error_Returning")
            return Response(status_code=424)


def map_defendants(prosecution_case_results: ProsecutionCasesResults) -> list[DefendantSummary]:
    response_list = []
    for result in prosecution_case_results.results:
        for summary in result.defendant_summaries:
            mapped_model = DefendantSummary(prosecution_case_reference=result.prosecution_case_reference,
                                            **summary.dict())
            full_name = f'{summary.first_name} {summary.middle_name} {summary.last_name}'
            mapped_model.name = full_name
            response_list.append(mapped_model)

    return response_list
