from pydantic import BaseModel


class RepresentationOrder(BaseModel):
    application_reference: str | None = None
    effective_start_date: str | None = None
    effective_end_date: str | None = None
    laa_contract_number: str | None = None
