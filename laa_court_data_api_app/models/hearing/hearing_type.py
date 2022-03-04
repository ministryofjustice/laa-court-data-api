from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class HearingType(BaseModel):
    id: Optional[UUID] = None
    description: Optional[str] = None

