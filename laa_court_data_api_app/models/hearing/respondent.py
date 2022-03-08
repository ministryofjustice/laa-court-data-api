from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Respondent(BaseModel):
    id: Optional[UUID] = None
    synonym: Optional[str] = None
    summons_required: Optional[bool] = None
    notification_required: Optional[bool] = None
