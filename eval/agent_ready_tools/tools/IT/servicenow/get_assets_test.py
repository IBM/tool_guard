from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.servicenow.get_assets import get_assets


def test_get_assets() -> None:
    """Test that assets can be retrieved successfully."""

    # Define test data:
    test_data = {
        "model": "d501454f1b1310002502fbcd2c071334",
        "model_category": "81feb9c137101000deeabfc8bcbe5dc4",
        "invoice_number": "",
        "asset_tag": "P1000479",
        "owned_by": "",
        "display_name": 'P1000479 - Apple MacBook Pro 15"',
        "delivery_date": "2022-07-22 07:00:00",
        "purchase_date": "2022-07-11",
        "sys_id": "00a96c0d3790200044e0bfc8bcbe5dc3",
        "assigned_to_user": "Miranda Hammitt",
        "quantity": "1",
        "serial_number": "BQP-854-D33246-GH",
        "comments": "Hello World!!!",
        "limit": 20,
    }

    # Patch `get_servicenow_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.servicenow.get_assets.get_servicenow_client"
    ) as mock_servicenow_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_servicenow_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "result": [
                {
                    "model": test_data["model"],
                    "model_category": test_data["model_category"],
                    "invoice_number": test_data["invoice_number"],
                    "asset_tag": test_data["asset_tag"],
                    "owned_by": test_data["owned_by"],
                    "display_name": test_data["display_name"],
                    "delivery_date": test_data["delivery_date"],
                    "purchase_date": test_data["purchase_date"],
                    "sys_id": test_data["sys_id"],
                    "assigned_to": test_data["assigned_to_user"],
                    "quantity": test_data["quantity"],
                    "serial_number": test_data["serial_number"],
                    "comments": test_data["comments"],
                },
            ],
        }

        # Get assets
        response = get_assets(
            model_name_system_id=test_data["model"], serial_number=test_data["serial_number"]
        )

        # Ensure that get_assets() executed and returned proper values
        assert response
        assert len(response.assets)
        assert response.assets[0].model == test_data["model"]
        assert response.assets[0].model_category == test_data["model_category"]
        assert response.assets[0].invoice_number == test_data["invoice_number"]
        assert response.assets[0].asset_tag == test_data["asset_tag"]
        assert response.assets[0].owned_by == test_data["owned_by"]
        assert response.assets[0].display_name == test_data["display_name"]
        assert response.assets[0].delivery_date == test_data["delivery_date"]
        assert response.assets[0].purchase_date == test_data["purchase_date"]
        assert response.assets[0].system_id == test_data["sys_id"]
        assert response.assets[0].assigned_to_user == test_data["assigned_to_user"]
        assert response.assets[0].quantity == test_data["quantity"]
        assert response.assets[0].serial_number == test_data["serial_number"]
        assert response.assets[0].comments == test_data["comments"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="alm_asset",
            params={
                "model": test_data["model"],
                "serial_number": test_data["serial_number"],
                "sysparm_limit": test_data["limit"],
                "sysparm_display_value": True,
            },
        )
