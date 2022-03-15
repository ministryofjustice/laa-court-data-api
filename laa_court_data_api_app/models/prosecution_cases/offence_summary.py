from uuid import UUID

from pydantic import BaseModel

from laa_court_data_api_app.models.prosecution_cases.laa_application import LaaApplication


class OffenceSummary(BaseModel):
    id: UUID | None = None
    code: str | None = None
    order_index: int | None = None
    title: str | None = None
    legislation: str | None= None
    wording: str | None = None
    arrest_date: str | None = None
    charge_date: str | None = None
    mode_of_trial: str | None = None
    start_date: str | None = None
    proceedings_concluded: bool | None = None
    laa_application: LaaApplication | None = None
