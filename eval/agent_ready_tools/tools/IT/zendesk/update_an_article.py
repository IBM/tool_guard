from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.zendesk_client import get_zendesk_client
from agent_ready_tools.utils.tool_credentials import ZENDESK_CONNECTIONS


@dataclass
class UpdateArticleResponse:
    """Represents the result of updating an article in Zendesk."""

    article_id: Optional[str] = None
    name: Optional[str] = None
    position: Optional[str] = None
    label_names: Optional[List[str]] = None
    section_id: Optional[str] = None
    permission_group_id: Optional[str] = None
    user_segment_id: Optional[str] = None
    promoted: Optional[bool] = None
    comments_disabled: Optional[bool] = None
    error_message: Optional[str] = None
    error_description: Optional[str] = None
    http_code: Optional[int] = None


@tool(expected_credentials=ZENDESK_CONNECTIONS)
def update_an_article(
    article_id: str,
    position: Optional[str] = None,
    label_names: Optional[List[str]] = None,
    section_id: Optional[str] = None,
    permission_group_id: Optional[str] = None,
    user_segment_id: Optional[str] = None,
    promoted: Optional[bool] = None,
    comments_disabled: Optional[bool] = None,
) -> UpdateArticleResponse:
    """
    Updates an article in Zendesk.

    Args:
        article_id: The article_id uniquely identifying them within the Zendesk API, returned by `search_articles` tool.
        position: The position of the article to update.
        label_names: The list of labels of the article to update.
        section_id: The id of the section in Zendesk API, returned by `list_sections` tool.
        permission_group_id: The id of the permission group in Zendesk API, returned by `list_permission_groups` tool.
        user_segment_id: The id of the user segment in Zendesk API, returned by `list_user_segments` tool.
        promoted: The article promoted status to be updated.
        comments_disabled: The article comments disabled status to be updated.

    Returns:
        Result of performing update operation on an article.
    """
    try:

        client = get_zendesk_client()

        # Ensure label_names is a list of strings if provided
        if label_names is not None and not isinstance(label_names, list):
            raise ValueError("label_names must be a list of strings")

        payload = {
            "position": position,
            "label_names": label_names,
            "section_id": section_id,
            "permission_group_id": permission_group_id,
            "user_segment_id": user_segment_id,
            "promoted": promoted,
            "comments_disabled": comments_disabled,
        }

        # Filter out None or blank values
        payload = {key: value for key, value in payload.items() if value is not None}

        response = client.put_request(
            entity=f"help_center/articles/{article_id}", payload={"article": payload}
        )

        article_data = response.get("article", {})

        return UpdateArticleResponse(
            article_id=str(article_data.get("id", "")),
            name=article_data.get("name", ""),
            position=str(article_data.get("position", "")),
            label_names=article_data.get("label_names", []),
            section_id=str(article_data.get("section_id", "")),
            permission_group_id=str(article_data.get("permission_group_id", "")),
            user_segment_id=str(article_data.get("user_segment_id", "")),
            promoted=article_data.get("promoted", False),
            comments_disabled=article_data.get("comments_disabled", True),
        )

    except HTTPError as e:
        error_response = e.response.json()
        http_code = e.response.status_code
        if http_code == 400:
            error_message = error_response.get("error", {}).get("title", "")
            error_description = error_response.get("error", {}).get("message", "")
        else:
            error_message = error_response.get("error", "")
            error_description = error_response.get("description", "")
        return UpdateArticleResponse(
            error_message=error_message,
            error_description=error_description,
            http_code=http_code,
        )

    except Exception as e:  # pylint: disable=broad-except
        error_message = str(e)
        return UpdateArticleResponse(
            error_message=error_message,
            error_description="An unexpected error occurred.",
        )
