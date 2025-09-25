from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.invoice_management.coupa.common_classes_invoice_management import (
    InvoiceStatus,
)
from agent_ready_tools.tools.procurement.invoice_management.coupa.get_invoices import (
    coupa_get_all_invoices,
)


def test_coupa_get_invoices() -> None:
    """Test the get_invoices tool."""

    # Define test data
    test_data = {
        "invoice-id": "123",
        "invoice-number": "inv-123",
        "supplier_name": "udpate name",
        "net-due-date": "",
        "gross-total": "0.00",
        "currency": "USD",
        "status": "draft",
        "created-at": "2021-03-25T19:47:07-07:00",
    }

    # Patch get_coupa_client to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.invoice_management.coupa.get_invoices.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request_list.return_value = [
            {
                "id": test_data["invoice-id"],
                "invoice-number": test_data["invoice-number"],
                "supplier": {"name": test_data["supplier_name"]},
                "net-due-date": test_data["net-due-date"],
                "gross-total": test_data["gross-total"],
                "currency": {"code": test_data["currency"]},
                "status": test_data["status"],
                "created-at": test_data["created-at"],
            }
        ]

        # Call the function under test
        response = coupa_get_all_invoices().content.invoices

        # Assertions

        assert len(response) == 1
        invoice = response[0]
        assert invoice.invoice_id == int(test_data["invoice-id"])
        assert invoice.invoice_number == test_data["invoice-number"]
        assert invoice.supplier_name == test_data["supplier_name"]
        assert invoice.currency == test_data["currency"]
        assert invoice.net_due_date == test_data["net-due-date"]
        assert invoice.total_amount == test_data["gross-total"]
        assert invoice.status == test_data["status"]
        assert invoice.created_at == test_data["created-at"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request_list.assert_called_once_with(
            resource_name="invoices",
            params={
                "fields": '["id","invoice-number",{"supplier":["name"]},"net-due-date","gross-total",{"currency":["code"]},"status","created-at"]',
                "limit": 10,
                "offset": 0,
            },
        )


def test_get_invoices_with_status() -> None:
    """Test the get_invoices tool using one of the optional parameter status."""

    # Define test data
    test_data = {
        "invoice-id": "123",
        "invoice-number": "772621-1",
        "supplier_name": "Manpower",
        "net-due-date": "2024-08-28T23:59:59-07:00",
        "gross-total": "2715.80",
        "currency": "USD",
        "status": "pending_action",
        "created-at": "2013-09-09T12:09:36-07:00",
    }

    # Patch get_coupa_client to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.invoice_management.coupa.get_invoices.get_coupa_client"
    ) as mock_coupa_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_coupa_client.return_value = mock_client
        mock_client.get_request_list.return_value = [
            {
                "id": test_data["invoice-id"],
                "invoice-number": test_data["invoice-number"],
                "supplier": {"name": test_data["supplier_name"]},
                "net-due-date": test_data["net-due-date"],
                "gross-total": test_data["gross-total"],
                "currency": {"code": test_data["currency"]},
                "status": test_data["status"],
                "created-at": test_data["created-at"],
            }
        ]

        # Call the function under test
        response = coupa_get_all_invoices(status=InvoiceStatus.PENDING_ACTION).content.invoices

        # Assertions

        assert len(response) == 1
        invoice = response[0]
        assert invoice.invoice_id == int(test_data["invoice-id"])
        assert invoice.invoice_number == test_data["invoice-number"]
        assert invoice.supplier_name == test_data["supplier_name"]
        assert invoice.currency == test_data["currency"]
        assert invoice.net_due_date == test_data["net-due-date"]
        assert invoice.total_amount == test_data["gross-total"]
        assert invoice.status == test_data["status"]
        assert invoice.created_at == test_data["created-at"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request_list.assert_called_once_with(
            resource_name="invoices",
            params={
                "status": InvoiceStatus.PENDING_ACTION,
                "fields": '["id","invoice-number",{"supplier":["name"]},"net-due-date","gross-total",{"currency":["code"]},"status","created-at"]',
                "limit": 10,
                "offset": 0,
            },
        )
