from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class LaaApplication(BaseModel):
    reference: Optional[str] = None
    id: Optional[UUID] = None
    code: Optional[str] = None
    description: Optional[str] = None
    date: Optional[str] = None
    effective_start_date: Optional[str] = None
    effective_end_date: Optional[str] = None
    laa_contract_number: Optional[str] = None
