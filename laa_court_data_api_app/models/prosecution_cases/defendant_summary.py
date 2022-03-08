from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from laa_court_data_api_app.models.prosecution_cases.offence_summary import OffenceSummary
from laa_court_data_api_app.models.prosecution_cases.representation_order import RepresentationOrder


class DefendantSummary(BaseModel):
    id: Optional[UUID] = None
    national_insurance_number: Optional[str] = None
    arrest_summons_number: Optional[str] = None
    name: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    proceedings_concluded: Optional[bool] = None
    representation_order: Optional[RepresentationOrder] = None
    offence_summaries: Optional[list[OffenceSummary]] = None
