from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.google_client import get_google_client
from agent_ready_tools.utils.tool_credentials import GOOGLE_CONNECTIONS


@dataclass
class FolderGoogleDrive:
    """Represents a folder in Google Drive."""

    folder_id: str
    folder_name: str


@dataclass
class FoldersResponse:
    """Represents a list of folders in Google Drive."""

    folders: list[FolderGoogleDrive]
    limit: Optional[int] = 0
    next_page_token: Optional[str] = None


@tool(expected_credentials=GOOGLE_CONNECTIONS)
def get_folders(
    folder_name: Optional[str] = None,
    limit: Optional[int] = 20,
    next_page_token: Optional[str] = None,
) -> FoldersResponse:
    """
    Retrieves a list of folders in Google Drive.

    Args:
        folder_name: Filter folders in Google Drive by exact name match.
        limit: The maximum number of folders retrieved in a single API call. Defaults to 20. Use
            this to control the result size.
        next_page_token: Token for retrieving the next page of results for pagination.

    Returns:
        List of folders in Google Drive, along with pagination parameters.
    """

    client = get_google_client()

    if folder_name:
        query = f"mimeType='application/vnd.google-apps.folder' and trashed = false and name = '{folder_name}'"
    else:
        query = "mimeType='application/vnd.google-apps.folder' and trashed = false"
    params = {
        "pageSize": limit,
        "pageToken": next_page_token,
        "q": query,
    }
    # Filter out the parameters which are blank/None
    params = {key: value for key, value in params.items() if value}

    response = client.get_request(entity="files", params=params)

    folders_list: list[FolderGoogleDrive] = []

    for folder in response.get("files", []):
        folders_list.append(
            FolderGoogleDrive(folder_id=folder.get("id", ""), folder_name=folder.get("name", ""))
        )

    return FoldersResponse(
        folders=folders_list, limit=limit, next_page_token=response.get("nextPageToken", "")
    )
