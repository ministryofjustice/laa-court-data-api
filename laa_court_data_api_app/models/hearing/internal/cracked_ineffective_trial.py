from uuid import UUID

from pydantic import BaseModel


class CrackedIneffectiveTrial(BaseModel):
    id: UUID | None
    code: str | None
    description: str | None
    type: str | None
    date: str | None
