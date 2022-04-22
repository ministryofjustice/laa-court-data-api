from pydantic import BaseModel


class Contact(BaseModel):
    home: str | None
    work: str | None
    mobile: str | None
    email_primary: str | None
    email_secondary: str | None
    fax: str | None
