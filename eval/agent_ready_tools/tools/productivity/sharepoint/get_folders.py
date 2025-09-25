import re
from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.get_id_from_links import get_query_param_from_links
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class SharePointFolder:
    """Represent the single details of the folder in Microsoft Sharepoint."""

    folder_id: str
    folder_name: str
    folder_path_url: str


@dataclass
class SharePointFoldersResponse:
    """Represents the list of folders in Microsoft Sharepoint."""

    folders: List[SharePointFolder]
    limit: Optional[int] = 0
    skip_token: Optional[str] = None


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def sharepoint_get_folders(
    site_id: str, limit: Optional[int] = 50, skip_token: Optional[str] = None
) -> SharePointFoldersResponse:
    """
    Get all folders from Sharepoint.

    Args:
        site_id: The site_id uniquely identifying them within the MS Graph API, returned by
            `get_sites` tool.
        limit: Limits the number of folders to retrieve in Microsoft SharePoint.
        skip_token: The number of folders to skip for pagination purposes. Use this to retrieve
            subsequent pages of results when handling large datasets.

    Returns:
        A list of folders from Sharepoint.
    """

    client = get_microsoft_client()

    params = {
        "$filter": "item",
        "$top": limit,
        "$skiptoken": skip_token,
    }
    params = {key: value for key, value in params.items() if value}
    response = client.get_request(endpoint=f"/sites/{site_id}/drive/items", params=params)

    folder_list = []
    for item in response.get("value", []):
        if item.get("folder", {}):
            web_url = item.get("webUrl", "")
            match = re.search(r"Shared%20Documents(.*)", web_url)
            folder_path_url = match.group(1) if match else ""

            folder_list.append(
                SharePointFolder(
                    folder_id=item.get("id", ""),
                    folder_name=item.get("name", ""),
                    folder_path_url=folder_path_url,
                )
            )
    next_api_link = response.get("@odata.nextLink", "")

    output_limit = None
    output_skip_token = None
    if next_api_link:
        query_params = get_query_param_from_links(href=next_api_link)
        output_limit = int(query_params.get("$top", ""))
        output_skip_token = query_params.get("$skiptoken", "")
    return SharePointFoldersResponse(
        folders=folder_list, limit=output_limit, skip_token=output_skip_token
    )
