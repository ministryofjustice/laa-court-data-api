from uuid import UUID

from pydantic import BaseModel

from laa_court_data_api_app.models.prosecution_cases.offence_summary import OffenceSummary
from laa_court_data_api_app.models.prosecution_cases.representation_order import RepresentationOrder


class DefendantSummary(BaseModel):
    id: UUID | None
    national_insurance_number: str | None
    arrest_summons_number: str | None
    name: str | None
    first_name: str | None
    middle_name: str | None
    last_name: str | None
    date_of_birth: str | None
    proceedings_concluded: bool | None
    representation_order: RepresentationOrder | None
    offence_summaries: list[OffenceSummary] | None
