from uuid import UUID
from pydantic import BaseModel

from laa_court_data_api_app.models.hearing.internal.judicial_result import JudicialResult


class DefendantJudicialResults(BaseModel):
    master_defendant_id: UUID | None
    judicialResult: JudicialResult | None
