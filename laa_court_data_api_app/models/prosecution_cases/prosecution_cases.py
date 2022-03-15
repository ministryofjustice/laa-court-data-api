from pydantic import Field, BaseModel

from laa_court_data_api_app.models.prosecution_cases.defendant_summary import DefendantSummary
from laa_court_data_api_app.models.prosecution_cases.hearing_summary import HearingSummary


class ProsecutionCases(BaseModel):
    prosecution_case_reference: str | None = None
    prosecution_case_status: str | None = Field(None, alias="case_status")
    defendant_summaries: list[DefendantSummary] | None = None
    hearing_summaries: list[HearingSummary] | None = None
