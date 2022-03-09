from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CrackedIneffectiveTrial(BaseModel):
    id: Optional[UUID] = None
    code: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    date: Optional[str] = None
