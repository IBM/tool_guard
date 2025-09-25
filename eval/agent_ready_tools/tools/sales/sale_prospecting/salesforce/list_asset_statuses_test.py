from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.salesforce.list_asset_statuses import (
    list_asset_statuses,
)
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import (
    AssetStatus,
    PickListOptionsPair,
)


def test_list_asset_statuses() -> None:
    """Tests that the `list_asset_statuses` function returns the expected response."""

    # Define test data:
    test_data = {"asset_status": "Shipped"}

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.list_asset_statuses.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.get_picklist_options.return_value = {
            "values": [{"value": test_data["asset_status"]}]
        }

        # Create Asset
        response = list_asset_statuses()

        expected = AssetStatus(asset_status=test_data["asset_status"])

        # Assert the expected and actual response
        assert response
        assert response[0] == expected

        # Ensure the API call was made with expected parameters
        mock_client.get_picklist_options.assert_called_once_with(
            PickListOptionsPair.AssetStatus.obj_api_name,
            PickListOptionsPair.AssetStatus.field_api_name,
        )
