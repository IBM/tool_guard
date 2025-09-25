from typing import Any
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.zendesk.update_an_article import update_an_article


def test_update_an_article() -> None:
    """Verifies that the `update_an_article` tool can successfully update a Zendesk article."""

    # Define test data:
    test_data: dict[str, Any] = {
        "article_id": "48566308219545",
        "name": "customer FAQ",
        "position": "13",
        "label_names": ["pic", "tripod"],
        "section_id": "6951132346009",
        "permission_group_id": "4414652137241",
        "user_segment_id": "4412087522585",
        "promoted": False,
        "comments_disabled": True,
    }

    # Patch the Zendesk client
    with patch(
        "agent_ready_tools.tools.IT.zendesk.update_an_article.get_zendesk_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        # Define expected API response
        mock_client.put_request.return_value = {
            "article": {
                "id": test_data["article_id"],
                "name": test_data["name"],
                "position": test_data["position"],
                "label_names": test_data["label_names"],
                "section_id": test_data["section_id"],
                "permission_group_id": test_data["permission_group_id"],
                "user_segment_id": test_data["user_segment_id"],
                "promoted": test_data["promoted"],
                "comments_disabled": test_data["comments_disabled"],
            }
        }

        # Update an article
        response = update_an_article(
            article_id=test_data["article_id"],
            position=test_data["position"],
            label_names=test_data["label_names"],
            section_id=test_data["section_id"],
            permission_group_id=test_data["permission_group_id"],
            user_segment_id=test_data["user_segment_id"],
            promoted=test_data["promoted"],
            comments_disabled=test_data["comments_disabled"],
        )

        # Ensure that update_an_article() executed and returned proper values
        assert response
        assert response.article_id == test_data["article_id"]
        assert response.name == test_data["name"]
        assert response.position == test_data["position"]
        assert response.label_names == test_data["label_names"]
        assert response.section_id == test_data["section_id"]
        assert response.permission_group_id == test_data["permission_group_id"]
        assert response.user_segment_id == test_data["user_segment_id"]
        assert response.promoted == test_data["promoted"]
        assert response.comments_disabled == test_data["comments_disabled"]

        # Ensure API call was made with correct payload
        mock_client.put_request.assert_called_once_with(
            entity=f"help_center/articles/{test_data['article_id']}",
            payload={
                "article": {
                    "position": test_data["position"],
                    "label_names": test_data["label_names"],
                    "section_id": test_data["section_id"],
                    "permission_group_id": test_data["permission_group_id"],
                    "user_segment_id": test_data["user_segment_id"],
                    "promoted": test_data["promoted"],
                    "comments_disabled": test_data["comments_disabled"],
                }
            },
        )
