from uuid import UUID

from pydantic import BaseModel

from laa_court_data_api_app.models.hearing.external.court_application import CourtApplication
from laa_court_data_api_app.models.hearing.external.court_centre import CourtCentre
from laa_court_data_api_app.models.hearing.external.cracked_ineffective_trial import CrackedIneffectiveTrial
from laa_court_data_api_app.models.hearing.external.defence_counsel import DefenceCounsel
from laa_court_data_api_app.models.hearing.external.defendant_attendance import DefendantAttendance
from laa_court_data_api_app.models.hearing.external.defendant_judicial_results import DefendantJudicialResults
from laa_court_data_api_app.models.hearing.external.hearing_day import HearingDay
from laa_court_data_api_app.models.hearing.external.hearing_type import HearingType
from laa_court_data_api_app.models.hearing.external.judiciary import Judiciary
from laa_court_data_api_app.models.hearing.external.prosecution_cases import ProsecutionCases
from laa_court_data_api_app.models.hearing.external.prosecution_counsel import ProsecutionCounsel


class Hearing(BaseModel):
    id: UUID | None
    jurisdiction_type: str | None
    court_centre: CourtCentre | None
    hearing_language: str | None
    has_shared_results: bool | None
    court_applications: list[CourtApplication] | None
    hearing_type: HearingType | None
    hearing_days: list[HearingDay] | None
    judiciary: list[Judiciary] | None
    prosecution_counsels: list[ProsecutionCounsel] | None
    defence_counsels: list[DefenceCounsel] | None
    cracked_ineffective_trial: CrackedIneffectiveTrial | None
    prosecution_cases: list[ProsecutionCases] | None
    defendant_judicial_results: list[DefendantJudicialResults] | None
    defendant_attendance: DefendantAttendance | None
