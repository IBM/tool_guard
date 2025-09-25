from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.invoice_management.sap_s4_hana.common_classes_invoice_management import (
    S4HANAInvoicePaymentmethod,
)
from agent_ready_tools.utils.date_conversion import iso_8601_to_sap_date
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


@dataclass
class S4HANACreateInvoiceResponse:
    """Represents the result of invoice creation in SAP S/4HANA."""

    invoice_id: str
    fiscal_year: str


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_create_an_invoice(
    company_code: str,
    document_date: str,
    posting_date: str,
    suppliers_invoice_id: str,
    gross_amount: str,
    supplier_invoice_item: str,
    purchase_order: str,
    purchase_order_item: str,
    tax_code: str,
    document_currency: str,
    quantity: str,
    unit: str,
    document_header_text: Optional[str] = None,
    tax_calculated: Optional[bool] = None,
    quoted_exchange_rate: Optional[str] = None,
    payment_terms: Optional[str] = None,
    cash_discount1_percent: Optional[str] = None,
    cash_discount1_days: Optional[str] = None,
    cash_discount2_percent: Optional[str] = None,
    cash_discount2_days: Optional[str] = None,
    net_payment_days: Optional[str] = None,
    payment_method: Optional[S4HANAInvoicePaymentmethod] = None,
) -> ToolResponse[S4HANACreateInvoiceResponse]:
    """
    Creates a supplier invoice in the SAP S/4HANA system.

    Args:
        company_code: The company code in SAP S/4HANA.
        document_date: The date of the invoice document in ISO 8601 format.
        posting_date: The posting date for the invoice in ISO 8601 format.
        suppliers_invoice_id: The supplier's invoice ID.
        gross_amount: The total gross amount of the invoice.
        supplier_invoice_item: The item number in the supplier invoice.
        purchase_order: The purchase order number associated with the invoice returned by the tool `sap_s4_hana_get_purchase_orders`.
        purchase_order_item: The item number in the purchase order returned by the tool `sap_s4_hana_get_purchase_order_items`.
        tax_code: The tax code applicable to the invoice item.
        document_currency: The currency used in the invoice.
        quantity: The quantity of items in the purchase order.
        unit: The unit of measure for the quantity.
        document_header_text: The header text for the invoice document.
        tax_calculated: Whether tax is calculated automatically.
        quoted_exchange_rate: The exchange rate quoted for the invoice.
        payment_terms: Payment terms applicable to the invoice.
        cash_discount1_percent: First cash discount percentage.
        cash_discount1_days: Number of days for the first cash discount.
        cash_discount2_percent: Second cash discount percentage.
        cash_discount2_days: Number of days for the second cash discount.
        net_payment_days: Number of days until net payment is due.
        payment_method: Enum value specifying the payment method (e.g., CHECK, BANK_TRANSFER_ACH_PPD).

    Returns:
        The result of creating a invoice.
    """
    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    payload: dict[str, Any] = {
        "CompanyCode": company_code,
        "DocumentDate": iso_8601_to_sap_date(document_date),
        "PostingDate": iso_8601_to_sap_date(posting_date),
        "SupplierInvoiceIDByInvcgParty": suppliers_invoice_id,
        "DocumentCurrency": document_currency,
        "InvoiceGrossAmount": gross_amount,
        "DocumentHeaderText": document_header_text,
        "TaxIsCalculatedAutomatically": tax_calculated,
        "DirectQuotedExchangeRate": quoted_exchange_rate,
        "PaymentTerms": payment_terms,
        "CashDiscount1Percent": cash_discount1_percent,
        "CashDiscount1Days": cash_discount1_days,
        "CashDiscount2Percent": cash_discount2_percent,
        "CashDiscount2Days": cash_discount2_days,
        "NetPaymentDays": net_payment_days,
        "PaymentMethod": (
            S4HANAInvoicePaymentmethod[payment_method.upper()].value if payment_method else None
        ),
        "to_SuplrInvcItemPurOrdRef": {
            "results": [
                {
                    "SupplierInvoiceItem": supplier_invoice_item,
                    "PurchaseOrder": purchase_order,
                    "PurchaseOrderItem": purchase_order_item,
                    "TaxCode": tax_code,
                    "DocumentCurrency": document_currency,
                    "SupplierInvoiceItemAmount": gross_amount,
                    "PurchaseOrderQuantityUnit": unit,
                    "QuantityInPurchaseOrderUnit": quantity,
                }
            ]
        },
    }

    response = client.post_request(
        entity="API_SUPPLIERINVOICE_PROCESS_SRV/A_SupplierInvoice", payload=payload
    )

    if "error" in response:
        content = response.get("error", {}).get("message", {})
        return ToolResponse(success=False, message=f"Request unsuccessful {content}")

    if "fault" in response:
        content = response.get("fault", {}).get("faultstring", "")
        return ToolResponse(success=False, message=f"Request unsuccessful {content}")

    invoice_id = response["d"]["SupplierInvoice"]
    fiscal_year = response["d"]["FiscalYear"]

    return ToolResponse(
        success=True,
        message="The supplier was successfully created.",
        content=S4HANACreateInvoiceResponse(invoice_id=invoice_id, fiscal_year=fiscal_year),
    )
