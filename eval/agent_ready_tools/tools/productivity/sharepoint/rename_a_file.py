from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class RenameFileResponse:
    """Represents the result of renaming a file in Microsoft SharePoint."""

    new_file_name: str


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def rename_a_file(
    site_id: str,
    file_id: str,
    new_file_name: str,
) -> RenameFileResponse:
    """
    Rename a file in Microsoft SharePoint.

    Args:
        site_id: The site_id uniquely identifying them within the MS Graph API, returned by
            `get_sites` tool.
        file_id: The unique id for a file in Microsoft SharePoint obtained by `sharepoint_get_files`
            tool.
        new_file_name: The new name of the file to update in Microsoft Sharepoint.

    Returns:
        The updated file name.
    """
    client = get_microsoft_client()
    payload = {"name": new_file_name}
    response = client.update_request(
        endpoint=f"sites/{site_id}/drive/items/{file_id}", data=payload
    )
    return RenameFileResponse(new_file_name=response.get("name", ""))
