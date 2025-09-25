from typing import Any, Dict, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.get_id_from_links import get_query_param_from_links
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class ContactFolder:
    """Represents a contact folder in Microsoft Outlook."""

    contact_folder_id: str
    contact_folder_name: str


@dataclass
class GetContactFoldersResponse:
    """Represents the response for retrieving contact folders in Microsoft Outlook."""

    contact_folders: List[ContactFolder]
    limit: Optional[int]
    skip: Optional[int]


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def get_contact_folders(
    folder_name: Optional[str] = None, limit: Optional[int] = 100, skip: Optional[int] = 0
) -> GetContactFoldersResponse:
    """
    Gets a list of contact folders from Microsoft Outlook.

    Args:
        folder_name: The field is used to filter out contact folders by their names.
        limit: The maximum number of contact folders to retrieve in a single API call. Defaults to
            100. Use this to control the size of the result set.
        skip: The number of contact folders to skip for pagination purposes. Use this to retrieve
            subsequent pages of results when handling large datasets.

    Returns:
        List of contact folders with their contact_folder_id and contact_folder_name, along with
        pagination parameters (limit and skip).
    """
    client = get_microsoft_client()

    params: Dict[str, Any] = {}
    if folder_name:
        params["$filter"] = f"displayName eq '{folder_name}'"
    if limit:
        params["$top"] = limit
    if skip:
        params["$skip"] = skip
    endpoint = f"{client.get_user_resource_path()}/contactFolders"

    response = client.get_request(endpoint, params=params)

    contact_folders: List[ContactFolder] = [
        ContactFolder(
            contact_folder_id=result.get("id", ""),
            contact_folder_name=result.get("displayName", ""),
        )
        for result in response.get("value", [])
    ]

    # Extract limit and skip from @odata.nextLink if it exists
    output_limit = None
    output_skip = None
    next_api_link = response.get("@odata.nextLink", "")
    if next_api_link:
        query_params = get_query_param_from_links(next_api_link)
        output_limit = int(query_params["$top"])
        output_skip = int(query_params["$skip"])

    return GetContactFoldersResponse(
        contact_folders=contact_folders,
        limit=output_limit,
        skip=output_skip,
    )
