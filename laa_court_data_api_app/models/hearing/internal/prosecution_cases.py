from pydantic import BaseModel
from laa_court_data_api_app.models.hearing.internal.defendants import Defendants

from laa_court_data_api_app.models.hearing.internal.prosecution_case_identifier import ProsecutionCaseIdentifier


class ProsecutionCases(BaseModel):
    id: str | None
    prosecution_case_identifier: ProsecutionCaseIdentifier | None
    status: str | None
    statement_of_facts: str | None
    statement_of_facts_welsh: str | None
    defendants: list[Defendants] | None
    
