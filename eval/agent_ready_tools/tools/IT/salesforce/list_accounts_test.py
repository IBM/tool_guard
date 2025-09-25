from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.list_accounts import list_accounts
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import Account


def test_list_accounts() -> None:
    """Test that the `list_accounts` function returns the expected response."""
    test_data = [
        Account(id="001fJ00000223nBQAQ", name="United Oil & Gas Corp.", industry="Energy"),
        Account(id="001fJ00001wHRQAQA4", name="Best Eats", industry="Energy"),
    ]

    expected: list[Account] = test_data
    with patch(
        "agent_ready_tools.tools.IT.salesforce.list_accounts.get_salesforce_client"
    ) as mock_salesforce_client:
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.query_all_iter.return_value = [
            {"Id": test_data[0].id, "Name": test_data[0].name, "Industry": test_data[0].industry},
            {"Id": test_data[1].id, "Name": test_data[1].name, "Industry": test_data[1].industry},
        ]

        response = list_accounts(
            "NumberOfEmployees<200000 AND (BillingState=NY OR BillingState=CA) AND Industry=Energy"
        )

        assert response == expected

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.query_all_iter.assert_called_once_with(
            "SELECT Id, Name, Industry FROM Account WHERE NumberOfEmployees < 200000 AND (BillingState = 'NY' OR BillingState = 'CA') AND Industry = 'Energy'"
        )
