from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from laa_court_data_api_app.models.hearing.external.delegated_powers import DelegatedPowers


class Plea(BaseModel):
    date: str | None
    value: str | None
    originating_hearing_id: UUID | None
    offence_id: UUID | None
    application_id: UUID | None
    delegated_powers: DelegatedPowers | None
