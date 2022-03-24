import logging
from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import Response

from laa_court_data_api_app.internal.court_data_adaptor_client import CourtDataAdaptorClient
from laa_court_data_api_app.models.defendants.defendants_response import DefendantsResponse
from laa_court_data_api_app.models.prosecution_cases.prosecution_cases_results import ProsecutionCasesResults

logger = logging.getLogger(__name__)

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
        logging.info("Defendants_Get_Name_And_Dob_Filtered")
        cda_response = await client.get("/api/internal/v2/prosecution_cases",
                                        params={"filter[name]": name, "filter[date_of_birth]": dob})
    elif urn and uuid:
        logging.info(f"Defendants_Get_Urn_And_Uuid_{urn}_{uuid}")
        cda_response = await client.get(f"/api/internal/v2/prosecution_cases/{urn}/defendants/{uuid}")
    elif urn:
        logging.info(f"Defendants_Get_Urn_{urn}")
        cda_response = await client.get("/api/internal/v2/prosecution_cases",
                                        params={"filter[prosecution_case_reference]": urn})
    elif asn:
        logging.info(f"Defendants_Get_asn_{asn}")
        cda_response = await client.get("/api/internal/v2/prosecution_cases",
                                        params={"filter[arrest_summons_number]": asn})
    elif nino:
        logging.info(f"Defendants_Get_nino_{nino}")
        cda_response = await client.get("/api/internal/v2/prosecution_cases",
                                        params={"filter[national_insurance_number]": nino})
    else:
        logger.error("Invalid_Defendant_Search")
        return Response(status_code=400)

    if cda_response is None:
        logging.error("Prosecution_Case_Endpoint_Did_Not_Return")
        return Response(status_code=424)

    logger.info(f"Defendants_Response_Returned_Status_Code_{cda_response.status_code}")

    match cda_response.status_code:
        case 200:
            if urn and uuid:
                summaries = [cda_response.json()]
                logging.info(f"Defendants_To_Show: {summaries.count}")
                return DefendantsResponse(defendant_summaries=summaries)
            prosecution_case_results = ProsecutionCasesResults(**cda_response.json())
            defendant_summaries = [x.defendant_summaries for x in prosecution_case_results.results]
            summaries = [item for sublist in defendant_summaries for item in sublist]
            logging.info(f"Defendants_To_Show: {summaries.count}")
            return DefendantsResponse(defendant_summaries=summaries)
        case 400:
            logging.info("Prosecution_Case_Endpoint_Validation_Failed")
            return Response(status_code=400)
        case 404:
            logging.info("Prosecution_Case_Endpoint_Not_Found")
            return Response(status_code=404)
        case _:
            logging.error("Prosecution_Case_Endpoint_Error_Returning")
            return Response(status_code=424)
