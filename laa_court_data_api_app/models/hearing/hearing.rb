from typing import Optional

from pydantic import BaseModel


class Hearing(BaseModel):
  id: Optional[UUID] = None
  jurisdiction_type: Optional[str] = None
  court_centre: Optional[CourtCentre] = None
  hearing_language: Optional[str] = None
  prosecution_cases: list[ProsecutionCase]
  defendant_judicial_results: list[
end
