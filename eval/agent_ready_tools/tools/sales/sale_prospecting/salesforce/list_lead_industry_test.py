from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.salesforce.list_lead_industry import (
    list_lead_industry,
)
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import (
    LeadIndustry,
    PickListOptionsPair,
)


def test_list_lead_industry() -> None:
    """Tests that the `list_lead_industry` function returns the expected response."""

    # Define test data:
    test_data = {
        "lead_industry": "Government",
    }

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.list_lead_industry.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.get_picklist_options.return_value = {
            "values": [{"value": test_data["lead_industry"]}]
        }

        # List lead industry
        response = list_lead_industry()

        expected = LeadIndustry(lead_industry=test_data["lead_industry"])

        # Assert the expected and actual response
        assert response
        assert response[0] == expected

        # Ensure the API call was made with expected parameters
        mock_client.get_picklist_options.assert_called_once_with(
            PickListOptionsPair.LeadIndustry.obj_api_name,
            PickListOptionsPair.LeadIndustry.field_api_name,
        )
