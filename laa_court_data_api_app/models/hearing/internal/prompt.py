from uuid import UUID

from pydantic import BaseModel


class Prompt(BaseModel):
    type_id: UUID | None
    label: str | None
    welsh_label: str | None
    is_available_for_court_extract: bool | None
    value: str | None
    welsh_value: str | None
    qualifier: str | None
    duration_sequence: int | None
    prompt_sequence: int | None
    prompt_reference: str | None
    total_penalty_points: int | None
    is_financial_imposition: bool | None
    usergroups: list[str] | None
