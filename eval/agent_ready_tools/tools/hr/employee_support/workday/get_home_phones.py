from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.workday_client import get_workday_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@dataclass
class HomePhone:
    """Represents a home phone number in Workday."""

    phone_number: str
    phone_id: str
    is_primary: Optional[bool] = None
    country_code: Optional[str] = None


@dataclass
class GetHomePhonesResponse:
    """Represents the response from getting a user's home phones in Workday."""

    home_phone_numbers: list[HomePhone]


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def get_home_phones(person_id: str) -> GetHomePhonesResponse:
    """
    Gets a user's home phones in Workday.

    Args:
        person_id: The user's person_id uniquely identifying them within the Workday API.

    Returns:
        The user's home phones.
    """
    client = get_workday_client()

    url = f"api/person/v4/{client.tenant_name}/people/{person_id}/homePhones"
    response = client.get_request(url=url)

    home_phones_list: list[HomePhone] = []
    for phone in response["data"]:
        home_phones_list.append(
            HomePhone(
                phone_id=phone.get("id"),
                phone_number=phone.get("descriptor"),
                country_code=phone.get("countryPhoneCode").get("countryPhoneCode"),
                is_primary=phone["usage"].get("primary"),
            )
        )
    return GetHomePhonesResponse(home_phone_numbers=home_phones_list)
