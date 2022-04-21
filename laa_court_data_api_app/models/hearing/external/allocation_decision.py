from uuid import UUID
from pydantic import BaseModel

from laa_court_data_api_app.models.hearing.external.court_indicated_sentence import CourtIndicatedSentence


class AllocationDecision(BaseModel):
    date: str | None
    originating_hearing_id: UUID | None
    offence_id: UUID | None
    mot_reason_id: UUID | None
    mot_reason_description: str | None
    mot_reason_code: str | None
    court_indicated_sentence: CourtIndicatedSentence | None
    sequence_number: int | None
