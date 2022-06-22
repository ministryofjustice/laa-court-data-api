from pydantic import BaseModel
from laa_court_data_api_app.models.case_summaries.defendants import Defendants
from laa_court_data_api_app.models.case_summaries.hearing_summary import HearingSummary


class CaseSummariesResponse(BaseModel):
    prosecution_case_reference: str | None
    hearing_summaries: list[HearingSummary] | None
    overall_defendants: list[Defendants]
