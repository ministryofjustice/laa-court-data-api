from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from laa_court_data_api_app.models.prosecution_cases.court_centre import CourtCentre
from laa_court_data_api_app.models.prosecution_cases.defence_counsel import DefenceCounsel
from laa_court_data_api_app.models.prosecution_cases.hearing_day import HearingDay


class HearingSummary(BaseModel):
    id: Optional[UUID] = None
    hearing_type: Optional[str] = None
    estimated_duration: Optional[str] = None
    court_centre: Optional[CourtCentre] = None
    hearing_days: Optional[list[HearingDay]] = None
    defence_counsels: Optional[list[DefenceCounsel]] = None
