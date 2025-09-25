from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.google_client import get_google_client
from agent_ready_tools.utils.tool_credentials import GOOGLE_CONNECTIONS


@dataclass
class FolderItems:
    """Represents items in Google Drive folder."""

    folder_item_name: str
    folder_item_id: str


@dataclass
class FolderItemsResult:
    """Represents the response from getting items from Google Drive folder."""

    folder_items: List[FolderItems]


@tool(expected_credentials=GOOGLE_CONNECTIONS)
def get_folder_items(folder_id: str) -> FolderItemsResult:
    """
    Gets items from Google Drive folder.

    Args:
        folder_id: The id of the folder returned by the `get_folders` tool.

    Returns:
        The items in a Google Drive folder.
    """
    client = get_google_client()

    params = {"q": f"'{folder_id}' in parents"}
    response = client.get_request(entity=f"files", params=params)
    folder_items: list[FolderItems] = []
    for result in response["files"]:
        folder_items.append(
            FolderItems(
                folder_item_name=result.get("name", ""), folder_item_id=result.get("id", "")
            )
        )
    return FolderItemsResult(folder_items=folder_items)
