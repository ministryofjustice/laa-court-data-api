from uuid import UUID
from pydantic import BaseModel


class Defendants(BaseModel):
    id: UUID | None
    first_name: str | None
    middle_name: str | None
    last_name: str | None
    arrest_summons_number: str | None
    date_of_birth: str | None
    national_insurance_number: str | None
