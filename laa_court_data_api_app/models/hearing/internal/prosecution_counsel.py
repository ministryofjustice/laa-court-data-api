from uuid import UUID

from pydantic import BaseModel


class ProsecutionCounsel(BaseModel):
    title: str | None
    first_name: str | None
    middle_name: str | None
    last_name: str | None
    status: str | None
    prosecution_cases: list[UUID] | None
    attendance_days: list[str] | None
