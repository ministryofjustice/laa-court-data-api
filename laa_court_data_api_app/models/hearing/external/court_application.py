from typing import Optional
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from laa_court_data_api_app.models.hearing.external.court_application_type import CourtApplicationType

from laa_court_data_api_app.models.hearing.external.judicial_result import JudicialResult
from laa_court_data_api_app.models.hearing.external.plea import Plea
from laa_court_data_api_app.models.hearing.external.respondent import Respondent
from laa_court_data_api_app.models.hearing.external.verdict import Verdict


class CourtApplication(BaseModel):
    id: UUID | None
    received_date: str | None
    application_reference: str | None
    respondents: list[Respondent] | None
    judicial_results: list[JudicialResult] | None
    plea: Plea | None
    verdict: Verdict | None
    type: CourtApplicationType | None
