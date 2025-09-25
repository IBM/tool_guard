from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.update_an_asset import update_an_asset


def test_update_an_asset() -> None:
    """Test that asset can be updated successfully by the `update_an_asset` tool."""

    # Define test data:
    test_data = {
        "system_id": "aab104dd8394ee10e73115a6feaad36b",
        "assigned_to_user_system_id": "5a64c48783c02610e73115a6feaad3c0",
        "cost": "1000.00",
        "quantity": "1",
        "due_in": "1 Hour",
        "install_status": "In use",
        "disposal_reason": "not working",
        "purchase_date": "2025-03-25",
        "http_code": 200,
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.update_an_asset.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.patch_request.return_value = {"status_code": test_data["http_code"]}

        # Update an asset
        response = update_an_asset(
            system_id=test_data["system_id"],
            assigned_to_user_system_id=test_data["assigned_to_user_system_id"],
            cost=test_data["cost"],
            quantity=test_data["quantity"],
            due_in=test_data["due_in"],
            install_status=test_data["install_status"],
            disposal_reason=test_data["disposal_reason"],
            purchase_date=test_data["purchase_date"],
        )

        # Ensure that update_an_asset() executed and returned proper values
        assert response
        assert response.http_code == 200

        # Ensure the API call was made with expected parameters
        mock_client.patch_request.assert_called_once_with(
            entity="alm_asset",
            entity_id=test_data["system_id"],
            payload={
                "assigned_to": test_data["assigned_to_user_system_id"],
                "cost": test_data["cost"],
                "quantity": test_data["quantity"],
                "due_in": test_data["due_in"],
                "disposal_reason": test_data["disposal_reason"],
                "install_status": test_data["install_status"],
                "purchase_date": test_data["purchase_date"],
            },
        )
