from typing import Optional
from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[float] = None
    created_at: Optional[float] = None
