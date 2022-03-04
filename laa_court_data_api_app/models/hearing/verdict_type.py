from typing import Optional

from pydantic import BaseModel


class VerdictType(BaseModel):
    id: Optional[UUID] = None
    category: Optional[str] = None
    category_type: Optional[str] = None
    cjs_verdict_code: Optional[str] = None
    description: Optional[str] = None
    sequence: Optional[int] = None
    verdict_code: Optional[str] = None
