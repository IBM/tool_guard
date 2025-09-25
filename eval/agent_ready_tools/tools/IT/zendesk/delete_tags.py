from typing import Any, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.zendesk_client import get_zendesk_client
from agent_ready_tools.tools.IT.zendesk.zendesk_schemas import ZendeskModules
from agent_ready_tools.utils.tool_credentials import ZENDESK_CONNECTIONS


@dataclass
class RemainingTagResponse:
    """Represents the result of delete operation performed on tags in Zendesk."""

    tags: Optional[List[str]] = None
    http_code: Optional[int] = None
    error_message: Optional[str] = None
    error_description: Optional[str] = None


@tool(expected_credentials=ZENDESK_CONNECTIONS)
def delete_tags(module: str, module_record_id: str, tag_names: str) -> RemainingTagResponse:
    """
    Deletes requested tags and returns remaining tags in Zendesk.

    Args:
        module: The name of the module (e.g., 'users', 'organizations', 'tickets').
        module_record_id: The record ID of the module, returned by the `zendesk_list_users` or `zendesk_get_organizations` or `get_tickets` tool using module of the current tool.
        tag_names: The names of the tags to be deleted.

    Returns:
        The tags that remain after removing the specified tags from the ticket.
    """

    client = get_zendesk_client()

    try:
        modules = [module.value for module in ZendeskModules]
        if module and module not in modules:
            raise ValueError(
                f"module '{module}' is not a valid value. Accepted values are {modules}"
            )

        tag_names_list = tag_names.split(",")

        payload: dict[str, Any] = {
            "tags": tag_names_list,
        }
        response = client.delete_request(
            entity=f"{module}/{module_record_id}/tags", payload=payload
        )
        tags = response.get("tags", [])
        return RemainingTagResponse(tags=tags, http_code=response.get("status_code", 200))
    except HTTPError as e:
        error_response = e.response.json()
        error_message = error_response.get("error", "")
        error_description = error_response.get("description", "")
        return RemainingTagResponse(
            http_code=e.response.status_code,
            error_message=error_message,
            error_description=error_description,
        )
    except Exception as e:  # pylint: disable=broad-except
        error_message = str(e)
        return RemainingTagResponse(
            http_code=response.get("status_code", 500),
            error_message=error_message,
            error_description="An unexpected error occurred.",
        )
