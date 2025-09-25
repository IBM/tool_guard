from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class CreateNewFolderResponse:
    """Represents the result of creating a new folder in Microsoft Sharepoint."""

    folder_name: str


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def create_new_folder(
    site_id: str, folder_name: str, parent_folder_id: str = "root"
) -> CreateNewFolderResponse:
    """
    Creates a new folder in Microsoft Sharepoint.

    Args:
        site_id: The site_id uniquely identifying them within the MS Graph API, returned by the
            `get_sites` tool.
        folder_name: The name of the folder.
        parent_folder_id: The item_id of the parent folder returned by the `sharepoint_get_folders`
            tool  in which the new folder will be created. Default is "root" (root folder).

    Returns:
        The result of creating a new folder.
    """

    client = get_microsoft_client()
    # The @microsoft.graph.conflictBehavior value is hardcoded to 'rename',
    # This auto renames the new folder with a numbered suffix to avoid a naming conflict
    # e.g., if Rahul_Test_Folder already exists
    # New folder would be named as Rahul_Test_Folder 1
    payload = {"name": folder_name, "folder": {}, "@microsoft.graph.conflictBehavior": "rename"}

    response = client.post_request(
        endpoint=f"sites/{site_id}/drive/items/{parent_folder_id}/children", data=payload
    )
    return CreateNewFolderResponse(folder_name=response["name"])
