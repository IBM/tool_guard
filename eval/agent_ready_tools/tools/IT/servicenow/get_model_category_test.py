from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.get_model_category import get_model_category


def test_get_model_category() -> None:
    """Test that model categories can be retrieved successfully."""

    # Define test data:
    test_data = {
        "name": "Communication Hardware",
        "id": "8c4cfdfb77b1a110da1f99f69c5a99d3",
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.get_model_category.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "result": [
                {
                    "sys_id": test_data["id"],
                    "name": test_data["name"],
                },
            ],
        }

        # Get device model categories
        response = get_model_category()

        # Ensure that get_model_category() executed and returned proper values
        assert response
        assert len(response.categories)
        assert response.categories[0].system_id == test_data["id"]
        assert response.categories[0].name == test_data["name"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(entity="cmdb_model_category", params={})
