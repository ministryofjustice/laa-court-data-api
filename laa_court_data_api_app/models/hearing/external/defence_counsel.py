from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class DefenceCounsel(BaseModel):
    title: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    status: Optional[str] = None
    attendance_days: Optional[list[str]] = None
    defendants: Optional[list[UUID]] = None
