from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.salesforce.delete_an_asset import (
    delete_an_asset,
)


def test_delete_an_asset() -> None:
    """Tests that an asset can be deleted successfully by the `delete_an_asset` tool."""
    # Define test data:
    test_data = {"asset_id": "02igL0000000KYDQA2", "http_code": 204}

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.delete_an_asset.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Asset.delete.return_value = test_data["http_code"]

        # Call the function
        response = delete_an_asset(asset_id=test_data["asset_id"])

        # Ensure that the delete_an_asset() has been executed and returned the expected response
        assert response
        assert response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.Asset.delete(test_data["asset_id"])
