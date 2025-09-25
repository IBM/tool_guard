from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class GetDownloadURLResponse:
    """Download url and status code for a file download in Microsoft SharePoint."""

    url: str
    http_code: int


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def download_a_file(site_id: str, file_path: str) -> GetDownloadURLResponse:
    """
    Get a file's download URL in Microsoft SharePoint.

    Args:
        site_id: The site_id uniquely identifying them within the MS Graph API, returned by
            `get_sites` tool.
        file_path: The root path of a file in Microsoft SharePoint.

    Returns:
        URL and status code of a file download.
    """
    client = get_microsoft_client()

    entity = f"sites/{site_id}/drive/root:/{file_path}"
    response = client.get_request(endpoint=entity)
    return GetDownloadURLResponse(
        url=response.get("@microsoft.graph.downloadUrl", ""),
        http_code=response.get("status_code", ""),
    )
