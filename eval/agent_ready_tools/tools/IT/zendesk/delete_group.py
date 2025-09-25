from http import HTTPStatus
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.zendesk_client import get_zendesk_client
from agent_ready_tools.utils.tool_credentials import ZENDESK_CONNECTIONS


@dataclass
class DeleteGroupResponse:
    """Represents the result of delete operation performed on a group in Zendesk."""

    http_code: int
    message: Optional[str] = None


@tool(expected_credentials=ZENDESK_CONNECTIONS)
def delete_group(group_id: str) -> DeleteGroupResponse:
    """
    Deletes a group in Zendesk.

    Args:
        group_id: The id of the group, returned by `list_groups` tool.

    Returns:
        The status of the delete operation.
    """
    client = get_zendesk_client()

    try:
        response = client.delete_request(entity=f"groups/{group_id}")
        return DeleteGroupResponse(http_code=response["status_code"])
    except HTTPError as e:
        error_response = e.response.json() if e.response else None
        message = (
            error_response.get("description", "")
            if error_response
            else "The specified group does not exist."
        )
        return DeleteGroupResponse(
            http_code=e.response.status_code if e.response else HTTPStatus.NOT_FOUND,
            message=message,
        )
    except Exception as e:  # pylint: disable=broad-except
        return DeleteGroupResponse(http_code=HTTPStatus.INTERNAL_SERVER_ERROR, message=str(e))
