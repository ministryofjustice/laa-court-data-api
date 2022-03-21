from uuid import UUID

from pydantic import BaseModel


class LaaReferencesPatch(BaseModel):
    user_name: str | None
    defendant_id: UUID | None
    maat_reference: int | None
    unlink_reason_code: int | None

    class Config:
        schema_extra = {
            "example": {
                "user_name": "jon-5",
                "defendant_id": "d7f509e8-309c-4262-a41d-ebbb44deab9e",
                "maat_reference": 1234567,
                "unlink_reason_code": 0
            }
        }
