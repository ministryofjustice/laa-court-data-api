from uuid import UUID
from pydantic import BaseModel


class ApplicationSummary(BaseModel):
    id: UUID | None
    short_id: str | None
    reference: str | None
    title: str | None
    received_date: str | None
