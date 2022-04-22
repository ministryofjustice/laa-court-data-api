from uuid import UUID
from pydantic import BaseModel


class DelegatedPowers(BaseModel):
    user_id: UUID | None
    first_name: str | None
    last_name: str | None
