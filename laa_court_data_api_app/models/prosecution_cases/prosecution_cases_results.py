from pydantic import BaseModel

from laa_court_data_api_app.models.prosecution_cases.prosecution_cases import ProsecutionCases


class ProsecutionCasesResults(BaseModel):
    total_results: int
    results: list[ProsecutionCases]
