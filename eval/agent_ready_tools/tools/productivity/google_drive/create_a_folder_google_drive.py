from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.google_client import get_google_client
from agent_ready_tools.utils.tool_credentials import GOOGLE_CONNECTIONS


@dataclass
class CreateFolderGoogleDriveResponse:
    """Represents the result of creating a folder in Google Drive."""

    folder_name: str


@tool(expected_credentials=GOOGLE_CONNECTIONS)
def create_a_folder_google_drive(
    folder_name: str, description: str, parent_id: Optional[str] = None
) -> CreateFolderGoogleDriveResponse:
    """
    Creates a folder in Google Drive.

    Args:
        folder_name: The name of the folder in Google Drive.
        description: The description of the folder in Google Drive.
        parent_id: The folder_id of the parent folder in Google Drive returned by the `get_folders`
            tool.

    Returns:
        The result of performing the creation of folder.
    """
    client = get_google_client()

    payload: dict[str, Any] = {
        "name": folder_name,
        "description": description,
        "parents": [parent_id],
        "mimeType": "application/vnd.google-apps.folder",
    }

    response = client.post_request(entity="files", payload=payload)
    return CreateFolderGoogleDriveResponse(folder_name=response.get("name", ""))
