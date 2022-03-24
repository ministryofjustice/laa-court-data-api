from uuid import UUID

from pydantic import BaseModel


class VerdictType(BaseModel):
    id: UUID | None
    category: str | None
    category_type: str | None
    cjs_verdict_code: str | None
    description: str | None
    sequence: int | None
    verdict_code: str | None
