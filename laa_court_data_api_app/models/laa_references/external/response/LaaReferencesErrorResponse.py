from typing import Optional

from pydantic import BaseModel


class LaaReferencesErrorResponse(BaseModel):
    error: Optional[str] = None
