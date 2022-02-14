from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from laa_court_data_api_app.models.prosecution_cases.laa_application import LaaApplication


class OffenceSummary(BaseModel):
    id: Optional[UUID] = None
    code: Optional[str] = None
    order_index: Optional[int] = None
    title: Optional[str] = None
    legislation: Optional[str] = None
    wording: Optional[str] = None
    arrest_date: Optional[str] = None
    charge_date: Optional[str] = None
    mode_of_trial: Optional[str] = None
    start_date: Optional[str] = None
    proceedings_concluded: Optional[bool] = None
    laa_application: Optional[LaaApplication] = None
