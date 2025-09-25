from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.delete_a_knowledge_article import (
    delete_a_knowledge_article,
)


def test_delete_a_knowledge_article() -> None:
    """Test that a knowledge article can be deleted successfully by the
    `delete_a_knowledge_article`tool."""
    # Define test data:
    test_data = {"id": "1100", "http_code": 201}

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.delete_a_knowledge_article.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.delete_request.return_value = test_data["http_code"]

        # Delete knowledge article
        response = delete_a_knowledge_article(knowledge_article_number_system_id=test_data["id"])

        # Ensure that delete_a_knowledge_article() executed and returned proper values
        assert response
        assert response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.delete_request.assert_called_once_with(
            entity="kb_knowledge", entity_id=test_data["id"]
        )
