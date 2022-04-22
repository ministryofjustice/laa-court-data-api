from uuid import UUID
from pydantic import BaseModel


class LaaApplication(BaseModel):
    reference: str | None
    id: UUID | None
    status_code: str | None
    description: str | None
    status_date: str | None
    effective_start_date: str | None
    effective_end_date: str | None
    laa_contract_number: str | None
