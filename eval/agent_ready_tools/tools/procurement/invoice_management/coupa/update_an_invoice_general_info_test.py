from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.invoice_management.coupa.update_an_invoice_general_info import (
    coupa_update_an_invoice_general_info,
)


def test_coupa_update_an_invoice_general_info() -> None:
    """Test that the `coupa_update_an_invoice_general_info` function returns the expected
    response."""

    # Define test data
    test_data = {
        "invoice_id": 4070,
        "invoice_number": "INV-4070-01",
        "invoice_date": "2025-04-22",
        "currency_code": "USD",
        "shipping_amount": "20.0",
        "handling_amount": "10.0",
        "misc_amount": "5.0",
    }
    with patch(
        "agent_ready_tools.tools.procurement.invoice_management.coupa.update_an_invoice_general_info.get_coupa_client"
    ) as mock_coupa_client:
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        data = {
            "invoice-number": test_data["invoice_number"],
            "invoice-date": test_data["invoice_date"],
            "currency": {
                "code": test_data["currency_code"],
            },
            "shipping-amount": test_data["shipping_amount"],
            "handling-amount": test_data["handling_amount"],
            "misc-amount": test_data["misc_amount"],
        }
        mock_client.put_request.return_value = {"id": test_data["invoice_id"]}
        ret = coupa_update_an_invoice_general_info(
            test_data["invoice_id"],
            invoice_number=test_data["invoice_number"],
            invoice_date=test_data["invoice_date"],
            currency_code=test_data["currency_code"],
            shipping_amount=test_data["shipping_amount"],
            handling_amount=test_data["handling_amount"],
            misc_amount=test_data["misc_amount"],
        ).content
        assert isinstance(ret, bool)
        assert ret  # check if ret being True (successfully updated the requested fields)
        mock_client.put_request.assert_called_once_with(
            resource_name=f"invoices/{test_data["invoice_id"]}", payload=data
        )
