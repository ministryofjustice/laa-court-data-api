from uuid import UUID

from pydantic import BaseModel

from laa_court_data_api_app.models.prosecution_cases.court_centre import CourtCentre
from laa_court_data_api_app.models.prosecution_cases.defence_counsel import DefenceCounsel
from laa_court_data_api_app.models.prosecution_cases.hearing_day import HearingDay


class HearingSummary(BaseModel):
    id: UUID | None
    hearing_type: str | None
    estimated_duration: str | None
    defendant_ids: list[str] | None = []
    jurisdiction_type: str | None
    court_centre: CourtCentre | None
    hearing_days: list[HearingDay] | None
    defence_counsels: list[DefenceCounsel] | None
