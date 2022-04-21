from typing import Optional

from pydantic import BaseModel


class Judiciary(BaseModel):
    title: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    type: Optional[str] = None
    is_deputy: Optional[str] = None
    is_bench_chairman: Optional[str] = None
