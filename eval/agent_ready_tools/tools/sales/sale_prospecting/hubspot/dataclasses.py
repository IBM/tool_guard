from enum import StrEnum
from typing import Any, Optional

from pydantic import ConfigDict, Field
from pydantic.dataclasses import dataclass


class HubspotDealType(StrEnum):
    """Possible Hubspot deal types."""

    NEW_BUSINESS = "newbusiness"
    EXISTING_BUSINESS = "existingbusiness"


def remove_underscores(input_string: str) -> str:
    """
    Remove underscores from the input string.

    Args:
        input_string: The string from which to remove underscores.

    Returns:
        The input string with underscores removed.
    """
    return input_string.replace("_", "")


@dataclass(config=ConfigDict(alias_generator=remove_underscores, extra="ignore"))
class HubspotDeal:
    """Dataclass for Hubspot deal."""

    deal_name: str
    deal_id: str = Field(alias="hs_object_id")
    deal_type: Optional[HubspotDealType] = Field(default=None)
    description: Optional[str] = Field(default=None)
    amount: Optional[float] = Field(default=None)
    pipeline: Optional[str] = Field(default=None)
    create_date: Optional[str] = Field(default=None)
    close_date: Optional[str] = Field(default=None)
    deal_stage: Optional[str] = Field(default=None)
    last_modified_date: Optional[str] = Field(alias="hs_lastmodifieddate", default=None)
    hubspot_owner_id: Optional[str] = Field(alias="hubspot_owner_id", default=None)


@dataclass(config=ConfigDict(alias_generator=remove_underscores, extra="ignore"))
class HubspotContact:
    """Represents a contact in HubSpot."""

    contact_id: str = Field(alias="hs_object_id")
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)
    company: Optional[str] = Field(default=None)
    job_title: Optional[str] = Field(default=None)
    lifecycle_stage: Optional[str] = Field(default=None)
    lead_status: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)
    state: Optional[str] = Field(default=None)
    country: Optional[str] = Field(default=None)
    zip: Optional[str] = Field(default=None)
    industry: Optional[str] = Field(default=None)


@dataclass
class HubspotErrorResponse:
    """Error response from Hubspot API."""

    message: Any
