from typing import Optional
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from laa_court_data_api_app.models.hearing.judicial_result import JudicialResult
from laa_court_data_api_app.models.hearing.plea import Plea
from laa_court_data_api_app.models.hearing.respondent import Respondent
from laa_court_data_api_app.models.hearing.verdict import Verdict


class CourtApplication(BaseModel):
    id: Optional[UUID] = None
    received_date: Optional[str] = None
    application_reference: Optional[str] = None
    respondents: Optional[list[Respondent]] = None
    judicial_results: Optional[list[JudicialResult]] = None
    plea: Optional[Plea] = None
    verdict: Optional[Verdict] = None

