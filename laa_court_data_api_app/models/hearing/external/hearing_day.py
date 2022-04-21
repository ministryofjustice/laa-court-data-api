from typing import Optional

from pydantic import BaseModel


class HearingDay(BaseModel):
    sitting_day: Optional[str] = None
    has_shared_results: Optional[bool] = None
