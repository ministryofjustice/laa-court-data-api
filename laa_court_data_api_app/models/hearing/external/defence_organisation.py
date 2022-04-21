from pydantic import BaseModel

from laa_court_data_api_app.models.hearing.external.organisation import Organisation


class DefenceOrganisation(BaseModel):
    organisation: Organisation | None
    laa_contract_number: str | None
