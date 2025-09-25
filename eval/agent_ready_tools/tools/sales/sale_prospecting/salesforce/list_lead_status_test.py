from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.salesforce.list_lead_status import (
    list_lead_status,
)
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import (
    LeadStatus,
    PickListOptionsPair,
)


def test_list_lead_status() -> None:
    """Tests that the `list_lead_status` function returns the expected response."""

    # Define test data:
    test_data = {
        "lead_status": "Government",
    }

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.list_lead_status.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.get_picklist_options.return_value = {
            "values": [{"value": test_data["lead_status"]}]
        }

        # List lead status
        response = list_lead_status()

        expected = LeadStatus(lead_status=test_data["lead_status"])

        # Assert the expected and actual response
        assert response
        assert response[0] == expected

        # Ensure the API call was made with expected parameters
        mock_client.get_picklist_options.assert_called_once_with(
            PickListOptionsPair.LeadStatus.obj_api_name,
            PickListOptionsPair.LeadStatus.field_api_name,
        )
