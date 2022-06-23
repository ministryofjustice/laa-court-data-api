from datetime import datetime

from pydantic import BaseModel


class HearingDay(BaseModel):
    sitting_day: datetime | None
    listing_sequence: int | None
    listed_duration_minutes: int | None
    has_shared_results: bool | None
