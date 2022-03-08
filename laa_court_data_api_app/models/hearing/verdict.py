from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from laa_court_data_api_app.models.hearing.verdict_type import VerdictType


class Verdict(BaseModel):
    date: Optional[datetime] = None
    type: Optional[VerdictType] = None
    originating_hearing_id: Optional[UUID] = None
    offence_id: Optional[UUID] = None
