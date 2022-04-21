from uuid import UUID

from pydantic import BaseModel


class Respondent(BaseModel):
    id: UUID | None
    synonym: str | None
    summons_required: bool | None
    notification_required: bool | None
