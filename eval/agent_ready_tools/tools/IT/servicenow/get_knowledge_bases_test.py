from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.get_knowledge_bases import get_knowledge_bases


def test_get_knowledge_bases() -> None:
    """Test that the `get_knowledge_bases` function returns the expected response."""

    # Define test data:
    test_data = {
        "title": "IT",
        "id": "a7e8a78bff0221009b20ffffffffff17",
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.get_knowledge_bases.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "result": [
                {
                    "sys_id": test_data["id"],
                    "title": test_data["title"],
                },
            ],
        }

        # Get knowledge bases
        response = get_knowledge_bases()

        # Ensure that get_knowledge_bases() executed and returned proper values
        assert response
        assert len(response.knowledge_bases)
        assert response.knowledge_bases[0].system_id == test_data["id"]
        assert response.knowledge_bases[0].knowledge_base == test_data["title"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(entity="kb_knowledge_base", params={})
