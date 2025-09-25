from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.google_client import get_google_client
from agent_ready_tools.utils.tool_credentials import GOOGLE_CONNECTIONS


@dataclass
class FileContentGoogleDriveResult:
    """Retrieves the contents of a file in Google Drive."""

    content: str


@tool(expected_credentials=GOOGLE_CONNECTIONS)
def get_file_content_google_drive(
    file_id: str,
    alt: str = "media",
    file_type: Optional[str] = None,
) -> FileContentGoogleDriveResult:
    """
    Retrieves the content of a file in Google Drive.

    Args:
        file_id: The id of the file returned by the `get_files` tool.
        alt: Returns the actual file content.
        file_type: The type of the file returned by the `get_files` tool.

    Returns:
        The content of a file.
    """

    client = get_google_client()

    # Handle different files
    if file_type == "application/vnd.google-apps.document":
        export_mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        entity = f"files/{file_id}/export"
        params = {"mimeType": export_mime_type}
    elif file_type == "application/vnd.google-apps.spreadsheet":
        export_mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        entity = f"files/{file_id}/export"
        params = {"mimeType": export_mime_type}
    else:
        params = {"alt": alt}
        entity = f"files/{file_id}"

    # Setting content to True by default to retrieve the file content as text.
    response = client.get_request(entity=entity, params=params, content=True)
    response_body, response_headers = response

    if isinstance(response_headers, dict) and response_headers.get("Content-Type") == "text/csv":
        text = response_body.encode("latin1").decode("utf-8")
        return FileContentGoogleDriveResult(content=text)
    else:
        return FileContentGoogleDriveResult(content=response_body)
