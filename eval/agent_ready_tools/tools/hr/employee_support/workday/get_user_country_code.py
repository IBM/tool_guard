from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.workday_client import get_workday_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@dataclass
class GetUserCountryCodeResponse:
    """Represents the response from getting a user's country code in Workday."""

    country_code: str


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def get_user_country_code(user_id: str) -> GetUserCountryCodeResponse:
    """
    Gets the ISO 3166-1 alpha-3 code of the user's country.

    Args:
        user_id: The user's user_id uniquely identifying them within the Workday API.

    Returns:
        The user's country code.
    """
    client = get_workday_client()
    url = f"api/staffing/v6/{client.tenant_name}/workers/{user_id}"
    response = client.get_request(url=url)
    return GetUserCountryCodeResponse(
        country_code=response["primaryJob"]["location"]["country"]["ISO_3166-1_Alpha-3_Code"]
    )
