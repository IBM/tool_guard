from http import HTTPStatus
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.zendesk_client import get_zendesk_client
from agent_ready_tools.utils.tool_credentials import ZENDESK_CONNECTIONS


@dataclass
class CreateArticleResponse:
    """Represents the result of creating a article in Zendesk."""

    article_id: Optional[str] = None
    article_title: Optional[str] = None
    error_message: Optional[str] = None
    http_code: Optional[int] = None


@tool(
    expected_credentials=ZENDESK_CONNECTIONS,
)
def create_article(
    section_id: str,
    article_title: str,
    permission_group_id: str,
    user_segment_id: str,
    article_body: Optional[str] = None,
) -> CreateArticleResponse:
    """
    Creates a article in Zendesk.

    Args:
        section_id: The id of the section where this article will be created, as returned by the tool `list_sections` in Zendesk.
        article_title: The title of the article in Zendesk.
        permission_group_id: The id of the permission group which defines who can edit and publish this article, returned by the tool `list_permission_groups` in Zendesk.
        user_segment_id: The list of user segment ids which define who can view this article, returned by the tool `list_user_segments` in Zendesk.
        article_body: The body of a article in Zendesk.

    Returns:
        The result of performing the creation of a article in Zendesk.
    """
    try:
        client = get_zendesk_client()

        payload = {
            "article": {
                "title": article_title,
                "permission_group_id": permission_group_id,
                "user_segment_id": user_segment_id,
                "body": article_body,
            }
        }

        payload = {key: value for key, value in payload.items() if value}

        entity = f"help_center/sections/{section_id}/articles"
        response = client.post_request(entity=entity, payload=payload)
        article = response.get("article", {})
        return CreateArticleResponse(
            article_id=str(article.get("id", "")), article_title=article.get("title", "")
        )
    except HTTPError as e:
        error_response = e.response.json() if e.response is not None else {}
        message = (
            error_response.get("details", {}).get("name", [])[0].get("description", "")
            if error_response
            else "An unexpected error occurred."
        )
        return CreateArticleResponse(
            error_message=message,
            http_code=(
                e.response.status_code
                if e.response.status_code
                else HTTPStatus.INTERNAL_SERVER_ERROR.value
            ),
        )
    except Exception as e:  # pylint: disable=broad-except
        return CreateArticleResponse(
            http_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            error_message=str(e),
        )
