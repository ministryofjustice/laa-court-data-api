from pydantic import BaseModel


class RepresentationOrder(BaseModel):
    laa_application_reference: str | None
    effective_start_date: str | None
    effective_end_date: str | None
    laa_contract_number: str | None
