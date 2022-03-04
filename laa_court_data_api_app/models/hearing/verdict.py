from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Verdict(BaseModel):
    date: Optional[datetime] = None
    type: Optional[VerdictType] = None
    originating_hearing_id: Optional[UUID] = None
    offence_id: Optional[UUID] = None
