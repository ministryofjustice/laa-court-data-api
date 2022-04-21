from pydantic import BaseModel

from laa_court_data_api_app.models.hearing.external.address import Address
from laa_court_data_api_app.models.hearing.external.contact import Contact


class Organisation(BaseModel):
    name: str | None
    incorporation_number: str | None
    registered_charity_number: str | None
    address: Address | None
    contact: Contact | None