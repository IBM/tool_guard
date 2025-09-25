from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.invoice_management.sap_s4_hana.get_invoices import (
    S4HANAInvoiceStatus,
    sap_s4_hana_get_invoices,
)


def test_sap_s4_hana_get_invoices() -> None:
    """Test that the `sap_s4_hana_get_invoices` function returns the expected response."""
    # Define test data:
    test_data = {
        "invoice_id": "5100000012",
        "fiscal_year": "2018",
        "company_code": "1010",
        "status": "5",
        "creation_date": "2018-03-27",
        "document_currency": "EUR",
        "invoice_gross_amount": "875.00",
        "supplier": "10300083",
        "document_number": "",
        "posting_date": "2018-03-27",
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.invoice_management.sap_s4_hana.get_invoices.get_sap_s4_hana_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "response": {
                "d": {
                    "results": [
                        {
                            "SupplierInvoice": test_data["invoice_id"],
                            "FiscalYear": test_data["fiscal_year"],
                            "CompanyCode": test_data["company_code"],
                            "SupplierInvoiceStatus": test_data["status"],
                            "CreationDate": test_data["creation_date"],
                            "DocumentCurrency": test_data["document_currency"],
                            "InvoiceGrossAmount": test_data["invoice_gross_amount"],
                            "InvoicingParty": test_data["supplier"],
                            "ReverseDocument": test_data["document_number"],
                            "PostingDate": test_data["posting_date"],
                        },
                    ]
                }
            }
        }

        # Get Invoices
        response = sap_s4_hana_get_invoices().content

        # Ensure that sap_s4_hana_get_invoices() executed and returned proper values
        assert response
        assert len(response.invoices) == 1
        invoice = response.invoices[0]
        assert invoice.invoice_id == test_data["invoice_id"]
        assert invoice.fiscal_year == test_data["fiscal_year"]
        assert invoice.company_code == test_data["company_code"]
        assert invoice.status == S4HANAInvoiceStatus(test_data["status"]).name
        assert invoice.creation_date == test_data["creation_date"]
        assert invoice.document_currency == test_data["document_currency"]
        assert invoice.invoice_gross_amount == test_data["invoice_gross_amount"]
        assert invoice.supplier == test_data["supplier"]
        assert invoice.document_number == test_data["document_number"]
        assert invoice.posting_date == test_data["posting_date"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="API_SUPPLIERINVOICE_PROCESS_SRV/A_SupplierInvoice",
            params={"$top": 20, "$skip": 0},
            filter_expr=None,
        )


def test_sap_s4_hana_get_invoices_with_supplier() -> None:
    """Test the `sap_s4_hana_get_invoices` function using one of the optional parameter supplier."""
    # Define test data:
    test_data = {
        "invoice_id": "5100000086",
        "fiscal_year": "2018",
        "company_code": "1010",
        "status": "5",
        "creation_date": "2024-04-19",
        "document_currency": "EUR",
        "invoice_gross_amount": "1735000.00",
        "supplier": "10300083",
        "document_number": "5100000001",
        "posting_date": "2023-09-18",
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.invoice_management.sap_s4_hana.get_invoices.get_sap_s4_hana_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "response": {
                "d": {
                    "results": [
                        {
                            "SupplierInvoice": test_data["invoice_id"],
                            "FiscalYear": test_data["fiscal_year"],
                            "CompanyCode": test_data["company_code"],
                            "SupplierInvoiceStatus": test_data["status"],
                            "CreationDate": test_data["creation_date"],
                            "DocumentCurrency": test_data["document_currency"],
                            "InvoiceGrossAmount": test_data["invoice_gross_amount"],
                            "InvoicingParty": test_data["supplier"],
                            "ReverseDocument": test_data["document_number"],
                            "PostingDate": test_data["posting_date"],
                        },
                    ]
                }
            }
        }

        # Get Invoices
        response = sap_s4_hana_get_invoices(supplier_id="10300083").content

        # Ensure that sap_s4_hana_get_invoices() executed and returned proper values
        assert response
        assert len(response.invoices) == 1
        invoice = response.invoices[0]
        assert invoice.invoice_id == test_data["invoice_id"]
        assert invoice.fiscal_year == test_data["fiscal_year"]
        assert invoice.company_code == test_data["company_code"]
        assert invoice.status == S4HANAInvoiceStatus(test_data["status"]).name
        assert invoice.creation_date == test_data["creation_date"]
        assert invoice.document_currency == test_data["document_currency"]
        assert invoice.invoice_gross_amount == test_data["invoice_gross_amount"]
        assert invoice.supplier == test_data["supplier"]
        assert invoice.document_number == test_data["document_number"]
        assert invoice.posting_date == test_data["posting_date"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="API_SUPPLIERINVOICE_PROCESS_SRV/A_SupplierInvoice",
            params={"$top": 20, "$skip": 0},
            filter_expr=f"(InvoicingParty eq '{test_data['supplier']}')",
        )


