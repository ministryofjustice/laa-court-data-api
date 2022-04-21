from pydantic import BaseModel


class BailStatus(BaseModel):
    code: str | None
    description: str | None
