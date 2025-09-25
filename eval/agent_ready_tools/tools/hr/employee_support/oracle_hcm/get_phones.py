from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class UserPhone:
    """Represents a phone number in Oracle HCM."""

    phone_id: int
    phone_type: str
    phone_number: str
    country_code: str
    area_code: Optional[str] = None


@dataclass
class UserPhonesResponse:
    """Represents the response from getting all of a user's phone numbers from Oracle HCM."""

    phones: list[UserPhone]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def get_phones(worker_id: str) -> UserPhonesResponse:
    """
    Gets all user's phones numbers from Oracle HCM.

    Args:
        worker_id: The user's worker_id uniquely identifying them within the Oracle HCM API.

    Returns:
        All of a user's phone numbers.
    """
    client = get_oracle_hcm_client()

    entity = f"workers/{worker_id}/child/phones"
    response = client.get_request(entity=entity)

    phones: list[UserPhone] = []
    for result in response.get("items", []):
        phones.append(
            UserPhone(
                phone_id=result.get("PhoneId", ""),
                phone_type=result.get("PhoneType", ""),
                phone_number=result.get("PhoneNumber", ""),
                area_code=result.get("AreaCode", ""),
                country_code=result.get("CountryCodeNumber", ""),
            )
        )
    return UserPhonesResponse(phones=phones)
