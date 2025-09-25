import json
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class AddListItemResponse:
    """Represents the result of adding an item to a list in Microsoft Sharepoint."""

    title: Optional[str] = None
    http_code: Optional[int] = None
    error_message: Optional[str] = None


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def add_list_item(site_id: str, list_id: str, title: str) -> AddListItemResponse:
    """
    Adds a new item to a list in Microsoft Sharepoint.

    Args:
        site_id: The site_id uniquely identifying them within the MS Graph API, returned by
            `get_sites` tool.
        list_id: The list_id uniquely identifying them within the MS Graph API, returned by
            `get_lists` tool.
        title: The title of the list item.

    Returns:
        The title of the created list item.
    """
    try:
        client = get_microsoft_client()

        payload = {"fields": {"Title": title}}

        response = client.post_request(
            endpoint=f"sites/{site_id}/lists/{list_id}/items", data=payload
        )

        return AddListItemResponse(title=response.get("fields", "").get("Title", ""))
    except HTTPError as e:
        error_message = ""
        try:
            # Try to parse the JSON error response from the API
            error_response = e.response.json()
            http_code = e.response.status_code
            error_message = error_response.get("error").get("message", "")
        except json.JSONDecodeError:
            # Fallback for non-JSON error responses (e.g., HTML from a proxy)
            error_message = e.response.text or "An HTTP error occurred without a JSON response."

        return AddListItemResponse(http_code=http_code, error_message=error_message)

    except Exception as e:  # pylint: disable=broad-except
        return AddListItemResponse(error_message=str(e))