def test_sap_s4_hana_get_invoices_with_payment_blocked_invoice() -> None:
    """Test that the `sap_s4_hana_get_invoices` function returns the expected response."""
    # Define test data:
    test_data = {
        "invoice_id": "5100000088",
        "fiscal_year": "2023",
        "company_code": "1010",
        "status": "D",
        "creation_date": "2024-04-19",
        "document_currency": "EUR",
        "invoice_gross_amount": "0.00",
        "supplier": "10300001",
        "document_number": "",
        "posting_date": "2023-09-18",
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.invoice_management.sap_s4_hana.get_invoices.get_sap_s4_hana_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "response": {
                "d": {
                    "results": [
                        {
                            "SupplierInvoice": test_data["invoice_id"],
                            "FiscalYear": test_data["fiscal_year"],
                            "CompanyCode": test_data["company_code"],
                            "SupplierInvoiceStatus": test_data["status"],
                            "CreationDate": test_data["creation_date"],
                            "DocumentCurrency": test_data["document_currency"],
                            "InvoiceGrossAmount": test_data["invoice_gross_amount"],
                            "InvoicingParty": test_data["supplier"],
                            "ReverseDocument": test_data["document_number"],
                            "PostingDate": test_data["posting_date"],
                        },
                    ]
                }
            }
        }

        # Get Invoices
        response = sap_s4_hana_get_invoices(payment_blocked_invoice=True).content

        # Ensure that sap_s4_hana_get_invoices() executed and returned proper values
        assert response
        assert len(response.invoices) == 1
        invoice = response.invoices[0]
        assert invoice.invoice_id == test_data["invoice_id"]
        assert invoice.fiscal_year == test_data["fiscal_year"]
        assert invoice.company_code == test_data["company_code"]
        assert invoice.status == S4HANAInvoiceStatus(test_data["status"]).name
        assert invoice.creation_date == test_data["creation_date"]
        assert invoice.document_currency == test_data["document_currency"]
        assert invoice.invoice_gross_amount == test_data["invoice_gross_amount"]
        assert invoice.supplier == test_data["supplier"]
        assert invoice.document_number == test_data["document_number"]
        assert invoice.posting_date == test_data["posting_date"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="API_SUPPLIERINVOICE_PROCESS_SRV/A_SupplierInvoice",
            params={"$top": 20, "$skip": 0},
            filter_expr="(PaymentBlockingReason eq 'A' or PaymentBlockingReason eq 'B')",
        )


def test_sap_s4_hana_get_invoices_with_payment_blocked_invoice_2() -> None:
    """Test that the `sap_s4_hana_get_invoices` function returns the expected response."""
    # Define test data:
    test_data = {
        "invoice_id": "5100000100",
        "fiscal_year": "2023",
        "company_code": "1010",
        "status": "D",
        "creation_date": "2024-04-27",
        "document_currency": "EUR",
        "invoice_gross_amount": "430.00",
        "supplier": "BP1010",
        "document_number": "",
        "posting_date": "2023-09-25",
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.invoice_management.sap_s4_hana.get_invoices.get_sap_s4_hana_client"
    ) as mock_sap_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "response": {
                "d": {
                    "results": [
                        {
                            "SupplierInvoice": test_data["invoice_id"],
                            "FiscalYear": test_data["fiscal_year"],
                            "CompanyCode": test_data["company_code"],
                            "SupplierInvoiceStatus": test_data["status"],
                            "CreationDate": test_data["creation_date"],
                            "DocumentCurrency": test_data["document_currency"],
                            "InvoiceGrossAmount": test_data["invoice_gross_amount"],
                            "InvoicingParty": test_data["supplier"],
                            "ReverseDocument": test_data["document_number"],
                            "PostingDate": test_data["posting_date"],
                        },
                    ]
                }
            }
        }

        # Get Invoices
        response = sap_s4_hana_get_invoices(
            supplier_id=test_data["supplier"], payment_blocked_invoice=True
        ).content

        # Ensure that sap_s4_hana_get_invoices() executed and returned proper values
        assert response
        assert len(response.invoices) == 1
        invoice = response.invoices[0]
        assert invoice.invoice_id == test_data["invoice_id"]
        assert invoice.fiscal_year == test_data["fiscal_year"]
        assert invoice.company_code == test_data["company_code"]
        assert invoice.status == S4HANAInvoiceStatus(test_data["status"]).name
        assert invoice.creation_date == test_data["creation_date"]
        assert invoice.document_currency == test_data["document_currency"]
        assert invoice.invoice_gross_amount == test_data["invoice_gross_amount"]
        assert invoice.supplier == test_data["supplier"]
        assert invoice.document_number == test_data["document_number"]
        assert invoice.posting_date == test_data["posting_date"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="API_SUPPLIERINVOICE_PROCESS_SRV/A_SupplierInvoice",
            params={"$top": 20, "$skip": 0},
            filter_expr=f"(InvoicingParty eq '{test_data["supplier"]}') and (PaymentBlockingReason eq 'A' or PaymentBlockingReason eq 'B')",
        )
