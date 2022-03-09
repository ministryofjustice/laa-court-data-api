from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Plea(BaseModel):
    date: Optional[str] = None
    value: Optional[str] = None
    originating_hearing_id: Optional[UUID] = None
