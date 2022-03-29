from uuid import UUID

from pydantic import BaseModel


class LaaReferencesPatchRequest(BaseModel):
    user_name: str | None
    defendant_id: UUID | None
    maat_reference: int | None
    unlink_reason_code: int | None
    unlink_other_reason_text: str | None

    class Config:
        schema_extra = {
            "example": {
                "user_name": "jon-5",
                "defendant_id": "d7f509e8-309c-4262-a41d-ebbb44deab9e",
                "maat_reference": 3141592,
                "unlink_reason_code": 1,
                "unlink_other_reason_text": "Linked to incorrect case"
            }
        }
