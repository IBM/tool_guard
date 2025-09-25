from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.create_a_knowledge_article import (
    create_a_knowledge_article,
)


def test_create_a_knowledge_article() -> None:
    """Verify that the `create_a_knowledge_article` tool can successfully create a knowledge article
    in ServiceNow."""

    # Define test data:
    test_data = {
        "short_description": "This is about creating knowledge article 17",
        "knowledge_base": "IT",
        "article_type": None,
        "text": "Hello This is for create a knowledge article 17",
        "wiki": None,
        "description": "This is a basic description for creating knowledge article 17.",
        "workflow_state": "draft",
        "topic": "General",
        "knowledge_category": "FAQ",
        "knowledge_article_number": 256,
        "http_code": 201,
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.create_a_knowledge_article.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "result": {
                "number": test_data["knowledge_article_number"],
                "short_description": test_data["short_description"],
                "status_code": test_data["http_code"],
            },
            "status_code": test_data["http_code"],
        }

        # Create knowledge article
        response = create_a_knowledge_article(
            short_description=test_data["short_description"],
            knowledge_base=test_data["knowledge_base"],
            article_type=test_data["article_type"],
            text=test_data["text"],
            wiki=test_data["wiki"],
            knowledge_category=test_data["knowledge_category"],
            description=test_data["description"],
            workflow_state=test_data["workflow_state"],
            topic=test_data["topic"],
        )

        # Ensure that create_a_knowledge_article() executed and returned proper values
        assert response.knowledge_article_number == test_data["knowledge_article_number"]
        assert response.short_description == test_data["short_description"]
        assert response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="kb_knowledge",
            payload={
                "short_description": test_data["short_description"],
                "kb_knowledge_base": test_data["knowledge_base"],
                "text": test_data["text"],
                "description": test_data["description"],
                "kb_category": test_data["knowledge_category"],
                "workflow_state": test_data["workflow_state"],
                "topic": test_data["topic"],
            },
        )
