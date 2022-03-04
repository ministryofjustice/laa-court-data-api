from typing import Optional
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CourtApplication(BaseModel):
    id: Optional[UUID] = None
    received_date: Optional[datetime] = None
    application_reference: Optional[str] = None
    respondents: Optional[list[Respondent]] = None
    judicial_results: Optional[list[JudicialResult]] = None
    plea: Optional[Plea] = None
    verdict: Optional[Verdict] = None

