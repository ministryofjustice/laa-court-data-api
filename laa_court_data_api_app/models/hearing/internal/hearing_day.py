from pydantic import BaseModel


class HearingDay(BaseModel):
    sitting_day: str | None
    has_shared_results: bool | None
