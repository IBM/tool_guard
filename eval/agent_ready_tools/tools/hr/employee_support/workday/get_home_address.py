from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.workday_client import get_workday_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@dataclass
class WorkdayHomeAddress:
    """Represents a home address in Workday."""

    address_id: str
    address_line_1: str
    city: str
    state_id: Optional[str]  # countryRegion
    country_id: Optional[str]
    postal_code: str
    state: Optional[str]
    country: Optional[str]
    address_line_2: Optional[str]


@dataclass
class WorkdayHomeAddressResponse:
    """Represents the response from getting a user's home addresses in Workday."""

    home_addresses: list[WorkdayHomeAddress]


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def get_home_address(person_id: str) -> WorkdayHomeAddressResponse:
    """
    Gets the home addresses of a person in Workday.

    Args:
        person_id: The user's person id within the Workday API.

    Returns:
        WorkdayHomeAddressResponse
    """
    client = get_workday_client()

    url = f"api/person/v4/{client.tenant_name}/people/{person_id}/homeAddresses"
    response = client.get_request(url=url)

    return_values: List[WorkdayHomeAddress] = []

    if "data" in response:
        resp_data = response.get("data", [])

        for data in resp_data:
            country_region_data = data.get("countryRegion", None)
            country_data = data.get("country", None)

            return_values.append(
                WorkdayHomeAddress(
                    address_id=data.get("id", None),
                    address_line_1=data.get("addressLine1", None),
                    address_line_2=data.get("addressLine2", None),
                    city=data.get("city", None),
                    state_id=country_region_data.get("id", None) if country_region_data else None,
                    state=(
                        country_region_data.get("descriptor", None) if country_region_data else None
                    ),
                    country_id=country_data.get("id", None) if country_data else None,
                    country=country_data.get("descriptor", None) if country_data else None,
                    postal_code=data.get("postalCode", None),
                )
            )

    return WorkdayHomeAddressResponse(home_addresses=return_values)
