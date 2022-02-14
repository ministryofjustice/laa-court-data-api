from typing import Optional

from pydantic import BaseModel


class RepresentationOrder(BaseModel):
    application_reference: Optional[str] = None
    effective_start_date: Optional[str] = None
    effective_end_date: Optional[str] = None
    laa_contract_number: Optional[str] = None
