from uuid import UUID

from pydantic import BaseModel


class HearingType(BaseModel):
    id: UUID | None
    description: str | None
    welsh_description: str | None
