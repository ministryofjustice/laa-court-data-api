from typing import Optional
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Plea(BaseModel):
    date: Optional[datetime] = None
    value: Optional[str] = None
    originating_hearing_id: Optional[UUID] = None
