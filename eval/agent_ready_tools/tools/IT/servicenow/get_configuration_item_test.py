from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.get_configuration_item import get_configuration_item


def test_get_configuration_item() -> None:
    """Test that the `get_configuration_item` function returns the expected response."""

    # Define test data:
    test_data = {
        "name": "eCAB Approval",
        "id": "A53 Series",
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.get_configuration_item.get_servicenow_client"
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

        # Get configuration item
        response = get_configuration_item(system_id=test_data["id"])

        # Ensure that get_article_types() executed and returned proper values
        assert response
        assert len(response.configuration_items)
        assert response.configuration_items[0].system_id == test_data["id"]
        assert response.configuration_items[0].configuration_item_name == test_data["name"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="cmdb_ci", params={"sys_id": test_data["id"]}
        )
