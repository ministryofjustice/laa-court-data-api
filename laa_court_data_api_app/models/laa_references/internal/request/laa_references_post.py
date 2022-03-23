from uuid import UUID

from pydantic import BaseModel


class LaaReferencesPost(BaseModel):
    user_name: str | None
    defendant_id: UUID | None
    maat_reference: int | None
