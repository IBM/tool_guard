from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.invoice_management.coupa.void_a_receipt import (
    coupa_void_a_receipt,
)


def test_coupa_void_a_receipt() -> None:
    """Test that the `void_a_receipt_coupa` function returns the expected response."""

    # Define test data:
    test_data = {"receipt_id": "713513"}

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.invoice_management.coupa.void_a_receipt.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.put_request.return_value = {
            "id": test_data["receipt_id"],
            "status": "voided",
        }

        # void the receipt
        response = coupa_void_a_receipt(test_data["receipt_id"]).content

        # Ensure that void_a_receipt_coupa() executed and returned proper values
        assert response
        resource_name = f"receiving_transactions/{test_data["receipt_id"]}/void"
        mock_client.put_request.assert_called_once_with(resource_name=resource_name)
