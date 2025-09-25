from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.invoice_management.coupa.get_invoice_by_id import (
    coupa_get_invoice_by_id,
)


def test_coupa_get_invoice_by_id() -> None:
    """Test that the `coupa_get_invoice_by_id` function returns the expected response."""

    # Define test data:
    test_data = {"invoice_id": 713513, "invoice_number": "713513M"}

    # Patch `get_coupa_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.invoice_management.coupa.get_invoice_by_id.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "id": test_data["invoice_id"],
            "invoice-number": test_data["invoice_number"],
        }
        response = coupa_get_invoice_by_id(test_data["invoice_id"]).content
        assert response
        assert response.id == test_data["invoice_id"]
        assert response.invoice_number == test_data["invoice_number"]
