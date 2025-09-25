from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.salesforce.list_opportunities import (
    list_opportunities,
)
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import Opportunity


def test_list_opportunities() -> None:
    """Test that the `list_opportunities` function returns the expected response."""

    # Define test data:
    test_data = {
        "id": "006fJ000000JarNQAS",
        "account_id": "001fJ00000223nBQAQ",
        "name": "United Oil Refinery Generators",
        "amount": 270000,
        "close_date": "2022-11-11",
        "stage_name": "Proposal/Price Quote",
        "description": "",
        "opportunity_type": "Existing Customer - Upgrade",
        "lead_source": "",
        "probability": 75,
        "age_in_days": 1,
        "additional_data": None,
    }

    expected = Opportunity(**test_data)  # type: ignore[arg-type]

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.list_opportunities.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.query_all_iter.return_value = [
            {
                "Id": test_data["id"],
                "AccountId": test_data["account_id"],
                "Name": test_data["name"],
                "Amount": test_data["amount"],
                "CloseDate": test_data["close_date"],
                "StageName": test_data["stage_name"],
                "Description": test_data["description"],
                "Type": test_data["opportunity_type"],
                "LeadSource": test_data["lead_source"],
                "Probability": test_data["probability"],
                "AgeInDays": test_data["age_in_days"],
            }
        ]

        # List all opportunities
        response = list_opportunities(
            search="Probability<100 AND Amount<3000 AND Name=United Oil Refinery Generators"
        )

        # Ensure that list_opportunities() executed and returned proper values
        assert response[0] == expected
