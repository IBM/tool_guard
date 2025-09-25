from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.box_client import get_box_client
from agent_ready_tools.utils.tool_credentials import BOX_CONNECTIONS


@dataclass
class BoxComment:
    """Represents single comment object in Box."""

    comment: str
    comment_id: str
    created_by: str
    created_date: str


@dataclass
class CommentsResponse:
    """A response containing the list of comments from Box."""

    comments_list: list[BoxComment]


@tool(expected_credentials=BOX_CONNECTIONS)
def get_comments(file_id: str) -> CommentsResponse:
    """
    Gets a list of comments from Box.

    Args:
        file_id: The id of the file returned by the `get_file_details_by_name` tool.

    Returns:
        A list of comments records.
    """

    client = get_box_client()

    response = client.get_request(entity=f"files/{file_id}/comments")

    comments_list: list[BoxComment] = [
        BoxComment(
            comment=comment.get("message", ""),
            comment_id=comment.get("id", ""),
            created_by=comment.get("created_by", "").get("name", ""),
            created_date=comment.get("created_at", ""),
        )
        for comment in response.get("entries", [])
    ]

    return CommentsResponse(comments_list=comments_list)
