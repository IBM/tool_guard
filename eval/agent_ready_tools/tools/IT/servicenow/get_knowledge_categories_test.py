from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.get_knowledge_categories import get_knowledge_categories


def test_get_knowledge_categories() -> None:
    """Test that the `get_knowledge_categories` function returns the expected response."""

    # Define test data:
    test_data = {
        "label": "Java",
        "id": "acba2d2047b002007f47563dbb9a71fc",
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.get_knowledge_categories.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "result": [
                {
                    "sys_id": test_data["id"],
                    "label": test_data["label"],
                },
            ],
        }

        # Get knowledge categories
        response = get_knowledge_categories()

        # Ensure that get_knowledge_categories() executed and returned proper values
        assert response
        assert len(response.categories)
        assert response.categories[0].system_id == test_data["id"]
        assert response.categories[0].category == test_data["label"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(entity="kb_category", params={})
