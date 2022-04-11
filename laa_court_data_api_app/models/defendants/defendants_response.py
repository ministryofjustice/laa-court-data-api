from typing import Optional
from pydantic import BaseModel

from laa_court_data_api_app.models.defendants.defendant_summary import DefendantSummary


class DefendantsResponse(BaseModel):
    defendant_summaries: Optional[list[DefendantSummary]] = None
