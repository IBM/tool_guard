from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import Account
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.list_accounts import (
    list_sales_accounts,
)


def test_list_accounts() -> None:
    """Test that the `list_accounts` function returns the expected response."""
    test_data = [
        Account(id="001fJ00000223nBQAQ", name="United Oil & Gas Corp.", industry="Energy"),
        Account(id="001fJ00001wHRQAQA4", name="Best Eats", industry="Energy"),
    ]

    expected: list[Account] = test_data
    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.list_accounts.get_salesforce_client"
    ) as mock_salesforce_client:
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.query_all_iter.return_value = [
            {"Id": test_data[0].id, "Name": test_data[0].name, "Industry": test_data[0].industry},
            {"Id": test_data[1].id, "Name": test_data[1].name, "Industry": test_data[1].industry},
        ]

        # uses FALLBACK_FIELDS for SELECT statement
        response = list_sales_accounts(
            search="NumberOfEmployees<200000 AND (BillingState=NY OR BillingState=CA) AND Industry=Energy"
        )

        assert response == expected

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.query_all_iter.assert_called_once_with(
            "SELECT Id, Industry, Name FROM Account WHERE NumberOfEmployees < 200000 AND (BillingState = 'NY' OR BillingState = 'CA') AND Industry = 'Energy'"
        )


def test_list_accounts_with_additional_fields() -> None:
    """Test that the `list_accounts` function returns the expected response."""
    test_data = [
        Account(
            id="001fJ00000223nBQAQ",
            name="United Oil & Gas Corp.",
            industry="Energy",
            additional_data={"BillingState": "CA"},
        ),
        Account(id="001fJ00001wHRQAQA4", name="Best Eats", industry="Energy"),
    ]

    expected: list[Account] = test_data
    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.list_accounts.get_salesforce_client"
    ) as mock_salesforce_client:
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.query_all_iter.return_value = [
            {
                "Id": test_data[0].id,
                "Name": test_data[0].name,
                "Industry": test_data[0].industry,
                "BillingState": "CA",
            },
            {"Id": test_data[1].id, "Name": test_data[1].name, "Industry": test_data[1].industry},
        ]

        response = list_sales_accounts(
            optional_fields="BillingState",
            use_optional_fields=True,
            search="NumberOfEmployees<200000 AND (BillingState=NY OR BillingState=CA) AND Industry=Energy",
        )

        assert response == expected

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.query_all_iter.assert_called_once_with(
            "SELECT BillingState, Id, Industry, Name FROM Account WHERE NumberOfEmployees < 200000 AND (BillingState = 'NY' OR BillingState = 'CA') AND Industry = 'Energy'"
        )
