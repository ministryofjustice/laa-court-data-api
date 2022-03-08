from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class HearingEvent(BaseModel):
    id: Optional[UUID] = None
    definition_id: Optional[UUID] = None
    defence_counsel_id: Optional[UUID] = None
    recorded_label: Optional[str] = None
    event_time: Optional[datetime] = None
    last_modified_time: Optional[datetime] = None
    alterable: Optional[bool] = None
    note: Optional[str] = None