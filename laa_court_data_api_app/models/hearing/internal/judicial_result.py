from uuid import UUID

from pydantic import BaseModel

from laa_court_data_api_app.models.hearing.internal.prompt import Prompt


class JudicialResult(BaseModel):
    id: UUID | None
    label: str | None
    is_adjournment_result: bool | None
    is_financial_result: bool | None
    is_convicted_result: bool | None
    is_available_for_court_extract: bool | None
    qualifier: str | None
    text: str | None
    cjs_code: str | None
    ordered_date: str | None
    prompts: list[Prompt] | None
    post_hearing_custody_status: str | None
    wording: str | None
