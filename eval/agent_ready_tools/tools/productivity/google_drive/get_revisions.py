from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.google_client import get_google_client
from agent_ready_tools.utils.tool_credentials import GOOGLE_CONNECTIONS


@dataclass
class Revisions:
    """Represents the revisions of a file in Google Drive."""

    revision_id: str
    mime_type: str
    kind: str
    modified_time: str


@dataclass
class RevisionsResponse:
    """A list of revisions of a file in Google Drive."""

    revisions: List[Revisions]


@tool(expected_credentials=GOOGLE_CONNECTIONS)
def get_revisions(file_id: str) -> RevisionsResponse:
    """
    Gets a list of revisions of a file in the Google Drive.

    Args:
        file_id: The id of the file, returned by the `get_files` tool.

    Returns:
        A list of revisions of a file from Google Drive.
    """

    client = get_google_client()
    response = client.get_request(entity=f"files/{file_id}/revisions")
    revisions = [
        Revisions(
            revision_id=result.get("id", ""),
            mime_type=result.get("mimeType", ""),
            kind=result.get("kind", ""),
            modified_time=result.get("modifiedTime", ""),
        )
        for result in response.get("revisions", [])
    ]
    return RevisionsResponse(revisions=revisions)
