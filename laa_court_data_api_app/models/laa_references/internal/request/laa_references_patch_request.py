from pydantic import BaseModel

from laa_court_data_api_app.models.laa_references.internal.request.laa_references_patch import LaaReferencesPatch


class LaaReferencesPatchRequest(BaseModel):
    laa_reference: LaaReferencesPatch | None
