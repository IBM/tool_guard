from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.workday_client import get_workday_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@dataclass
class UpdateHomeAddressResponse:
    """Represents the response from updating a user's home email in Workday."""

    change_description: str
    request_status: str
    email_id: str
    new_email_address: str


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def update_home_email(
    user_id: str, effective_date: str, home_email_id: str, new_home_email: str
) -> UpdateHomeAddressResponse:
    """
    Updates the user's home email in Workday.

    Args:
        user_id: The user's id uniquely identifying them within the Workday API.
        effective_date: The date the change should become effective in ISO 8601 format (e.g., YYYY-
            MM-DD).
        home_email_id: The ID of the email address to update, as specified by the `get_home_email`
            tool.
        new_home_email: The new home email address.

    Returns:
        The user's new home email address.
    """
    client = get_workday_client()

    post_response = client.post_home_contact_information_changes(
        user_id=user_id, effective_date=effective_date
    )
    home_contact_information_change_id = post_response["id"]

    if (
        home_email_id in ["null", "NULL", "None", ""] or len(home_email_id) != 32
    ):  # uuid has length of 32
        update_response = client.add_home_email(
            home_contact_information_change_id=home_contact_information_change_id,
            new_home_email=new_home_email,
        )
    else:
        update_response = client.update_home_email(
            home_contact_information_change_id=home_contact_information_change_id,
            home_email_id=home_email_id,
            new_home_email=new_home_email,
        )

    submit_response = client.post_home_contact_information_changes_submit(
        home_contact_information_change_id=home_contact_information_change_id
    )

    return UpdateHomeAddressResponse(
        change_description=submit_response["descriptor"],
        request_status=submit_response["businessProcessParameters"]["overallStatus"],
        email_id=update_response["id"],
        new_email_address=update_response["emailAddress"],
    )
