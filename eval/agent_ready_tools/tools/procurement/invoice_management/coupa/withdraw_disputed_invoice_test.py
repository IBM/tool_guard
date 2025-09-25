from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.invoice_management.coupa.withdraw_disputed_invoice import (
    coupa_withdraw_disputed_invoice,
)


def test_withdraw_disputed_invoice_success() -> None:
    """Test withdrawing a disputed invoice when status is valid (Disputed)."""

    test_data = {"invoice_id": 12345, "current_status": "Disputed", "result_status": "Withdrawn"}

    with patch(
        "agent_ready_tools.tools.procurement.invoice_management.coupa.withdraw_disputed_invoice.get_coupa_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        # Mock invoice fetch returns disputed status
        mock_client.get_request.return_value = {
            "id": test_data["invoice_id"],
            "status": test_data["current_status"],
        }

        # Mock successful withdrawal response
        mock_client.put_request.return_value = {
            "id": test_data["invoice_id"],
            "status": test_data["result_status"],
        }

        response = coupa_withdraw_disputed_invoice(test_data["invoice_id"]).content

        assert response.invoice_id == test_data["invoice_id"]
        assert response.status == test_data["result_status"]
        mock_client.get_request.assert_called_once_with(
            resource_name=f"invoices/{test_data['invoice_id']}"
        )
        mock_client.put_request.assert_called_once_with(
            resource_name=f"invoices/{test_data['invoice_id']}/withdraw_dispute"
        )


def test_withdraw_disputed_invoice_invalid_status() -> None:
    """Test withdrawal is not allowed when status is not Disputed."""

    test_data = {"invoice_id": 99999, "invalid_status": "Approved"}

    with patch(
        "agent_ready_tools.tools.procurement.invoice_management.coupa.withdraw_disputed_invoice.get_coupa_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_client.get_request.return_value = {
            "id": test_data["invoice_id"],
            "status": test_data["invalid_status"],
        }

        response = coupa_withdraw_disputed_invoice(test_data["invoice_id"])

        assert response.success is False
        assert response.content is None

        mock_client.get_request.assert_called_once_with(
            resource_name=f"invoices/{test_data['invoice_id']}"
        )
        mock_client.put_request.assert_not_called()
