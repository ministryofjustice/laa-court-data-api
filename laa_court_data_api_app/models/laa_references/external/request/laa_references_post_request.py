from pydantic import BaseModel

from laa_court_data_api_app.models.laa_references.external.request.laa_references_post import LaaReferencesPost


class LaaReferencesPostRequest(BaseModel):
    laa_reference: LaaReferencesPost | None
