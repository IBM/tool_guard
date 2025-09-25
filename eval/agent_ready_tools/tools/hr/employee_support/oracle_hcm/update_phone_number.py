from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class UpdatePhoneNumberResult:
    """Represents the result of phone update operation in Oracle HCM."""

    phone_number: str
    phone_id: Optional[int]
    phone_type: str
    country_code: str
    response_code: Optional[int]
    area_code: Optional[str] = None
    message: Optional[str] = None


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def update_phone_number(
    worker_id: str,
    phone_id: int,
    area_code: str,
    phone_number: str,
    phone_type: str,
    country_code: str,
    legislation_code: str,
) -> UpdatePhoneNumberResult:
    """
    Updates a user's phone number in Oracle HCM.

    Args:
        worker_id: The user's worker_id uniquely identifying them within the Oracle HCM API. Worker
            ID can be directly provided by the user or obtained by the get_user_oracle_ids tool.
        phone_id: The user's phone_id uniquely identifying the given phone number within the the
            Oracle HCM API, obtained by calling the `get_phones_ids` tool"
        area_code: Given a user's full phone number, the area code is the initial part (typically
            2-4 digits) that identifies a geographic region or network.
        phone_number: The phone number is the remaining part of the user's number after the area
            code.
        phone_type: The phone type corresponding to the phone with id matching the phone_id, it has
            to be one of the types returned by the get_phone_types.
        country_code: The country_code refers to the international dialing prefix used to reach a
            phone number from abroad. It is a numeric code that identifies the country or region.
        legislation_code: The legislation code used to define country-specific rules and formatting
            for a phone number. It's standard ISO 2-letter codes representing a country, e.g. "US".

    Returns:
        The user's phone item.
    """
    client = get_oracle_hcm_client()

    payload = {
        "PhoneNumber": phone_number,
        "PhoneType": phone_type,
        "AreaCode": area_code,
        "CountryCodeNumber": country_code,
    }

    if legislation_code:
        payload["LegislationCode"] = legislation_code

    entity = f"workers/{worker_id}/child/phones/{phone_id}"
    response = client.update_request(payload=payload, entity=entity)
    return UpdatePhoneNumberResult(
        phone_number=response.get("PhoneNumber", ""),
        area_code=response.get("AreaCode", ""),
        phone_id=response.get("PhoneId", None),
        phone_type=response.get("PhoneType", ""),
        country_code=response.get("CountryCodeNumber", ""),
        message=response.get("message", ""),
        response_code=response.get("status_code", None),
    )
