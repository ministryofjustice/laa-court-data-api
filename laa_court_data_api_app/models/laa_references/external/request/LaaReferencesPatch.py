from uuid import UUID

from pydantic import BaseModel


class LaaReferencesPatch(BaseModel):
    user_name: str | None
    defendant_id: UUID | None
    maat_reference: int | None
    unlink_reason_code: int | None
