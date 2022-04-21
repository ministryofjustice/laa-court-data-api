from uuid import UUID

from pydantic import BaseModel

from laa_court_data_api_app.models.prosecution_cases.plea import Plea
from laa_court_data_api_app.models.prosecution_cases.verdict import Verdict
from laa_court_data_api_app.models.prosecution_cases.laa_application import LaaApplication


class OffenceSummary(BaseModel):
    id: UUID | None
    code: str | None
    order_index: int | None
    title: str | None
    legislation: str | None
    wording: str | None
    arrest_date: str | None
    charge_date: str | None
    mode_of_trial: str | None
    start_date: str | None
    proceedings_concluded: bool | None
    plea: Plea | None
    verdict: Verdict | None
    laa_application: LaaApplication | None
