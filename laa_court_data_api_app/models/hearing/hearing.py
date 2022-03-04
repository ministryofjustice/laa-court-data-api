from typing import Optional

from pydantic import BaseModel


class Hearing(BaseModel):
  id: Optional[UUID] = None
  jurisdiction_type: Optional[str] = None
  court_centre: Optional[CourtCentre] = None
  language: Optional[str] = None
  # prosecution_cases:
  # defendant_judicial_results:
  has_shared_results: Optional[bool] = None
  court_applications: Optional[list[CourtApplication]] = None
  type: Optional[Type] = None
  hearing_days: Optional[list[HearingDay]] = None
  judiciary: Optional[list[Judiciary]] = None
  prosecution_counsels: Optional[list[ProsecutionCounsel]] = None
  defence_counsels: Optional[list[DefenceCounsel]] = None
  cracked_ineffective_trial: Optional[list[CrackedIneffectiveTrial]] = None

