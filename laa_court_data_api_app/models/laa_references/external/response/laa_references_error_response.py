from pydantic import BaseModel, Field


class LaaReferencesErrorResponse(BaseModel):
    errors: dict[str, object] | None = Field(None, alias="error")
