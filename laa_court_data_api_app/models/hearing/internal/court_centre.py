from uuid import UUID

from pydantic import BaseModel

from laa_court_data_api_app.models.hearing.internal.address import Address


class CourtCentre(BaseModel):
    id: UUID | None
    name: str | None
    welsh_name: str | None
    room_id: str | None
    room_name: str | None
    welsh_room_name: str | None
    welsh_court_centre: str | None
    short_oucode: str | None
    oucode_l2_code: str | None
    code: str | None
    address: Address | None
