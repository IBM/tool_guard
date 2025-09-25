from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.zendesk_client import get_zendesk_client
from agent_ready_tools.utils.tool_credentials import ZENDESK_CONNECTIONS


@dataclass
class UpdateGroupResponse:
    """Represents the result of updating a group in Zendesk."""

    name: Optional[str] = None
    updated_at: Optional[str] = None
    description: Optional[str] = None
    http_code: Optional[int] = None
    error_description: Optional[str] = None


@tool(expected_credentials=ZENDESK_CONNECTIONS)
def update_group(
    group_id: str, new_group_name: Optional[str] = None, new_group_description: Optional[str] = None
) -> UpdateGroupResponse:
    """
    Updates a group in Zendesk.

    Args:
        group_id: The ID of the group to be updated, returned by the `zendesk_get_groups` tool.
        new_group_name: The new name of the group.
        new_group_description: The new description of the group.

    Returns:
        Details of the updated group in Zendesk.
    """

    client = get_zendesk_client()

    data = {
        "name": new_group_name,
        "description": new_group_description,
    }

    # Filter out the blank parameters
    data = {key: value for key, value in data.items() if value}

    try:
        client = get_zendesk_client()
        response = client.put_request(entity=f"groups/{group_id}", payload={"group": data})
        print(data)
        group_data = response.get("group", {})
        return UpdateGroupResponse(
            name=group_data.get("name", ""),
            description=group_data.get("description", ""),
            updated_at=group_data.get("updated_at", ""),
        )

    except HTTPError as e:
        error_response = e.response.json() if e.response is not None else {}
        error = error_response.get("error", "")
        if isinstance(error, dict):
            error_description = error.get("message", "")
        else:
            error_description = error_response.get("details", {}).get("name", [{}])[0].get(
                "description", ""
            ) or error_response.get("error", "")
        http_code = e.response.status_code
        return UpdateGroupResponse(
            error_description=error_description,
            http_code=http_code,
        )

    except Exception as e:  # pylint: disable=broad-except
        return UpdateGroupResponse(
            error_description=f"An unexpected error occurred.{e}",
        )
