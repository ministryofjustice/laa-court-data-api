from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class LaaReferencesPatch(BaseModel):
    user_name: Optional[str] = None
    defendant_id: Optional[UUID] = None
    maat_reference: Optional[int] = None
    unlink_reason_code: Optional[int] = None
