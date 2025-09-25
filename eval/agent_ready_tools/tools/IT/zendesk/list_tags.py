from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.zendesk_client import get_zendesk_client
from agent_ready_tools.tools.IT.zendesk.zendesk_schemas import ZendeskModules
from agent_ready_tools.utils.tool_credentials import ZENDESK_CONNECTIONS


@dataclass
class GetTagsResponse:
    """Represents the result of retrieving all tags in Zendesk."""

    tags: List[str]
    http_code: Optional[int] = None
    message: Optional[str] = None


@tool(expected_credentials=ZENDESK_CONNECTIONS)
def list_tags(module: str, module_record_id: str) -> GetTagsResponse:
    """
    Gets all the tags in Zendesk.

    Args:
        module: The name of the module (e.g., 'users', 'organizations', 'tickets').
        module_record_id: The ID of the module, returned by the `list_users` or `list_organizations` or `list_tickets` tool using module of the current tool.

    Returns:
       The list of tags.
    """

    try:
        client = get_zendesk_client()

        modules = [module.value for module in ZendeskModules]
        if module and module not in modules:
            raise ValueError(
                f"module '{module}' is not a valid value. Accepted values are {modules}"
            )

        response = client.get_request(entity=f"{module}/{module_record_id}/tags")
        return GetTagsResponse(tags=response.get("tags", []))

    except HTTPError as e:
        error_response = e.response.json() if e.response is not None else None
        message = (
            error_response.get("description", "")
            if error_response
            else "An unexpected error occurred."
        )
        return GetTagsResponse(
            tags=[],  # Provide default empty list
            http_code=e.response.status_code,
            message=message,
        )
    except Exception as e:  # pylint: disable=broad-except
        return GetTagsResponse(
            tags=[],  # Provide default empty list
            http_code=500,
            message=str(e),
        )
