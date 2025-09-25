from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.salesforce.list_orders import list_orders
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import Order


def test_list_orders() -> None:
    """Tests that the `list_orders` function returns the expected response."""

    # Define test data
    test_data = {
        "id": "801gL000004j6esQAA",
        "order_number": "00000101",
        "order_amount": 40000.0,
        "effective_date": "2025-04-24",
        "status": "Activated",
        "account_id": "800gL000003nTqLQAU",
        "contract_id": "1000067",
    }

    expected = Order(**test_data)  # type: ignore[arg-type]

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.list_orders.get_salesforce_client"
    ) as mock_salesforce_client:
        # Set up the mock Salesforce client and its response
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.query_all_iter.return_value = [
            {
                "Id": test_data["id"],
                "Status": test_data["status"],
                "EffectiveDate": test_data["effective_date"],
                "AccountId": test_data["account_id"],
                "ContractId": test_data["contract_id"],
                "OrderNumber": test_data["order_number"],
                "TotalAmount": test_data["order_amount"],
            }
        ]

        # Call the tool function with a mock search clause
        response = list_orders(
            "AccountId = '001gL000004Zin4QAC' AND Status = 'Activated' AND EffectiveDate = 2025-04-24"
        )

        # Assert the output matches the expected result
        assert response[0] == expected

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.query_all_iter.assert_called_once_with(
            "SELECT Id, Status, EffectiveDate, AccountId, ContractId, OrderNumber, TotalAmount FROM Order WHERE AccountId = '001gL000004Zin4QAC' AND Status = 'Activated' AND EffectiveDate = '2025-04-24'"
        )
