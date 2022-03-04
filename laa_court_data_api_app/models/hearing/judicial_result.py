from typing import Optional
from uuid import UUID

from pydantic import BaseModel

class JudicialResult(BaseModel):
    id: Optional[UUID] = None
    label: Optional[str] = None
    text: Optional[str] = None
    cjs_code: Optional[str] = None
    ordered_date: Optional[datetime] = None
    prompts: Optional[list[Prompt]] = None


