from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class Item:
    """Represents sigle item."""

    id: str
    name: str


@dataclass
class GetAllFoldersItemsResponse:
    """Represents the result of getting all items in the given folder."""

    items: List[Item]


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def get_all_folders_items(site_id: str, item_id: str) -> GetAllFoldersItemsResponse:
    """
    Get all folders items from MS Graph API.

    Args:
        site_id: The id of the site. The site id will be returned by the `get_sites` tool.
        item_id: The id of the folder. The item id will be returned by the `sharepoint_get_folders`
            tool.

    Returns:
        List of items in folder.
    """
    client = get_microsoft_client()

    endpoint = f"/sites/{site_id}/drive/items/{item_id}/children"
    response = client.get_request(endpoint)

    items: List[Item] = []

    for result in response["value"]:
        items.append(
            Item(
                id=result.get("id"),
                name=result.get("name"),
            )
        )

    return GetAllFoldersItemsResponse(items=items)
