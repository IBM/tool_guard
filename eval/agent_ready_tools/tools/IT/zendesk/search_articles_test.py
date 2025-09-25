from typing import Any
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.zendesk.search_articles import (
    Article,
    SearchArticlesResponse,
    search_articles,
)


def test_search_articles() -> None:
    """Tests that the `search_articles` function returns expected article data."""

    # Define test data
    test_query = "software"
    test_article_data: dict[str, Any] = {
        "id": "48445105656729",
        "title": "Software Installation Guide",
        "body": "getting started for installation",
        "position": "0",
        "section_id": "6951132346009",
        "permission_group_id": "4414652137241",
        "user_segment_id": "6319581504793",
        "promoted": False,
        "comments_disabled": False,
    }
    # Inputs and expected pagination values
    per_page = 5
    page = 1
    output_page = 1
    output_per_page = 5

    with patch(
        "agent_ready_tools.tools.IT.zendesk.search_articles.get_zendesk_client"
    ) as mock_get_client:
        # Setup mock client and response
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "results": [test_article_data],
            "next_page": "https://d3v-ibmappconn.zendesk.com/api/v2/help_center/articles/search.json?page=1&per_page=5&query=software",
        }

        # Patch pagination helper if needed
        with patch(
            "agent_ready_tools.utils.get_id_from_links.get_query_param_from_links"
        ) as mock_get_query_params:
            mock_get_query_params.return_value = {
                "page": str(output_page),
                "per_page": str(output_per_page),
            }

        # Call the function
        response = search_articles(query=test_query, per_page=per_page, page=page)

        # Expected article
        expected_article = Article(
            article_id=test_article_data["id"],
            title=test_article_data["title"],
            body=test_article_data["body"],
            position=test_article_data["position"],
            section_id=test_article_data["section_id"],
            permission_group_id=test_article_data["permission_group_id"],
            user_segment_id=test_article_data["user_segment_id"],
            promoted=test_article_data["promoted"],
            comments_disabled=test_article_data["comments_disabled"],
        )

        # Assertions
        assert response == SearchArticlesResponse(
            articles=[expected_article], page=output_page, per_page=output_per_page
        )

        # Assert correct API call
        mock_client.get_request.assert_called_once_with(
            entity="help_center/articles/search",
            params={"query": test_query, "per_page": per_page, "page": page},
        )
