from uuid import UUID
from pydantic import BaseModel
from laa_court_data_api_app.models.hearing.external.defence_organisation import DefenceOrganisation
from laa_court_data_api_app.models.hearing.external.defendant_details import DefendantDetails

from laa_court_data_api_app.models.hearing.external.judicial_result import JudicialResult
from laa_court_data_api_app.models.hearing.external.offences import Offences


class Defendants(BaseModel):
    id: UUID | None
    prosecution_case_id: UUID | None
    offences: list[Offences] | None
    defence_organisation: DefenceOrganisation | None
    defendant_details: DefendantDetails | None
    judicial_results: list[JudicialResult] | None
    legal_aid_status: str | None
    proceedings_concluded: bool | None
    isYouth: bool | None
