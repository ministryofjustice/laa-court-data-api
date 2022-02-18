from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class HearingDay(BaseModel):
    sitting_day: Optional[datetime] = None
    listing_sequence: Optional[int] = None
    listed_duration_minutes: Optional[int] = None
    has_shared_results: Optional[bool] = None
