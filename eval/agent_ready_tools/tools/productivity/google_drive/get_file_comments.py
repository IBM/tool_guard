from typing import Any, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.google_client import get_google_client
from agent_ready_tools.utils.tool_credentials import GOOGLE_CONNECTIONS


@dataclass
class GetFileComment:
    """Represents the result of fetching a file's comment in Google Drive."""

    comment_id: str
    comment: str
    author_name: str
    created_datetime: str


@dataclass
class GetFileCommentsResponse:
    """Represents a list of comments of a file in Google Drive."""

    comments: List[GetFileComment]
    limit: Optional[int] = 10
    next_page_token: Optional[str] = None


@tool(expected_credentials=GOOGLE_CONNECTIONS)
def get_file_comments(
    file_id: str, limit: Optional[int] = 10, next_page_token: Optional[str] = None
) -> GetFileCommentsResponse:
    """
    Fetches a file's comments in Google Drive.

    Args:
        file_id: The id of the file in Google Drive returned by the `get_files` tool.
        limit: The maximum number of files retrieved in a single API call. Defaults to 10. Use this
            to control the size of the result set in Google Drive.
        next_page_token: A token used to skip a specific number of items for pagination purposes.
            Use this to retrieve subsequent pages of results when handling large datasets.

    Returns:
        A list of comments of a file.
    """

    client = get_google_client()

    endpoint = f"files/{file_id}/comments?fields=*"

    params: dict[str, Any] = {"pageSize": limit, "pageToken": next_page_token}

    response = client.get_request(entity=endpoint, params=params)

    comment: list[GetFileComment] = []
    comment = [
        GetFileComment(
            comment_id=item.get("id", ""),
            comment=item.get("content", ""),
            author_name=item.get("author", {}).get("displayName", ""),
            created_datetime=item.get("createdTime", ""),
        )
        for item in response["comments"]
    ]

    return GetFileCommentsResponse(
        comments=comment, limit=limit, next_page_token=response.get("nextPageToken", "")
    )
