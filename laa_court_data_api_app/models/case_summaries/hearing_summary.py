from uuid import UUID

from pydantic import BaseModel

from laa_court_data_api_app.models.case_summaries.court_centre import CourtCentre
from laa_court_data_api_app.models.case_summaries.defence_counsel import DefenceCounsel
from laa_court_data_api_app.models.case_summaries.defendants import Defendants
from laa_court_data_api_app.models.case_summaries.hearing_day import HearingDay


class HearingSummary(BaseModel):
    id: UUID | None
    hearing_type: str | None
    estimated_duration: str | None
    defendants: list[Defendants] | None = []
    jurisdiction_type: str | None
    court_centre: CourtCentre | None
    hearing_days: list[HearingDay] | None
    defence_counsels: list[DefenceCounsel] | None
