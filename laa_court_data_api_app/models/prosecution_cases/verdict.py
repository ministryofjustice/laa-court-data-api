from uuid import UUID

from pydantic import BaseModel

from laa_court_data_api_app.models.hearing.verdict_type import VerdictType


class Verdict(BaseModel):
    date: str | None
    type: VerdictType | None
    originating_hearing_id: UUID | None
    offence_id: UUID | None
