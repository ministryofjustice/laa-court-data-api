from pydantic import BaseModel


class PersonDetails(BaseModel):
    title: str | None
    first_name: str | None
    middle_name: str | None
    last_name: str | None
    date_of_birth: str | None
    gender: str | None
    documentation_language_needs: str | None
    nino: str | None
    occupation: str | None
    occupation_code: str | None