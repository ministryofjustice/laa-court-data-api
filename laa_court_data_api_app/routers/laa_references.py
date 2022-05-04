import structlog
import re

from fastapi import APIRouter
from fastapi.responses import Response, JSONResponse

from laa_court_data_api_app.internal.court_data_adaptor_client import CourtDataAdaptorClient
from laa_court_data_api_app.models.laa_references.external.request.laa_references_patch_request import \
    LaaReferencesPatchRequest as ExternalPatchRequest
from laa_court_data_api_app.models.laa_references.external.request.laa_references_post_request import \
    LaaReferencesPostRequest as ExternalPostRequest
from laa_court_data_api_app.models.laa_references.external.response.laa_references_error_response import \
    LaaReferencesErrorResponse
from laa_court_data_api_app.models.laa_references.internal.request.laa_references_patch_request import \
    LaaReferencesPatchRequest as InternalPatchRequest
from laa_court_data_api_app.models.laa_references.internal.request.laa_references_patch_request import \
    LaaReferencesPatch as InternalPatch
from laa_court_data_api_app.models.laa_references.internal.request.laa_references_post_request import \
    LaaReferencesPost as InternalPost
from laa_court_data_api_app.models.laa_references.internal.request.laa_references_post_request import \
    LaaReferencesPostRequest as InternalPostRequest

logger = structlog.get_logger(__name__)
router = APIRouter()

responses = {
    202: {"description": "Request has been accepted"},
    400: {"description": "Validation has failed", "model": LaaReferencesErrorResponse},
    422: {"description": "Request cannot be processed", "model": LaaReferencesErrorResponse},
    424: {"description": "Error with Upstream service"}
}


@router.patch("/v2/laa_references/{defendant_id}/", status_code=202, responses=responses)
async def patch_maat_unlink(defendant_id: str, request: ExternalPatchRequest):
    if (defendant_id != str(request.defendant_id)):
        logger.info("Mismatched_DefendantId_In_Patch_Request")
        return JSONResponse(status_code=400, content=LaaReferencesErrorResponse(
            error={'defendant_id': ['mismatch in ids given']}).dict())

    logger.info("Calling_Maat_Patch", defendant_id=defendant_id)
    client = CourtDataAdaptorClient()
    cda_response = await client.patch(f'/api/internal/v2/laa_references/{defendant_id}',
                                      body=InternalPatchRequest(laa_reference=InternalPatch(**request.dict())))

    return formulated_response(cda_response, defendant_id, "Unlinking")


@router.post("/v2/laa_references", status_code=202, responses=responses)
async def post_maat_link(request: ExternalPostRequest):
    logger.info("Calling_Maat_Post", defendant_id=request.defendant_id)
    client = CourtDataAdaptorClient()

    cda_response = await client.post("/api/internal/v2/laa_references/",
                                     body=InternalPostRequest(laa_reference=InternalPost(**request.dict())))

    return formulated_response(cda_response, request.defendant_id, "Linking")


def formulated_response(cda_response, defendant_id, request_type):
    if cda_response is None:
        logger.error("Laa_References_Endpoint_Did_Not_Return")
        return Response(status_code=424)

    match cda_response.status_code:
        case 202:
            logger.info(f"Maat_Id_For_{request_type}_Successfully_Requested", defendant_id=defendant_id)
            return Response(status_code=202)
        case 400:
            logger.info(f"Validation_Failed_For_{request_type}", defendant_id=defendant_id)
            return JSONResponse(status_code=400,
                                content=LaaReferencesErrorResponse(
                                    error=cda_response.json()).dict())
        case 404:
            logger.info("Laa_References_Endpoint_Not_Found")
            return Response(status_code=404)
        case 422:
            logger.info(f"Unable_To_Process_{request_type}", defendant_id=defendant_id)
            return JSONResponse(status_code=422,
                                content=LaaReferencesErrorResponse(
                                    error=parse_error_response(cda_response.json()["error"])).dict())
        case _:
            logger.error("Laa_References_Endpoint_Error_Returning")
            return Response(status_code=424)


def parse_error_response(response):
    error_string = re.findall(r"{.*?}", response)
    error_dict = re.findall(r":(.*?)=>\[\"(.*?)\"\]", error_string[0])
    return dict((x, [y]) for x, y in error_dict)
