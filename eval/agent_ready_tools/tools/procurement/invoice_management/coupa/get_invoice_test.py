from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.invoice_management.coupa.get_invoice import (
    coupa_get_invoice,
)


def test_coupa_get_invoice() -> None:
    """Test that the `read_an_invoice_coupa` function returns the expected response."""

    # Define test data:
    test_data = {"invoice_id": 713513, "invoice_number": "713513M"}

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.invoice_management.coupa.get_invoice.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request_list.return_value = [
            {
                "id": test_data["invoice_id"],
                "invoice-number": test_data["invoice_number"],
            }
        ]
        # Read the invoice
        response = coupa_get_invoice(test_data["invoice_number"]).content
        # Ensure that coupa_get_invoice() executed and returned proper values
        assert response
        assert response.id == test_data["invoice_id"]
        assert response.invoice_number == test_data["invoice_number"]
