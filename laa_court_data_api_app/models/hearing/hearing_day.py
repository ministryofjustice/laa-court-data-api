from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class HearingDay(BaseModel):
    sitting_day: Optional[datetime] = None
    has_shared_results: Optional[bool] = None
