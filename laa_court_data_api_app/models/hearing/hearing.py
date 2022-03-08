from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from laa_court_data_api_app.models.hearing.court_application import CourtApplication
from laa_court_data_api_app.models.hearing.court_centre import CourtCentre
from laa_court_data_api_app.models.hearing.cracked_ineffective_trial import CrackedIneffectiveTrial
from laa_court_data_api_app.models.hearing.defence_counsel import DefenceCounsel
from laa_court_data_api_app.models.hearing.hearing_day import HearingDay
from laa_court_data_api_app.models.hearing.hearing_type import HearingType
from laa_court_data_api_app.models.hearing.judiciary import Judiciary
from laa_court_data_api_app.models.hearing.prosecution_counsel import ProsecutionCounsel


class Hearing(BaseModel):
    id: Optional[UUID] = None
    jurisdiction_type: Optional[str] = None
    court_centre: Optional[CourtCentre] = None
    language: Optional[str] = None
    # prosecution_cases:
    # defendant_judicial_results:
    has_shared_results: Optional[bool] = None
    court_applications: Optional[list[CourtApplication]] = None
    type: Optional[HearingType] = None
    hearing_days: Optional[list[HearingDay]] = None
    judiciary: Optional[list[Judiciary]] = None
    prosecution_counsels: Optional[list[ProsecutionCounsel]] = None
    defence_counsels: Optional[list[DefenceCounsel]] = None
    cracked_ineffective_trial: Optional[CrackedIneffectiveTrial] = None
