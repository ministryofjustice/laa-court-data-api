from uuid import UUID

from pydantic import BaseModel

from laa_court_data_api_app.models.defendants.laa_application import LaaApplication
from laa_court_data_api_app.models.defendants.plea import Plea
from laa_court_data_api_app.models.defendants.verdict import Verdict


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
    pleas: list[Plea] | None
    verdict: Verdict | None
    laa_application: LaaApplication | None
