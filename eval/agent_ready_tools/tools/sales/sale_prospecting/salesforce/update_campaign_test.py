from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.salesforce.update_campaign import (
    update_campaign,
)


def test_update_campaign() -> None:
    """Tests that the `update_campaign` function returns the expected response."""

    # Define test data:
    test_data = {
        "campaign_id": "006fJ000002Ew9SQAS",
        "campaign_name": "Wxo Test",
        "campaign_description": 3.0,
        "campaign_is_active": "2025-03-31",
        "campaign_type": "Value Proposition",
        "campaign_status": "Wxo Test Account",
        "campaign_start_date": "New Customer",
        "campaign_end_date": "Other",
        "campaign_expected_revenue": 500,
        "campaign_budgeted_cost": 5000,
        "campaign_actual_cost": 68820,
        "campaign_expected_response": 7500,
        "campaign_number_sent": 5600,
        "parent_campaign_id": "006fJ000002Ew9SQAA",
    }

    test_response = 204

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.update_campaign.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Campaign.update.return_value = test_response

        # Update Campaign
        response = update_campaign(**test_data)

        # Ensure that update_campaign() executed and returned proper values
        assert response
        assert response == test_response

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.Campaign.update(test_data, test_data["campaign_id"])
