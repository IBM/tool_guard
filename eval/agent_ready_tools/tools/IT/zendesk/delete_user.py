from http import HTTPStatus
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.zendesk_client import get_zendesk_client
from agent_ready_tools.utils.tool_credentials import ZENDESK_CONNECTIONS


@dataclass
class DeleteUserResponse:
    """Represents the result of deleting a user in Zendesk."""

    user_name: Optional[str] = None
    active_status: Optional[bool] = None
    error_message: Optional[str] = None
    error_description: Optional[str] = None
    http_code: Optional[int] = None


@tool(expected_credentials=ZENDESK_CONNECTIONS)
def delete_user(user_id: str) -> DeleteUserResponse:
    """
    Deletes a user in Zendesk.

    Args:
        user_id: The id of the user, returned by the `list_user` tool.

    Returns:
        The result of performing the delete a user in Zendesk.
    """
    client = get_zendesk_client()

    try:
        response = client.delete_request(entity=f"users/{user_id}")
        result = response.get("user", {})
        return DeleteUserResponse(
            user_name=result.get("name", ""), active_status=result.get("active", False)
        )
    except HTTPError as e:
        error_response = e.response.json() if e.response else {}
        http_code = e.response.status_code if e.response else HTTPStatus.INTERNAL_SERVER_ERROR.value
        error_value = error_response.get("error")

        if isinstance(error_value, dict):
            error_message = error_value.get("title", "")
            error_description = error_value.get("message", "")
        else:
            error_message = error_value or ""
            error_description = error_response.get("description", "")

        return DeleteUserResponse(
            error_message=error_message,
            error_description=error_description,
            http_code=http_code,
        )

    except Exception as e:  # pylint: disable=broad-except
        error_message = str(e)
        return DeleteUserResponse(
            error_message=error_message,
            error_description="An unexpected error occurred.",
            http_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )
