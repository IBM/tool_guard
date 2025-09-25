from typing import Any, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.zendesk_client import get_zendesk_client
from agent_ready_tools.tools.IT.zendesk.zendesk_schemas import ZendeskModules
from agent_ready_tools.utils.tool_credentials import ZENDESK_CONNECTIONS


@dataclass
class AddTagsResponse:
    """Represents the result of adding the tags in Zendesk."""

    tags: Optional[List[str]] = None
    error_message: Optional[str] = None
    error_description: Optional[str] = None
    http_code: Optional[int] = None


@tool(expected_credentials=ZENDESK_CONNECTIONS)
def add_tags(module: ZendeskModules, module_record_id: str, tags: str) -> AddTagsResponse:
    """
    Adds the tags in Zendesk.

    Args:
        module: The name of the module in Zendesk.
        module_record_id: The record ID of the module, returned by the `zendesk_list_users`, `zendesk_get_organizations`, or `zendesk_get_tickets` tool.
        tags: A comma-separated string of tags to add.


    Returns:
       The list of tags that were successfully added.
    """
    client = get_zendesk_client()

    modules = [module.value for module in ZendeskModules]
    if module and module not in modules:
        raise ValueError(f"module '{module}' is not a valid value. Accepted values are {modules}")

    payload: dict[str, Any] = {
        "tags": [tags],
    }
    try:
        response = client.put_request(entity=f"{module}/{module_record_id}/tags", payload=payload)
        return AddTagsResponse(tags=response.get("tags", []))

    except HTTPError as e:
        error_response = e.response.json()
        http_code = e.response.status_code
        if http_code == 404:
            error_message = error_response.get("error", "")
            error_description = error_response.get("description", "")
        else:
            error_message = error_response.get("error", {}).get("title", "")
            error_description = error_response.get("error", {}).get("message", "")
        return AddTagsResponse(
            error_message=error_message,
            error_description=error_description,
            http_code=http_code,
        )

    except Exception as e:  # pylint: disable=broad-except
        error_message = str(e)
        return AddTagsResponse(
            error_message=error_message,
            error_description="An unexpected error occurred.",
        )
