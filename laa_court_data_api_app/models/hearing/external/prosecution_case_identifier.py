from pydantic import BaseModel

from laa_court_data_api_app.models.hearing.external.contact import Contact


class ProsecutionCaseIdentifier(BaseModel):
    case_urn: str | None
    prosecution_authority_id: str | None
    prosecution_authority_code: str | None
    prosecution_authority_name: str | None
    contact: Contact | None
