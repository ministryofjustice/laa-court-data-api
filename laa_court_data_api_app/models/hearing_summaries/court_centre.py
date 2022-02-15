from uuid import UUID

from pydantic import BaseModel
from typing import Optional


class CourtCentre(BaseModel):
    id: Optional[UUID] = None
    name: Optional[str] = None
    room_id: Optional[str] = None
    room_name: Optional[str] = None
    short_oucode: Optional[str] = None
    oucode_l2_code: Optional[str] = None
    code: Optional[str] = None
