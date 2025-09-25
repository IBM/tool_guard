from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.workday_client import get_workday_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@dataclass
class UpdateHomePhoneResponse:
    """Represents the response from updating a user's phone number in Workday."""

    change_description: str
    request_status: str
    home_phone_id: str
    new_home_phone: str


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def update_home_phone(
    user_id: str, effective_date: str, home_phone_id: str, new_home_phone: str
) -> UpdateHomePhoneResponse:
    """
    Updates the user's home phone number in Workday.

    Args:
        user_id: The user's id uniquely identifying them within the Workday API, as returned by the
            `get_user_workday_ids` tool.
        effective_date: The date the change should become effective in ISO 8601 format (e.g., YYYY-
            MM-DD).
        home_phone_id: The ID of the phone number to update, as specified by the `get_home_phones`
            tool.
        new_home_phone: The new home phone address.

    Returns:
        The user's new home phone number.
    """
    client = get_workday_client()

    post_response = client.post_home_contact_information_changes(
        user_id=user_id, effective_date=effective_date
    )
    home_contact_information_change_id = post_response["id"]

    patch_response = client.update_home_phone(
        home_contact_information_change_id=home_contact_information_change_id,
        home_phone_id=home_phone_id,
        new_home_phone=new_home_phone,
    )

    submit_response = client.post_home_contact_information_changes_submit(
        home_contact_information_change_id=home_contact_information_change_id
    )

    return UpdateHomePhoneResponse(
        change_description=submit_response["descriptor"],
        request_status=submit_response["businessProcessParameters"]["overallStatus"],
        home_phone_id=patch_response["id"],
        new_home_phone=patch_response["completePhoneNumber"],
    )
