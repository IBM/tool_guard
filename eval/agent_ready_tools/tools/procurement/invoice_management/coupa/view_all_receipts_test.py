from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.invoice_management.coupa.view_all_receipts import (
    coupa_view_all_receipts,
)


def test_coupa_view_all_receipts() -> None:
    """Test that the `view_all_receipts` function returns the expected response."""

    # Define test data:
    test_data = [
        {"id": 10603, "type": "ReceivingQuantityConsumption", "created-by": {"login": "mjordan"}},
        {"id": 10544, "type": "InventoryReceipt", "created-by": {"login": "mjordan"}},
    ]
    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.invoice_management.coupa.view_all_receipts.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request_list.return_value = test_data

        # View all receipts call
        receipts = coupa_view_all_receipts().content

        # Ensure that coupa_view_all_receipts executed and returned proper values
        assert len(receipts) == 2
        assert receipts[0].id == 10603
        assert receipts[1].id == 10544

        # Ensure the API call was made with expected parameters
        mock_client.get_request_list.assert_called_once_with(
            resource_name="receiving_transactions",
            params={
                "limit": 10,
                "offset": 0,
                "order_by": "created-at",
                "dir": "desc",
            },
        )
