from typing import Optional
from pydantic import BaseModel, Field


class Ping(BaseModel):
    app_branch: Optional[str] = Field(None, example='test_branch')
    build_date: Optional[str] = Field(None, example='02022022')
    build_tag: Optional[str] = Field(None, example='test')
    commit_id: Optional[str] = Field(None, example='123456')
