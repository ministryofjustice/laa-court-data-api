from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from laa_court_data_api_app.models.hearing_summaries.hearing_summary import HearingSummary


class HearingSummariesResponse(BaseModel):
    hearing_summaries: Optional[list[HearingSummary]] = None