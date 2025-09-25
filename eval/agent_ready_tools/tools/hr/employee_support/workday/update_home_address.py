from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.workday_client import get_workday_client
from agent_ready_tools.tools.hr.employee_support.workday.get_home_address import WorkdayHomeAddress
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def update_home_address(
    user_id: str,
    address_id: str,
    effective_date: str,
    address_line_1: str,
    country_id: str,
    state_id: str,
    city: str,
    postal_code: str,
    is_primary: bool,
    address_line_2: Optional[str] = None,
) -> Optional[WorkdayHomeAddress]:
    """
    Updates the user's home address in Workday.

    Args:
        user_id: The user's id uniquely identifying them within the Workday API.
        address_id: The ID of the address to update, as specified by the `get_home_address` tool.
        effective_date: The effective date user change take place in ISO 8601 format.
        address_line_1: First line of address.
        country_id: country ID, as specified by the `get_country_id` tool.
        state_id: The state ID, as specified by the `get_state_id` tool.
        city: The name of the city the address is located in.
        postal_code: The postal code or the zip code.
        is_primary: A true or false value indicating whether this will be a primary address.
        address_line_2: Second line of address.

    Returns:
        The new home address after performing the update to the user's home address.
    """
    client = get_workday_client()

    response = client.post_home_contact_information_changes(
        user_id=user_id, effective_date=effective_date
    )

    home_contact_information_changes_id = response["id"]

    put_response = client.put_home_address(
        home_contact_information_changes_id=home_contact_information_changes_id,
        address_id=address_id,
        address_line_1=address_line_1,
        address_line_2=address_line_2,
        city=city,
        state_id=state_id,
        country_id=country_id,
        postal_code=postal_code,
        is_primary=is_primary,
    )

    response = client.post_home_contact_information_changes_submit(
        home_contact_information_change_id=home_contact_information_changes_id
    )

    try:
        assert response["businessProcessParameters"]["overallStatus"] == "Successfully Completed"
    except (IndexError, AttributeError, AssertionError):
        raise ValueError(f"the address update was not submitted successfully")

    return WorkdayHomeAddress(
        address_id=put_response["id"],
        address_line_1=put_response["addressLine1"],
        address_line_2=put_response.get("addressLine2"),
        city=put_response["city"],
        state_id=put_response["countryRegion"]["id"],
        state=None,
        country_id=put_response["country"]["id"],
        country=None,
        postal_code=put_response["postalCode"],
    )
