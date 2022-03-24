from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class DefenceCounsel(BaseModel):
    title: str | None
    first_name: str | None
    middle_name: str | None
    last_name: str | None
    status: str | None
    attendance_days: list[datetime] | None
    defendants: list[UUID] | None
