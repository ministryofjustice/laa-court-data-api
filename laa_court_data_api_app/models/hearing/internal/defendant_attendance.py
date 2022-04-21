from uuid import UUID
from pydantic import BaseModel

from laa_court_data_api_app.models.hearing.internal.attendance_days import AttendanceDays


class DefendantAttendance(BaseModel):
    defendant_id: UUID | None
    attendance_days: list[AttendanceDays] | None