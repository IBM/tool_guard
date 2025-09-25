from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.get_knowledge_topics import get_knowledge_topics


def test_get_knowledge_topic() -> None:
    """Test that the `get_knowledge_topic` function returns the expected response."""

    # Define test data:
    test_data = {
        "label": "Generative AI",
        "value": "b97e89b94a36231201676b73322a0311",
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.get_knowledge_topics.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "result": [
                {
                    "value": test_data["value"],
                    "label": test_data["label"],
                },
            ],
        }

        # Get knowledge topics
        response = get_knowledge_topics()

        # Ensure that get_knowledge_topics() executed and returned proper values
        assert response
        assert len(response.knowledge_topic)
        assert response.knowledge_topic[0].topic_value == test_data["value"]
        assert response.knowledge_topic[0].topic == test_data["label"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="sys_choice", params={"name": "kb_knowledge", "element": "topic"}
        )
