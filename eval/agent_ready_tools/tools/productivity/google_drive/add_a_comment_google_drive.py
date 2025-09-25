from typing import Any, Dict

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.google_client import get_google_client
from agent_ready_tools.utils.tool_credentials import GOOGLE_CONNECTIONS


@dataclass
class AddACommentResponse:
    """Represents the result of adding a comment to a file in Google Drive."""

    content: str


@tool(expected_credentials=GOOGLE_CONNECTIONS)
def add_a_comment_google_drive(file_id: str, content: str) -> AddACommentResponse:
    """
    Adds a comment to a specified file in Google Drive.

    Args:
        file_id: Unique identifier for a file in Google Drive returned by `get_files` tool.
        content: The text of the comment.

    Returns:
        The content of the added comment.
    """
    client = get_google_client()

    params: Dict[str, Any] = {
        "fields": "*",
    }
    payload: Dict[str, Any] = {"name": file_id, "content": content}

    response = client.post_request(
        entity=f"files/{file_id}/comments", payload=payload, params=params
    )

    return AddACommentResponse(content=response.get("content", ""))
