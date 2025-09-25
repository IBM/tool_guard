from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.google_client import get_google_client
from agent_ready_tools.utils.tool_credentials import GOOGLE_CONNECTIONS


@dataclass
class Files:
    """Represents the details of a file in Google Drive."""

    file_id: str
    file_name: str
    file_type: str
    kind: str


@dataclass
class FilesResponse:
    """Represents a list of files in Google Drive."""

    files: List[Files]
    limit: Optional[int] = 0
    next_page_token: Optional[str] = None


@tool(expected_credentials=GOOGLE_CONNECTIONS)
def get_files(
    file_name: Optional[str] = None,
    limit: Optional[int] = 20,
    next_page_token: Optional[str] = None,
) -> FilesResponse:
    """
    Retrieves a list of files in Google Drive.

    Args:
        file_name: The file_name is used to filter results in Google Drive based upon the name of
            the file.
        limit: The maximum number of files retrieved in a single API call. Defaults to 20. Use this
            to control the size of the result set in Google Drive.
        next_page_token: A token used to skip a specific number of items for pagination purposes.
            Use this to retrieve subsequent pages of results when handling large datasets.

    Returns:
        List of all the files in Google Drive, along with pagination parameters (limit and
        next_page_token).
    """

    client = get_google_client()

    query = "mimeType !='application/vnd.google-apps.folder'"
    params = {
        "pageSize": limit,
        "pageToken": next_page_token,
        "q": query,
    }

    if file_name:
        params["q"] = f"name = '{file_name}'"

    response = client.get_request(entity="files", params=params)

    files_list: List[Files] = []

    for file in response["files"]:
        files_list.append(
            Files(
                file_id=file.get("id", ""),
                file_name=file.get("name", ""),
                file_type=file.get("mimeType", ""),
                kind=file.get("kind", ""),
            )
        )

    return FilesResponse(
        files=files_list, limit=limit, next_page_token=response.get("nextPageToken", "")
    )
