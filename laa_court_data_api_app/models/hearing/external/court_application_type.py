from uuid import UUID
from pydantic import BaseModel


class CourtApplicationType(BaseModel):
    id: UUID | None
    code: str | None
    description: str | None
    legislation: str | None
    category_code: str | None
    link_type: str | None
    jurisdiction: str | None
    appeal_flag: bool | None
    summons_template_type: str | None
    valid_from: str | None
    valid_to: str | None
    applicant_appellant_flag: bool | None
    plea_applicable_flag: bool | None
    offence_active_order: str | None
    commr_of_oath_flag: bool | None
    breach_type: str | None
    court_of_appeal_flag: bool | None
    court_extract_avl_flag: bool | None
    listing_notif_template: str | None
    boxwork_notif_template: str | None
    type_welsh: str | None
    legislation_welsh: str | None
    prosecutor_third_party_flag: bool | None
    spi_out_applicable_flag: bool | None
    hearing_code: str | None
