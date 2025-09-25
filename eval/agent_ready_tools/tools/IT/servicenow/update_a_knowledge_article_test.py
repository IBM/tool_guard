from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.update_a_knowledge_article import (
    update_a_knowledge_article,
)


def test_update_a_knowledge_article() -> None:
    """Test that the `update_a_knowledge_article` function returns the expected response."""

    # Define test data:
    test_data = {
        "knowledge_article_number_system_id": "e97ee81eff6002009b20ffffffffffe0",
        "short_description": "Eclipse configuration and setup",
        "text": "Hello this is for update a knowledge article",
        "knowledge_base": "IT",
        "topic": "General",
        "http_code": 200,
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.update_a_knowledge_article.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.patch_request.return_value = {"status_code": test_data["http_code"]}

        # Update knowledge article
        response = update_a_knowledge_article(
            knowledge_article_number_system_id=test_data["knowledge_article_number_system_id"],
            short_description=test_data["short_description"],
            knowledge_base=test_data["knowledge_base"],
            text=test_data["text"],
            topic=test_data["topic"],
        )

        # Ensure that update_a_knowledge_article() executed and returned proper values
        assert response
        assert response.http_code == 200

        # Ensure the API call was made with expected parameters
        mock_client.patch_request.assert_called_once_with(
            entity="kb_knowledge",
            entity_id=test_data["knowledge_article_number_system_id"],
            payload={
                "short_description": test_data["short_description"],
                "kb_knowledge_base": test_data["knowledge_base"],
                "text": test_data["text"],
                "topic": test_data["topic"],
            },
        )
