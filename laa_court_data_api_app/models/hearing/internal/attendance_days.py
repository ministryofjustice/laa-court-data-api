from pydantic import BaseModel


class AttendanceDays(BaseModel):
    day: str | None
    attendance_type: str | None
