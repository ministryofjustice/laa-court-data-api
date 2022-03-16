from pydantic import BaseModel


class LaaReferencesErrorResponse(BaseModel):
    error: str | None
