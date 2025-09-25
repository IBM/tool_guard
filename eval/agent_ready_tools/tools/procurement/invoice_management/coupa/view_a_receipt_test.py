from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.invoice_management.coupa.view_a_receipt import (
    coupa_view_a_receipt,
)


def test_coupa_view_a_receipt() -> None:
    """Test that the `view_a_receipt` function returns the expected response."""

    # Define test data:
    test_data = {"id": 10544, "type": "InventoryReceipt"}
    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.invoice_management.coupa.view_a_receipt.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "id": test_data["id"],
            "type": test_data["type"],
        }
        # View a receipt test
        receipt = coupa_view_a_receipt(str(test_data["id"])).content
        # Ensure that view_a_receipt_coupa() executed and returned proper values
        assert receipt
        assert receipt.id == test_data["id"]
        assert receipt.type == test_data["type"]
        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            resource_name=f"receiving_transactions/{test_data['id']}"
        )
