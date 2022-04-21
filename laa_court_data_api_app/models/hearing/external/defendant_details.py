from pydantic import BaseModel
from laa_court_data_api_app.models.hearing.external.bail_status import BailStatus
from laa_court_data_api_app.models.hearing.external.person_details import PersonDetails


class DefendantDetails(BaseModel):
    person_details: PersonDetails | None
    arrest_summons_number: str | None
    bail_conditions: str | None
    bail_status: BailStatus | None
    required: str | None
