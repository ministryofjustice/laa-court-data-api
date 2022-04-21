from pydantic import BaseModel
from laa_court_data_api_app.models.hearing.internal.bail_status import BailStatus
from laa_court_data_api_app.models.hearing.internal.person_details import PersonDetails


class DefendantDetails(BaseModel):
    person_details: PersonDetails | None
    arrest_summons_number: str | None
    bail_conditions: str | None
    bail_status: BailStatus | None
    required: str | None
