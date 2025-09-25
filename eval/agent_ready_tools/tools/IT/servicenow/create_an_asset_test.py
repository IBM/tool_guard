from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.create_an_asset import create_an_asset


def test_create_an_asset() -> None:
    """Test that the `create_an_asset` function returns the expected response."""

    # Define test data:
    test_data = {
        "asset_type": "Software License",
        "model_category": "Computer",
        "model": "Asus A53 Series",
        "asset_tag": "P1000490",
        "quantity": "1",
        "configuration_item_system_id": "82061af2c0a8018b381a7bc2a212784e",
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.create_an_asset.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "result": {
                "display_name": test_data["model"],
            }
        }

        # Create an asset
        response = create_an_asset(
            asset_type=test_data["asset_type"],
            model_category=test_data["model_category"],
            model=test_data["model"],
            asset_tag=test_data["asset_tag"],
            quantity=test_data["quantity"],
            configuration_item_system_id=test_data["configuration_item_system_id"],
        )

        # Ensure that create_an_asset() executed and returned proper values
        assert response
        assert response.display_name == test_data["model"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="alm_asset",
            payload={
                "sys_class_name": test_data["asset_type"],
                "model_category": test_data["model_category"],
                "model": test_data["model"],
                "asset_tag": test_data["asset_tag"],
                "quantity": test_data["quantity"],
                "ci": test_data["configuration_item_system_id"],
            },
        )
