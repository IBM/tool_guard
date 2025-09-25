from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.zendesk_client import get_zendesk_client
from agent_ready_tools.utils.tool_credentials import ZENDESK_CONNECTIONS


@dataclass
class ZendeskUpdateUserResponse:
    """Represents the result of updating a user in Zendesk."""

    user_id: Optional[str] = None
    error_message: Optional[str] = None
    error_description: Optional[str] = None
    http_code: Optional[int] = None


@tool(expected_credentials=ZENDESK_CONNECTIONS)
def zendesk_update_user(
    user_id: str,
    new_user_name: Optional[str] = None,
    user_organization_id: Optional[str] = None,
    alias: Optional[str] = None,
    notes: Optional[str] = None,
) -> ZendeskUpdateUserResponse:
    """
    Updates a user in Zendesk.

    Args:
        user_id: The unique identifier of the user to be updated, returned by `get_users` tool.
        new_user_name: The new name of the user to update.
        user_organization_id: The id of the organization in Zendesk API, returned by `get_organizations` tool
        alias: An alias displayed to end users.
        notes: To store any notes about the user.

    Returns:
        The updated user details.
    """
    client = get_zendesk_client()

    payload = {
        "user": {
            "name": new_user_name,
            "organization_id": user_organization_id,
            "alias": alias,
            "notes": notes,
        }
    }

    # Filter out None or blank values
    payload["user"] = {
        key: value for key, value in payload.get("user", {}).items() if value is not None
    }

    try:
        response = client.patch_request(entity=f"users/{user_id}", payload=payload)
        user_data = response.get("user", {})

        return ZendeskUpdateUserResponse(user_id=str(user_data.get("id", "")))

    except HTTPError as e:
        error_response = e.response.json()
        http_code = e.response.status_code
        if http_code == 400:
            error_message = error_response.get("error", {}).get("title", "")
            error_description = error_response.get("error", {}).get("message", "")
        else:
            error_message = error_response.get("error", "")
            error_description = error_response.get("description", "")
        return ZendeskUpdateUserResponse(
            error_message=error_message,
            error_description=error_description,
            http_code=http_code,
        )

    except Exception as e:  # pylint: disable=broad-except
        error_message = str(e)
        return ZendeskUpdateUserResponse(
            error_message=error_message,
            error_description="An unexpected error occurred.",
        )
