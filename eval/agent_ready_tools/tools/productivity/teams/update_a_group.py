from http import HTTPStatus
import json
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class UpdateAGroupResponse:
    """Represents the result of updating group details in Microsoft Teams."""

    http_code: int
    error_message: Optional[str]


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def update_a_group(
    original_group_id: str,
    new_group_name: str,
    new_group_description: str,
) -> UpdateAGroupResponse:
    """
    Updates group details in Microsoft Teams.

    Args:
        original_group_id: The id of the group, returned by the `get_groups` tool.
        new_group_name: The new name of the Microsoft Teams group.
        new_group_description: The new description of the Microsoft Teams group.

    Returns:
        Confirmation of the details update.
    """
    client = get_microsoft_client()

    payload = {"displayName": new_group_name, "description": new_group_description}
    entity = f"groups/{original_group_id}"
    try:
        response = client.update_request(endpoint=entity, data=payload)

        return UpdateAGroupResponse(
            http_code=response.get("status_code", HTTPStatus.NO_CONTENT), error_message=None
        )

    except HTTPError as e:
        error_message = ""
        try:
            # Try to parse the JSON error response from the API
            error_response = e.response.json()
            error_message = error_response.get("error", {}).get("message", "")
        except json.JSONDecodeError:
            # Fallback for non-JSON error responses (e.g., HTML from a proxy)
            error_message = e.response.text or "An HTTP error occurred without a JSON response."

        return UpdateAGroupResponse(
            http_code=e.response.status_code,
            error_message=error_message,
        )
