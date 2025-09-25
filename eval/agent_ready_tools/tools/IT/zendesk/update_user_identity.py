from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.zendesk_client import get_zendesk_client
from agent_ready_tools.utils.tool_credentials import ZENDESK_CONNECTIONS


@dataclass
class UpdateUserIdentityResponse:
    """Represents the result of updating a user indentity in Zendesk."""

    user_identity_id: Optional[str] = None
    error_message: Optional[str] = None
    error_description: Optional[str] = None
    http_code: Optional[int] = None


@tool(expected_credentials=ZENDESK_CONNECTIONS)
def update_user_identity(
    user_id: str,
    user_identity_id: str,
    value: Optional[str] = None,
    primary: Optional[bool] = False,
) -> UpdateUserIdentityResponse:
    """
    Updates the user's identity in the Zendesk.

    Args:
        user_id: The unique identifier of the user within the Zendesk API, returned by the `get_users` tool.
        user_identity_id: The unique identifier of the identity to be updated, returned by the `get_user_identity` tool.
        value: The value of the identity, determined by the type of identity.
        primary: Indicates whether the identity is primary identity.

    Returns:
        The updated unique identity of the user within Zendesk.
    """

    client = get_zendesk_client()

    payload = {
        "identity": {
            "value": value,
            "primary": primary,
        }
    }

    payload["identity"] = {
        key: value for key, value in payload.get("identity", {}).items() if value is not None
    }

    try:
        response = client.patch_request(
            entity=f"users/{user_id}/identities/{user_identity_id}", payload=payload
        )
        identity = response.get("identity", {})

        return UpdateUserIdentityResponse(user_identity_id=str(identity.get("id", "")))

    except HTTPError as e:
        error_response = e.response.json()
        http_code = e.response.status_code
        if http_code == 400:
            error_message = error_response.get("error", {}).get("title", "")
            error_description = error_response.get("error", {}).get("message", "")
        else:
            error_message = error_response.get("error", "")
            error_description = error_response.get("description", "")
        return UpdateUserIdentityResponse(
            error_message=error_message,
            error_description=error_description,
            http_code=http_code,
        )

    except Exception as e:  # pylint: disable=broad-except
        error_message = str(e)
        return UpdateUserIdentityResponse(
            error_message=error_message,
            error_description="An unexpected error occurred.",
        )
