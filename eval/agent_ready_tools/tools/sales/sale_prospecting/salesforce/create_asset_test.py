from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.salesforce.create_asset import (
    CreateAssetResponse,
    create_asset,
)


def test_create_an_account() -> None:
    """Tests that the `create_asset` function returns the expected response."""

    # Define test data
    test_data = {
        "account_id": "001gL000004Zin4QAC",
        "contact_id": "003gL000002CLU9QAO",
        "asset_name": "Test Asset YS 06",
        "asset_amount": 600,
        "asset_status": "Registered",
        "asset_quantity": 4,
        "asset_description": "Test Hello World 001",
    }

    asset_id = "02igL0000000LyvQAE"

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.create_asset.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Asset.create.return_value = {"id": asset_id}

        # Create Asset
        response = create_asset(**test_data)

        expected = CreateAssetResponse(asset_id=asset_id)

        # Assert the expected and actual response
        assert response
        assert expected.asset_id is not None

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.Asset.create(
            {
                "AccountId": test_data["account_id"],
                "ContactId": test_data["contact_id"],
                "Name": test_data["asset_name"],
                "Price": test_data["asset_amount"],
                "Status": test_data["asset_status"],
                "Quantity": test_data["asset_quantity"],
                "Description": test_data["asset_description"],
            }
        )
