from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS

# Defaulting list type to generic list.
LIST_TYPE = "genericList"


@dataclass
class Lists:
    """Represents a list in Microsoft SharePoint."""

    list_id: str
    list_name: str
    description: str


@dataclass
class ListsResponse:
    """Represents a collection of all lists from a Microsoft SharePoint site."""

    lists: List[Lists]


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def get_lists(site_id: str, limit: Optional[int] = 500) -> ListsResponse:
    """
    Retrieves a collection of all lists from a Microsoft SharePoint site.

    Args:
        site_id: The site_id uniquely identifying them within the MS Graph API, returned by
            `get_sites` tool.
        limit: Limits the number of items to retrieve/filter in Microsoft SharePoint.

    Returns:
        A collection of all lists from a Microsoft SharePoint site.
    """

    client = get_microsoft_client()
    params = {"$top": limit}
    params = {key: value for key, value in params.items() if value}

    response = client.get_request(endpoint=f"sites/{site_id}/lists", params=params)

    lists: List[Lists] = []

    for result in response.get("value", []):
        # Filter only lists with template 'genericList'
        if result.get("list", {}).get("template") == LIST_TYPE:
            lists.append(
                Lists(
                    list_id=result.get("id", ""),
                    list_name=result.get("displayName", ""),
                    description=result.get("description", ""),
                )
            )

    return ListsResponse(lists=lists)
