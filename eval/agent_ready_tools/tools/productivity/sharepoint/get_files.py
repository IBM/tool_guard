import re
from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.get_id_from_links import get_query_param_from_links
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class SharePointFile:
    """Represent the single details of the file in Microsoft Sharepoint."""

    file_id: str
    file_name: str
    file_path_url: str


@dataclass
class SharePointFilesResponse:
    """Represents the list of files in Microsoft Sharepoint."""

    files: List[SharePointFile]
    limit: Optional[int] = 0
    skip_token: Optional[str] = None


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def sharepoint_get_files(
    site_id: str, limit: Optional[int] = 50, skip_token: Optional[str] = None
) -> SharePointFilesResponse:
    """
    Get all files from Sharepoint.

    Args:
        site_id: The site_id uniquely identifying them within the MS Graph API, returned by
            `get_sites` tool.
        limit: Limits the number of files to retrieve in Microsoft SharePoint.
        skip_token: The number of files to skip for pagination purposes. Use this to retrieve
            subsequent pages of results when handling large datasets.

    Returns:
        A list of files from Sharepoint.
    """

    client = get_microsoft_client()

    params = {
        "$filter": "item",
        "$top": limit,
        "$skiptoken": skip_token,
    }
    params = {key: value for key, value in params.items() if value}
    response = client.get_request(endpoint=f"/sites/{site_id}/drive/items", params=params)

    file_list = []
    for item in response.get("value", []):
        if item.get("file", {}):
            web_url = item.get("webUrl", "")
            match = re.search(r"Shared%20Documents/(.*)", web_url)
            file_path_url = match.group(1) if match else None
            if file_path_url is None:
                parent_reference = item.get("parentReference", {})
                parent_path = parent_reference.get("path", "")
                match = re.search(r"root:/(.*)", parent_path)
                file_path_url = match.group(1) if match else None
                file_path_url = (
                    file_path_url + "/" + item.get("name", "")
                    if file_path_url
                    else item.get("name", "")
                )

            file_list.append(
                SharePointFile(
                    file_id=item.get("id", ""),
                    file_name=item.get("name", ""),
                    file_path_url=file_path_url,
                )
            )
    next_api_link = response.get("@odata.nextLink", "")

    output_limit = None
    output_skip_token = None
    if next_api_link:
        query_params = get_query_param_from_links(href=next_api_link)
        output_limit = int(query_params.get("$top", ""))
        output_skip_token = query_params.get("$skiptoken", "")
    return SharePointFilesResponse(
        files=file_list, limit=output_limit, skip_token=output_skip_token
    )
