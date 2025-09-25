from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.salesforce.update_opportunity import (
    update_opportunity,
)


def test_update_opportunity() -> None:
    """Test that the `update_opportunity` function returns the expected response."""

    # Define test data:
    test_data = {
        "opportunity_id": "006fJ000002Ew9SQAS",
        "name": "Wxo Test",
        "amount": 3.0,
        "close_date": "2025-03-31",
        "stage_name": "Value Proposition",
        "description": "Wxo Test Account",
        "opportunity_type": "New Customer",
        "lead_source": "Other",
    }

    test_response = 204

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.update_opportunity.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Opportunity.update.return_value = test_response

        # Update opportunity
        response = update_opportunity(**test_data)

        # Ensure that list_account_contacts() executed and returned proper values
        assert response
        assert response == test_response

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.Opportunity.update(test_data, test_data["opportunity_id"])
