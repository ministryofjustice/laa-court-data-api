from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Prompt(BaseModel):
    type_id: Optional[UUID] = None
    label: Optional[str] = None
    is_available_for_court_extract: Optional[bool] = None
    value: Optional[str] = None
    qualifier: Optional[str] = None
    duration_sequence: Optional[int] = None
    prompt_sequence: Optional[int] = None
    total_penalty_points: Optional[int] = None
    # is_financial_imposition
    # usergroups: Optional[list[str]] = None
