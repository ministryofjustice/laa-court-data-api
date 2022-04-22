from pydantic import BaseModel


class Judiciary(BaseModel):
    title: str | None
    first_name: str | None
    middle_name: str | None
    last_name: str | None
    type: str | None
    is_deputy: str | None
    is_bench_chairman: str | None
