from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.salesforce.update_asset import update_asset


def test_update_asset() -> None:
    """Tests that the `update_asset` function returns the expected response in Salesforce."""

    # Define test data:
    test_data = {
        "asset_id": "03kgL0085300ix7QBG",
        "asset_name": "Test Asset 1",
        "asset_description": "Test Asset desc - 1",
        "asset_status": "Purchased",
        "account_id": "001g0870012Xy3JFE",
        "contact_id": "003g054012Xy3ALGE",
        "asset_amount": 1070,
        "asset_quantity": 10,
    }

    # Define the expected response
    test_response = 204

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.update_asset.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Asset.update.return_value = test_response

        # Call the update an asset function
        response = update_asset(**test_data)

        # Ensure that update_asset() executed and returned proper values
        assert response
        assert response == test_response

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.Asset.update(test_data["asset_id"], test_data)
