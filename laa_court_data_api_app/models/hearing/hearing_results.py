from typing import Optional
from datetime import datetime

from pydantic import BaseModel

from laa_court_data_api_app.models.hearing.hearing import Hearing


class HearingResult(BaseModel):
    hearing: Optional[Hearing] = None
    shared_time: Optional[datetime] = None
