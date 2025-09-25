from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.invoice_management.coupa.create_an_invoice import (
    coupa_create_an_invoice,
)


def test_coupa_create_an_invoice() -> None:
    """Test that the `view_a_receipt` function returns the expected response."""

    test_data = {
        "po_id": 4070,
        "invoice_number": "INV-4070-01",
        "invoice_date_str": "2025-04-22",
    }
    with patch(
        "agent_ready_tools.tools.procurement.invoice_management.coupa.create_an_invoice.get_coupa_client"
    ) as mock_coupa_client:
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "id": 123,
            "supplier": {"id": 84},
            "currency": {"code": "USD"},
            "order-lines": [
                {
                    "id": 5658,
                    "type": "OrderQuantityLine",
                    "price": "250.00",
                    "quantity": "20.0",
                    "total": "5000.00",
                    "uom": {"code": "HR"},
                    "description": "Sr. Project Manager",
                    "account": {"id": 1445, "account-type-id": 18},
                    "total-with-estimated-tax": "5000.00",
                    "estimated-tax-amount": "0.00",
                }
            ],
            "total-with-estimated-tax": "5000.00",
            "estimated-tax-amount": "0.00",
        }
        post_payload = {
            "supplier": {"id": 84},
            "invoice-number": "INV-4070-01",
            "invoice-date": "2025-04-22",
            "currency": {"code": "USD"},
            "invoice-lines": [
                {
                    "order-line-id": 5658,
                    "type": "InvoiceQuantityLine",
                    "price": "250.00",
                    "quantity": "20.0",
                    "total": "5000.00",
                    "uom": {"code": "HR"},
                    "description": "Sr. Project Manager",
                    "account": {"id": 1445, "account-type-id": 18},
                }
            ],
            "shipping-amount": "0.0",
            "handling-amount": "0.0",
            "misc-amount": "0.0",
            "tax-amount": "0.00",
            "total-with-taxes": "5000.00",
            "gross-total": "5000.0",
        }
        mock_client.post_request.return_value = {
            "id": 1,
        }
        new_invoice_id = coupa_create_an_invoice(
            test_data["po_id"],
            test_data["invoice_number"],
            test_data["invoice_date_str"],
        ).content
        assert new_invoice_id == 1
        mock_client.get_request.assert_called_once_with(
            resource_name=f"purchase_orders/{test_data['po_id']}"
        )
        mock_client.post_request.assert_called_once_with(
            resource_name="invoices", payload=post_payload
        )
