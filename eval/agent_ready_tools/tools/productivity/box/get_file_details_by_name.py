from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.box_client import get_box_client
from agent_ready_tools.utils.tool_credentials import BOX_CONNECTIONS


@dataclass
class FileDetails:
    """Represents the details of file in Box."""

    id: str
    name: str
    path_structure: str
    parent_name: str
    item_type: Optional[str]
    created_by_name: Optional[str]
    modified_by_name: Optional[str]
    owned_by_name: Optional[str]


@dataclass
class FileDetailsResponse:
    """A list of file details in a Box."""

    details: List[FileDetails]


@tool(expected_credentials=BOX_CONNECTIONS)
def get_file_details_by_name(name: str) -> FileDetailsResponse:
    """
    Gets a list of files details in this Box.

    Args:
        name: The name of the file to filter in the Box.

    Returns:
        A list of files.
    """

    client = get_box_client()
    item_type = "file"
    params = {"query": f"{name}", "type": f"{item_type}"}
    params = {key: value for key, value in params.items() if value}

    response = client.get_request(entity="search", params=params)

    details_list = [
        FileDetails(
            id=detail.get("id"),
            name=detail.get("name"),
            item_type=detail.get("type"),
            created_by_name=detail.get("created_by").get("name"),
            modified_by_name=detail.get("modified_by").get("name"),
            owned_by_name=detail.get("owned_by").get("name"),
            path_structure="/".join(
                entry["name"] for entry in detail.get("path_collection", {}).get("entries", [])
            ),
            parent_name=detail.get("parent").get("name"),
        )
        for detail in response.get("entries", [])
    ]

    return FileDetailsResponse(details=details_list)
