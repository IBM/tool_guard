from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.zendesk_client import get_zendesk_client
from agent_ready_tools.tools.IT.zendesk.zendesk_utility import get_name_by_id
from agent_ready_tools.utils.get_id_from_links import get_query_param_from_links
from agent_ready_tools.utils.tool_credentials import ZENDESK_CONNECTIONS


@dataclass
class Comment:
    """Represents a comment in Zendesk."""

    comment_id: str
    comment: str
    created_at: str
    author_name: Optional[str] = None
    file_name: Optional[str] = None
    content_url: Optional[str] = None
    content_type: Optional[str] = None
    page: Optional[int] = None
    per_page: Optional[int] = None


@dataclass
class GetCommentsResponse:
    """Represents the response for retrieving comments in Zendesk."""

    comments: List[Comment]
    page: Optional[int]
    per_page: Optional[int]
    http_code: Optional[int] = None
    error_message: Optional[str] = None
    error_description: Optional[str] = None


@tool(expected_credentials=ZENDESK_CONNECTIONS)
def get_ticket_comments(
    ticket_id: str, per_page: Optional[int] = 10, page: Optional[int] = 1
) -> GetCommentsResponse:
    """
    Retreives the list of comments in a specific ticket from Zendesk.

    Args:
        ticket_id: The ID of the ticket to retrieve comments, returned by `zendesk_get_tickets` tool.
        per_page: Number of comments to retrieve per page. Defaults to 10.
        page: Page number to retrieve. Defaults to 1.

    Returns:
        List of comments.
    """
    try:
        client = get_zendesk_client()
        params = {"per_page": per_page, "page": page, "include": "users"}

        params = {key: value for key, value in params.items() if value is not None}
        response = client.get_request(entity=f"tickets/{ticket_id}/comments", params=params)
        comments: List[Comment] = [
            Comment(
                comment_id=str(comment.get("id", "")),
                author_name=(
                    get_name_by_id(response.get("users", []), comment.get("author_id"))
                    if comment.get("author_id")
                    else None
                ),
                comment=comment.get("body", ""),
                created_at=comment.get("created_at", ""),
                file_name=(
                    comment["attachments"][0].get("file_name", "")
                    if comment.get("attachments")
                    else None
                ),
                content_url=(
                    comment["attachments"][0].get("content_url", "")
                    if comment.get("attachments")
                    else None
                ),
                content_type=(
                    comment["attachments"][0].get("content_type", "")
                    if comment.get("attachments")
                    else None
                ),
            )
            for comment in response.get("comments", [])
        ]

        # Extract page and per_page from next_page if it exists
        output_page = None
        output_per_page = None
        next_api_link = response.get("next_page")
        if next_api_link is not None:
            query_params = get_query_param_from_links(next_api_link)
            output_page = int(query_params["page"]) if "page" in query_params else None
            output_per_page = int(query_params["per_page"]) if "per_page" in query_params else None

        return GetCommentsResponse(
            comments=comments,
            page=output_page,
            per_page=output_per_page,
        )
    except HTTPError as e:
        error_response = e.response.json() if e.response is not None else None
        error_message = (
            error_response.get("error", {}).get("message", "")
            if error_response
            else "An unexpected error occurred."
        )
        return GetCommentsResponse(
            comments=[],  # Provide default empty list
            page=None,
            per_page=None,
            http_code=e.response.status_code,
            error_message=error_message,
        )
    except Exception as e:  # pylint: disable=broad-except
        return GetCommentsResponse(
            comments=[],  # Provide default empty list
            page=None,
            per_page=None,
            http_code=500,
            error_message=str(e),
        )
