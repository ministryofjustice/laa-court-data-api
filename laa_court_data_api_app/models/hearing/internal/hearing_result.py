from pydantic import BaseModel

from laa_court_data_api_app.models.hearing.internal.hearing import Hearing


class HearingResult(BaseModel):
    hearing: Hearing | None
    shared_time: str | None
