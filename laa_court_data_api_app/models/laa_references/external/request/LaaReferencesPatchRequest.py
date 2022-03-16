from typing import Optional

from pydantic import BaseModel

from laa_court_data_api_app.models.laa_references.external.request.LaaReferencesPatch import LaaReferencesPatch


class LaaReferencesPatchRequest(BaseModel):
    laa_reference: LaaReferencesPatch | None
