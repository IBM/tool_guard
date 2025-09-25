from typing import Any
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.invoice_management.sap_s4_hana.common_classes_invoice_management import (
    S4HANAInvoicePaymentmethod,
)
from agent_ready_tools.tools.procurement.invoice_management.sap_s4_hana.create_an_invoice import (
    sap_s4_hana_create_an_invoice,
)
from agent_ready_tools.utils.date_conversion import iso_8601_to_sap_date


def test_create_an_invoice() -> None:
    """Test that the `create_an_invoice` tool can successfully create an invoice in SAP S/4HANA."""
    # Define test data:
    test_data: dict[str, Any] = {
        "company_code": "WXO1",
        "document_date": "2025-07-21",
        "posting_date": "2025-07-21",
        "suppliers_invoice_id": "INV_4500001928",
        "gross_amount": "5100.00",
        "tax_calculated": True,
        "quoted_exchange_rate": "1.00000",
        "supplier_invoice_item": "1",
        "purchase_order": "4500001928",
        "purchase_order_item": "10",
        "tax_code": "E0",
        "document_currency": "USD",
        "quantity": "5",
        "unit": "BT",
        "document_header_text": "testing invoice",
        "invoice_id": "5100000140",
        "fiscal_year": "2025",
        "payment_terms": "0004",
        "cash_discount1_percent": "0",
        "cash_discount1_days": "0",
        "cash_discount2_percent": "0",
        "cash_discount2_days": "0",
        "net_payment_days": "0",
        "payment_method": "BANK_TRANSFER_ACH_PPD",
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.invoice_management.sap_s4_hana.create_an_invoice.get_sap_s4_hana_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_client.post_request.return_value = {
            "d": {
                "SupplierInvoice": test_data["invoice_id"],
                "FiscalYear": test_data["fiscal_year"],
            }
        }

        # Create Invoices
        response = sap_s4_hana_create_an_invoice(
            company_code=test_data["company_code"],
            document_date=test_data["document_date"],
            posting_date=test_data["posting_date"],
            suppliers_invoice_id=test_data["suppliers_invoice_id"],
            gross_amount=test_data["gross_amount"],
            supplier_invoice_item=test_data["supplier_invoice_item"],
            purchase_order=test_data["purchase_order"],
            purchase_order_item=test_data["purchase_order_item"],
            tax_code=test_data["tax_code"],
            document_currency=test_data["document_currency"],
            quantity=test_data["quantity"],
            unit=test_data["unit"],
            document_header_text=test_data["document_header_text"],
            tax_calculated=test_data["tax_calculated"],
            quoted_exchange_rate=test_data["quoted_exchange_rate"],
            payment_terms=test_data["payment_terms"],
            cash_discount1_percent=test_data["cash_discount1_percent"],
            cash_discount1_days=test_data["cash_discount1_days"],
            cash_discount2_percent=test_data["cash_discount2_percent"],
            cash_discount2_days=test_data["cash_discount2_days"],
            net_payment_days=test_data["net_payment_days"],
            payment_method=test_data["payment_method"],
        ).content

        # Ensure that craete_an_invoices() executed and returned proper values
        assert response.invoice_id is not None
        assert response.fiscal_year == test_data["fiscal_year"]

        expected_payload = {
            "CompanyCode": test_data["company_code"],
            "DocumentDate": iso_8601_to_sap_date(test_data["document_date"]),
            "PostingDate": iso_8601_to_sap_date(test_data["posting_date"]),
            "SupplierInvoiceIDByInvcgParty": test_data["suppliers_invoice_id"],
            "DocumentCurrency": test_data["document_currency"],
            "InvoiceGrossAmount": test_data["gross_amount"],
            "DocumentHeaderText": test_data["document_header_text"],
            "TaxIsCalculatedAutomatically": test_data["tax_calculated"],
            "DirectQuotedExchangeRate": test_data["quoted_exchange_rate"],
            "PaymentTerms": test_data["payment_terms"],
            "CashDiscount1Percent": test_data["cash_discount1_percent"],
            "CashDiscount1Days": test_data["cash_discount1_days"],
            "CashDiscount2Percent": test_data["cash_discount2_percent"],
            "CashDiscount2Days": test_data["cash_discount2_days"],
            "NetPaymentDays": test_data["net_payment_days"],
            "PaymentMethod": S4HANAInvoicePaymentmethod[test_data["payment_method"]].value,
            "to_SuplrInvcItemPurOrdRef": {
                "results": [
                    {
                        "SupplierInvoiceItem": test_data["supplier_invoice_item"],
                        "PurchaseOrder": test_data["purchase_order"],
                        "PurchaseOrderItem": test_data["purchase_order_item"],
                        "TaxCode": test_data["tax_code"],
                        "DocumentCurrency": test_data["document_currency"],
                        "SupplierInvoiceItemAmount": test_data["gross_amount"],
                        "PurchaseOrderQuantityUnit": test_data["unit"],
                        "QuantityInPurchaseOrderUnit": test_data["quantity"],
                    }
                ]
            },
        }

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="API_SUPPLIERINVOICE_PROCESS_SRV/A_SupplierInvoice",
            payload=expected_payload,
        )
