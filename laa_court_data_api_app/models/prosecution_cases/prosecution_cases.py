from typing import Optional

from pydantic import Field, BaseModel

from laa_court_data_api_app.models.prosecution_cases.defendant_summary import DefendantSummary
from laa_court_data_api_app.models.prosecution_cases.hearing_summary import HearingSummary


class ProsecutionCases(BaseModel):
    prosecution_case_reference: Optional[str] = None
    prosecution_case_status: Optional[str] = Field(None, alias="case_status")
    defendant_summaries: Optional[list[DefendantSummary]] = None
    hearing_summaries: Optional[list[HearingSummary]] = None
