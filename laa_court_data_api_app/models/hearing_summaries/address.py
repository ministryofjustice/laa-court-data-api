from pydantic import BaseModel


class Address(BaseModel):
    address_1: str | None
    address_2: str | None
    address_3: str | None
    address_4: str | None
    address_5: str | None
    postcode: str | None