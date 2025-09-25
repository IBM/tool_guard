from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.salesforce.list_campaign_type import (
    list_campaign_type,
)
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import (
    CampaignType,
    PickListOptionsPair,
)


def test_list_campaign_type() -> None:
    """Test that retrieves all the campaign types successfully by the `list_campaign_type` tool."""
    # Define test data:
    test_data = {
        "campaign_type": "Conference",
    }

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.list_campaign_type.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.get_picklist_options.return_value = {
            "values": [{"value": test_data["campaign_type"]}]
        }

        # Get campaign types
        response = list_campaign_type()

        expected = CampaignType(campaign_type=test_data["campaign_type"])

        # Assert the expected and actual response
        assert response
        assert response[0] == expected

        # Ensure the API call was made with expected parameters
        mock_client.get_picklist_options.assert_called_once_with(
            PickListOptionsPair.CampaignStatus.obj_api_name,
            PickListOptionsPair.CampaignStatus.field_api_name,
        )
