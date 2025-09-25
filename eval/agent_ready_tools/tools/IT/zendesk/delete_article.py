from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.zendesk_client import get_zendesk_client
from agent_ready_tools.utils.tool_credentials import ZENDESK_CONNECTIONS


@dataclass
class DeleteArticleResponse:
    """Represents the result of deleting an article in Zendesk."""

    http_code: int
    error_message: Optional[str] = None
    error_description: Optional[str] = None


@tool(expected_credentials=ZENDESK_CONNECTIONS)
def delete_article(
    article_id: str,
) -> DeleteArticleResponse:
    """
    Deletes an article in Zendesk.

    Args:
        article_id: The id of the article, returned by the `list_articles` tool.

    Returns:
        The result of performing the delete an article in Zendesk.
    """
    client = get_zendesk_client()

    try:
        response = client.delete_request(entity=f"help_center/articles/{article_id}")
        return DeleteArticleResponse(http_code=response.get("status_code", 500))
    except HTTPError as e:
        error_response = e.response.json()
        error_message = error_response.get("error", "404")
        error_description = error_response.get("description", "")
        return DeleteArticleResponse(
            http_code=e.response.status_code,
            error_message=error_message,
            error_description=error_description,
        )
    except Exception as e:  # pylint: disable=broad-except
        error_message = str(e)
        return DeleteArticleResponse(
            http_code=500,
            error_message=error_message,
            error_description="An unexpected error occurred.",
        )
