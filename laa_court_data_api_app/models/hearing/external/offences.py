from uuid import UUID
from pydantic import BaseModel
from laa_court_data_api_app.models.hearing.external.allocation_decision import AllocationDecision
from laa_court_data_api_app.models.hearing.external.judicial_result import JudicialResult
from laa_court_data_api_app.models.hearing.external.laa_application import LaaApplication

from laa_court_data_api_app.models.hearing.external.plea import Plea
from laa_court_data_api_app.models.hearing.external.verdict import Verdict


class Offences(BaseModel):
    id: UUID | None
    code: str | None
    title: str | None
    legislation: str | None
    mode_of_trial: str | None
    wording: str | None
    start_date: str | None
    order_index: int | None
    allocation_decision: AllocationDecision | None
    plea: Plea | None
    verdict: Verdict | None
    judicial_results: list[JudicialResult] | None
    laa_application: LaaApplication | None
    proceedings_concluded: bool | None
