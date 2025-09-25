from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.get_knowledge_articles import get_knowledge_articles


def test_get_knowledge_articles() -> None:
    """Test that the `get_knowledge_articles` function returns the expected response."""

    # Define test data:
    test_data = {
        "id": "3ce8d1de83d82650e73115a6feaad33f",
        "number": "KB0010326",
        "short_description": "This is about creating knowledge article 13",
        "wiki": "Hello This is for create a knowledge article 13",
        "knowledge_base": "IT",
        "knowledge_category": "Policies",
        "valid_to": "2100-01-01",
        "topic": "General",
        "workflow_state": "draft",
        "sys_updated_on": "2025-03-17 13:20:22",
        "search": "number=KB0010326",
        "limit": 10,
        "skip": 0,
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.get_knowledge_articles.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "result": [
                {
                    "sys_id": test_data["id"],
                    "short_description": test_data["short_description"],
                    "wiki": test_data["wiki"],
                    "kb_knowledge_base": test_data["knowledge_base"],
                    "kb_category": test_data["knowledge_category"],
                    "knowledge_article_number": test_data["number"],
                    "valid_to": test_data["valid_to"],
                    "topic": test_data["topic"],
                    "workflow_state": test_data["workflow_state"],
                    "sys_updated_on": test_data["sys_updated_on"],
                },
            ],
        }

        # Get knowledge articles
        response = get_knowledge_articles(search=test_data["search"])

        # Ensure that get_knowledge_articles() executed and returned proper values
        assert response
        assert len(response.knowledge_articles)
        assert response.knowledge_articles[0].system_id == test_data["id"]
        assert response.knowledge_articles[0].short_description == test_data["short_description"]
        assert response.knowledge_articles[0].wiki == test_data["wiki"]
        assert response.knowledge_articles[0].knowledge_base == test_data["knowledge_base"]
        assert response.knowledge_articles[0].knowledge_category == test_data["knowledge_category"]
        assert response.knowledge_articles[0].topic == test_data["topic"]
        assert response.knowledge_articles[0].valid_to_date == test_data["valid_to"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="kb_knowledge",
            params={
                "sysparm_query": test_data["search"],
                "sysparm_limit": test_data["limit"],
                "sysparm_offset": test_data["skip"],
                "sysparm_display_value": True,
            },
        )
