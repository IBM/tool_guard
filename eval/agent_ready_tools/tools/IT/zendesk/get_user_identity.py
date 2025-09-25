from http import HTTPStatus
from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.zendesk_client import get_zendesk_client
from agent_ready_tools.utils.tool_credentials import ZENDESK_CONNECTIONS


@dataclass
class UserIdentity:
    """Represents a user identity in Zendesk."""

    identity_id: str
    identity_type: str
    value: Optional[str] = None
    primary: Optional[bool] = None


@dataclass
class GetUserIdentityResponse:
    """Represents the response for retrieving a user's identity in Zendesk."""

    identities: List[UserIdentity]
    error_description: Optional[str] = None
    http_code: Optional[int] = None


@tool(expected_credentials=ZENDESK_CONNECTIONS)
def get_user_identity(user_id: str, identity_type: Optional[str] = None) -> GetUserIdentityResponse:
    """
    Retrieves a specific user identity from Zendesk.

    Args:
        user_id: The id of the user, returned by `get_users` tool.
        identity_type: The type of the identity.

    Returns:
        The user's identity details.
    """
    try:

        client = get_zendesk_client()
        params = {}
        if identity_type:
            params["type[]"] = identity_type
        response = client.get_request(entity=f"users/{user_id}/identities", params=params)

        identity_data_list = response.get("identities", [])

        identities: List[UserIdentity] = [
            UserIdentity(
                identity_id=str(identity.get("id", "")),
                identity_type=identity.get("type", ""),
                value=identity.get("value", ""),
                primary=identity.get("primary", ""),
            )
            for identity in identity_data_list
        ]

        return GetUserIdentityResponse(identities=identities)

    except HTTPError as e:
        error_response = e.response.json() if e.response is not None else {}
        error_description = (
            error_response.get("error", {}).get("message", "")
            if error_response
            else "An unexpected error occurred."
        )

        return GetUserIdentityResponse(
            identities=[],
            error_description=error_description,
            http_code=(
                e.response.status_code if e.response else HTTPStatus.INTERNAL_SERVER_ERROR.value
            ),
        )

    except Exception as e:  # pylint: disable=broad-except
        return GetUserIdentityResponse(
            identities=[],
            http_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            error_description=str(e),
        )
