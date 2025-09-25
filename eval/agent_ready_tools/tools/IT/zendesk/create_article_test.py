from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.zendesk.create_article import create_article


def test_create_article() -> None:
    """Verifies that the `create_article` tool can successfully create an article in Zendesk."""

    # Define test data
    test_data = {
        "article_id": "48498282254233",
        "section_id": "6951132346009",
        "article_title": "Software Installation",
        "permission_group_id": "4414652137241",
        "user_segment_id": "6319581504793",
        "article_body": "getting started for installation",
    }

    # Patch `get_zendesk_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.zendesk.create_article.get_zendesk_client"
    ) as mock_zendesk_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_zendesk_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "article": {"id": test_data["article_id"], "title": test_data["article_title"]}
        }

        # Create an article
        response = create_article(
            section_id=test_data["section_id"],
            article_title=test_data["article_title"],
            permission_group_id=test_data["permission_group_id"],
            user_segment_id=test_data["user_segment_id"],
            article_body=test_data["article_body"],
        )

        # Ensure that create_aticle() has executed and returned proper values
        assert response
        assert response.article_id is not None
        assert response.article_title == test_data["article_title"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity=f"help_center/sections/{test_data["section_id"]}/articles",
            payload={
                "article": {
                    "title": test_data["article_title"],
                    "permission_group_id": test_data["permission_group_id"],
                    "user_segment_id": test_data["user_segment_id"],
                    "body": test_data["article_body"],
                }
            },
        )


def test_create_article_partial() -> None:
    """Verifies that the `create_article` tool can successfully create an article in Zendesk."""

    # Define test data
    test_data = {
        "article_id": "5353598787225",
        "section_id": "5223800429977",
        "article_title": "customer support",
        "permission_group_id": "4414652137241",
        "user_segment_id": "6319581504793",
        "article_body": None,
    }

    # Patch `get_zendesk_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.zendesk.create_article.get_zendesk_client"
    ) as mock_zendesk_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_zendesk_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "article": {"id": test_data["article_id"], "title": test_data["article_title"]}
        }

        # Create an article
        response = create_article(
            section_id=test_data["section_id"],
            article_title=test_data["article_title"],
            permission_group_id=test_data["permission_group_id"],
            user_segment_id=test_data["user_segment_id"],
        )

        # Ensure that create_article() has executed and returned proper values
        assert response
        assert response.article_id is not None
        assert response.article_title == test_data["article_title"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity=f"help_center/sections/{test_data["section_id"]}/articles",
            payload={
                "article": {
                    "title": test_data["article_title"],
                    "permission_group_id": test_data["permission_group_id"],
                    "user_segment_id": test_data["user_segment_id"],
                    "body": test_data["article_body"],
                }
            },
        )
