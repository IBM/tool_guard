from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.invoice_management.coupa.dispute_invoice import (
    coupa_dispute_invoice,
)


def test_coupa_dispute_invoice_success() -> None:
    """Test that the `dispute_invoice` function returns the expected response when status is
    valid."""

    test_data = {
        "invoice_id": 713514,
        "status": "disputed",
    }

    with patch(
        "agent_ready_tools.tools.procurement.invoice_management.coupa.dispute_invoice.get_coupa_client"
    ) as mock_coupa_client:
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client

        mock_client.get_request.return_value = {
            "id": test_data["invoice_id"],
            "status": "pending_action",
        }

        mock_client.put_request.return_value = {
            "id": test_data["invoice_id"],
            "status": test_data["status"],
        }

        response = coupa_dispute_invoice(test_data["invoice_id"]).content

        assert response
        assert response.invoice_id == test_data["invoice_id"]
        assert response.status == test_data["status"]

        mock_client.get_request.assert_called_once_with(
            resource_name=f"invoices/{test_data['invoice_id']}"
        )
        mock_client.put_request.assert_called_once_with(
            resource_name=f"invoices/{test_data['invoice_id']}/dispute"
        )


def test_coupa_dispute_invoice_invalid_status() -> None:
    """Test that the `dispute_invoice` function skips dispute when status is invalid."""

    test_data = {
        "invoice_id": 713514,
    }

    with patch(
        "agent_ready_tools.tools.procurement.invoice_management.coupa.dispute_invoice.get_coupa_client"
    ) as mock_coupa_client:
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client

        mock_client.get_request.return_value = {
            "id": test_data["invoice_id"],
            "status": "approved",  # Invalid status (lowercase for consistency)
        }

        response = coupa_dispute_invoice(test_data["invoice_id"])

        assert response.success is False
        assert response.content is None

        mock_client.get_request.assert_called_once_with(
            resource_name=f"invoices/{test_data['invoice_id']}"
        )
        mock_client.put_request.assert_not_called()
