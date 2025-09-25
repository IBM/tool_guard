from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.invoice_management.sap_s4_hana.get_an_invoice import (
    sap_s4_hana_get_an_invoice,
)
from agent_ready_tools.utils.date_conversion import sap_date_to_iso_8601


def test_sap_s4_hana_get_an_invoice() -> None:
    """Test that the `sap_s4_hana_get_an_invoice` function returns the expected response."""

    # Define test data:
    test_data = {
        "invoice_id": "5100000115",
        "fiscal_year": "2024",
        "company_code": "WXO1",
        "purchase_order": "4500001927",
        "tax_code": "E0",
        "due_calculation_base_date": "/Date(1722729600000)/",
        "plant": "WXO1",
        "postal_code": "",
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.invoice_management.sap_s4_hana.get_an_invoice.get_sap_s4_hana_client"
    ) as mock_sap_s4_hana_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_s4_hana_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "response": {
                "d": {
                    "SupplierInvoice": "5100000115",
                    "FiscalYear": "2024",
                    "CompanyCode": "WXO1",
                    "DueCalculationBaseDate": "/Date(1722729600000)/",
                    "to_SuplrInvcItemPurOrdRef": {
                        "results": [
                            {
                                "PurchaseOrder": "4500001927",
                            },
                            {
                                "Plant": "WXO1",
                            },
                        ]
                    },
                    "to_SupplierInvoiceTax": {
                        "results": [
                            {
                                "TaxCode": "E0",
                            }
                        ]
                    },
                    "to_SuplrInvoiceAdditionalData": {
                        "PostalCode": "",
                    },
                }
            }
        }

        # Read the invoice
        response = sap_s4_hana_get_an_invoice(
            test_data["invoice_id"], test_data["fiscal_year"]
        ).content
        print(response.payment)
        # Ensure that sap_s4_hana_get_an_invoice() executed and returned proper values
        assert response
        assert response.invoice_id == test_data["invoice_id"]
        assert response.fiscal_year == test_data["fiscal_year"]
        assert response.company_code == test_data["company_code"]
        assert response.purchase_order[0].purchase_order == test_data["purchase_order"]
        assert response.tax_results[0].tax_code == test_data["tax_code"]
        assert response.payment.due_calculation_base_date == sap_date_to_iso_8601(
            test_data["due_calculation_base_date"]
        )
        assert response.line_items[1].plant == test_data["plant"]
        assert response.vendor.postal_code == test_data["postal_code"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity=f"API_SUPPLIERINVOICE_PROCESS_SRV/A_SupplierInvoice(SupplierInvoice='{test_data["invoice_id"]}',FiscalYear='{test_data["fiscal_year"]}')",
            expand_expr="to_SuplrInvcItemPurOrdRef,to_SuplrInvoiceAdditionalData,to_SupplierInvoiceTax,to_SupplierInvoiceItemGLAcct,to_SupplierInvoiceWhldgTax",
        )
