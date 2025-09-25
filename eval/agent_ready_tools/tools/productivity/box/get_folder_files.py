from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.box_client import get_box_client
from agent_ready_tools.utils.tool_credentials import BOX_CONNECTIONS


@dataclass
class Entry:
    """Represents the entry of a folder."""

    id: int
    name: str
    type: Optional[str]


@dataclass
class GetFolderItemsResponse:
    """A list of entries inside the folder."""

    entries: list[Entry]
    total_count: Optional[int]
    offset: Optional[int]
    limit: Optional[int]


@tool(expected_credentials=BOX_CONNECTIONS)
def get_folder_files(folder_id: str, limit: int = 20, offset: int = 0) -> GetFolderItemsResponse:
    """
    Gets a list of entries for a folder in Box.

    Args:
        folder_id: The id of the folder returned by the `get_folder_details_by_name` tool, if
            mentioned as root folder/top level folder items then folder_id has to be 0.
        limit: The maximum number of items to retrieve (default: 20).
        offset: The starting offset for pagination (default: 0).

    Returns:
        A list of items inside a folder.
    """

    client = get_box_client()

    response = client.get_request(
        entity=f"folders/{folder_id}/items", params={"limit": limit, "offset": offset}
    )
    results = response["entries"]
    entry_list = [
        Entry(
            type=item.get("type", ""),
            id=item.get("id", ""),
            name=item.get("name", ""),
        )
        for item in results
    ]
    total_count = response.get("total_count", 0)
    offset = response.get("offset", offset)
    limit = response.get("limit", limit)
    return GetFolderItemsResponse(
        entries=entry_list, total_count=total_count, limit=limit, offset=offset
    )
