from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel

from laa_court_data_api_app.models.hearing_events.hearing_event.response.hearing_event import HearingEvent


class HearingEventsResponse(BaseModel):
    hearing_id: Optional[UUID] = None
    has_active_hearing: Optional[bool] = None
    events: Optional[List[HearingEvent]] = None
