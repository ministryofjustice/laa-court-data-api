from uuid import UUID
from pydantic import BaseModel


class CourtIndicatedSentence(BaseModel):
    type_id: UUID | None
    description: str | None
