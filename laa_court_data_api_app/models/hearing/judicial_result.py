from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from laa_court_data_api_app.models.hearing.prompt import Prompt


class JudicialResult(BaseModel):
    id: Optional[UUID] = None
    label: Optional[str] = None
    text: Optional[str] = None
    cjs_code: Optional[str] = None
    ordered_date: Optional[str] = None
    prompts: Optional[list[Prompt]] = None
    post_hearing_custody_status: Optional[str] = None
    wording: Optional[str] = None
