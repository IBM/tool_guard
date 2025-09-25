from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.zendesk_client import get_zendesk_client
from agent_ready_tools.utils.get_id_from_links import get_query_param_from_links
from agent_ready_tools.utils.tool_credentials import ZENDESK_CONNECTIONS


@dataclass
class Article:
    """Represents an article from Zendesk Help Center."""

    article_id: str
    title: Optional[str] = None
    body: Optional[str] = None
    position: Optional[str] = None
    section_id: Optional[str] = None
    permission_group_id: Optional[str] = None
    user_segment_id: Optional[str] = None
    promoted: Optional[bool] = None
    comments_disabled: Optional[bool] = None


@dataclass
class SearchArticlesResponse:
    """Response containing articles matching the query."""

    articles: List[Article]
    page: Optional[int]
    per_page: Optional[int]


@tool(expected_credentials=ZENDESK_CONNECTIONS)
def search_articles(
    query: str, per_page: Optional[int] = 10, page: Optional[int] = 1
) -> SearchArticlesResponse:
    """
    Searches Zendesk Help Center articles by query.

    Args:
        query: The search term to look for in articles.
        per_page: Number of articles to retrieve per page. Defaults to 10.
        page: Page number to articles. Defaults to 1.

    Returns:
        A list of articles matching the query.
    """
    # Default to wildcard search if query is empty
    query = query or "*"

    client = get_zendesk_client()
    params = {
        "query": query,
        "per_page": per_page,
        "page": page,
    }
    response = client.get_request(entity="help_center/articles/search", params=params)

    articles = [
        Article(
            article_id=str(article.get("id", "")),
            title=article.get("title", ""),
            body=article.get("body", ""),
            position=str(article.get("position", "")),
            section_id=str(article.get("section_id", "")),
            permission_group_id=str(article.get("permission_group_id", "")),
            user_segment_id=str(article.get("user_segment_id", "")),
            promoted=article.get("promoted", False),
            comments_disabled=article.get("comments_disabled", True),
        )
        for article in response.get("results", [])
    ]

    # Extract page and per_page from next_page if it exists
    output_page = None
    output_per_page = None
    next_api_link = response.get("next_page", "")
    if next_api_link:
        query_params = get_query_param_from_links(next_api_link)
        output_page = int(query_params.get("page", 1))
        output_per_page = int(query_params.get("per_page", 10))

    return SearchArticlesResponse(
        articles=articles,
        page=output_page,
        per_page=output_per_page,
    )
