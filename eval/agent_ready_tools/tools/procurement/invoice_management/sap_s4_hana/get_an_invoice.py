from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.invoice_management.sap_s4_hana.common_classes_invoice_management import (
    S4HANAInvoiceLineItems,
    S4HANAInvoicePayment,
    S4HANAInvoicePurchaseOrder,
    S4HANAInvoiceSupplier,
    S4HANAInvoiceTax,
    SAPS4HANAInvoice,
)
from agent_ready_tools.utils.date_conversion import sap_date_to_iso_8601
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_get_an_invoice(
    invoice_id: int,
    fiscal_year: int,
) -> ToolResponse:
    """
    Gets the details of a supplier invoice from SAP S4 HANA.

    Args:
        invoice_id: The id of the supplier of the invoice.
        fiscal_year: The year of the invoice.

    Returns:
        Details of an invoice.
    """

    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    response = client.get_request(
        entity=f"API_SUPPLIERINVOICE_PROCESS_SRV/A_SupplierInvoice(SupplierInvoice='{invoice_id}',FiscalYear='{fiscal_year}')",
        expand_expr="to_SuplrInvcItemPurOrdRef,to_SuplrInvoiceAdditionalData,to_SupplierInvoiceTax,to_SupplierInvoiceItemGLAcct,to_SupplierInvoiceWhldgTax",
    )

    if "error" in response:
        content = response.get("error", {}).get("message", {})
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    if "fault" in response:
        content = response.get("fault", {}).get("faultstring", "")
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    result = response.get("response", {}).get("d", {})

    invoices = SAPS4HANAInvoice(
        invoice_id=result.get("SupplierInvoice", ""),
        fiscal_year=result.get("FiscalYear", ""),
        company_code=result.get("CompanyCode", ""),
        invoice_date=(sap_date_to_iso_8601(result.get("DocumentDate", ""))),
        posting_date=(sap_date_to_iso_8601(result.get("PostingDate", ""))),
        invoice_gross_amount=result.get("InvoiceGrossAmount", ""),
        currency=result.get("DocumentCurrency", ""),
        invoice_header=result.get("DocumentHeaderText", ""),
        payment_terms=result.get("PaymentTerms", ""),
        due_calculation_base_date=(sap_date_to_iso_8601(result.get("DueCalculationBaseDate", ""))),
        invoice_reference=result.get("InvoiceReference", ""),
        status=result.get("SupplierInvoiceStatus", ""),
        creation_date=(sap_date_to_iso_8601(result.get("CreationDate", ""))),
        assignment=result.get("SupplierInvoiceIDByInvcgParty", ""),
        accounting_document_type=result.get("AccountingDocumentType", ""),
        supplier=result.get("InvoicingParty", ""),
        document_number=result.get("ReverseDocument", ""),
    )

    invoices.payment = S4HANAInvoicePayment(
        invoice_id=result.get("SupplierInvoice", ""),
        fiscal_year=result.get("FiscalYear", ""),
        due_calculation_base_date=(sap_date_to_iso_8601(result.get("DueCalculationBaseDate", ""))),
        manual_cash_discount=result.get("ManualCashDiscount", ""),
        invoice_reference=result.get("InvoiceReference", ""),
        payment_terms=result.get("PaymentTerms", ""),
        cash_discount_1_percent=result.get("CashDiscount1Percent", ""),
        cash_discount_1_days=result.get("CashDiscount1Days", ""),
        cash_discount_2_percent=result.get("CashDiscount2Percent", ""),
        cash_discount_2_days=result.get("CashDiscount2Days", ""),
        net_payment_days=result.get("NetPaymentDays", ""),
        payment_blocking_reason=result.get("PaymentBlockingReason", ""),
    )

    tax_results = result.get("to_SupplierInvoiceTax", {}).get("results", [])
    if tax_results:
        invoices.tax_results = []
        for tax_result in tax_results:
            invoices.tax_results.append(
                S4HANAInvoiceTax(
                    invoice_id=tax_result.get("SupplierInvoice", ""),
                    fiscal_year=tax_result.get("FiscalYear", ""),
                    tax_code=tax_result.get("TaxCode", ""),
                    currency=tax_result.get("DocumentCurrency", ""),
                    tax_amount=tax_result.get("TaxAmount", ""),
                )
            )

    vendor_result = result.get("to_SuplrInvoiceAdditionalData", {})
    if vendor_result:
        invoices.vendor = S4HANAInvoiceSupplier(
            invoice_id=vendor_result.get("SupplierInvoice", ""),
            fiscal_year=vendor_result.get("FiscalYear", ""),
            invoicing_party=result.get("InvoicingParty", ""),
            postal_code=vendor_result.get("PostalCode", ""),
            city_name=vendor_result.get("CityName", ""),
            country=vendor_result.get("Country", ""),
            street_address_name=vendor_result.get("StreetAddressName", ""),
        )

    purchase_order_results = result.get("to_SuplrInvcItemPurOrdRef", {}).get("results", [])
    if purchase_order_results:
        invoices.purchase_order = []
        invoices.line_items = []

        for purchase_order_result in purchase_order_results:
            invoices.purchase_order.append(
                S4HANAInvoicePurchaseOrder(
                    invoice_id=purchase_order_result.get("SupplierInvoice", ""),
                    fiscal_year=purchase_order_result.get("FiscalYear", ""),
                    supplier_invoice_item=purchase_order_result.get("SupplierInvoiceItem", ""),
                    purchase_order=purchase_order_result.get("PurchaseOrder", ""),
                    purchase_order_item=purchase_order_result.get("PurchaseOrderItem", ""),
                    plant=purchase_order_result.get("Plant", ""),
                    reference_document=purchase_order_result.get("ReferenceDocument", ""),
                    reference_document_fiscal_year=purchase_order_result.get(
                        "ReferenceDocumentFiscalYear", ""
                    ),
                    reference_document_item=purchase_order_result.get("ReferenceDocumentItem", ""),
                    tax_code=purchase_order_result.get("TaxCode", ""),
                    supplier_invoice_item_amount=purchase_order_result.get(
                        "SupplierInvoiceItemAmount", ""
                    ),
                    currency=purchase_order_result.get("DocumentCurrency", ""),
                    quantity_in_purchase_order_unit=purchase_order_result.get(
                        "QuantityInPurchaseOrderUnit", ""
                    ),
                )
            )
            invoices.line_items.append(
                S4HANAInvoiceLineItems(
                    invoice_id=purchase_order_result.get("SupplierInvoice", ""),
                    fiscal_year=purchase_order_result.get("FiscalYear", ""),
                    supplier_invoice_item=purchase_order_result.get("SupplierInvoiceItem", ""),
                    purchase_order=purchase_order_result.get("PurchaseOrder", ""),
                    purchase_order_item=purchase_order_result.get("PurchaseOrderItem", ""),
                    plant=purchase_order_result.get("Plant", ""),
                    currency=purchase_order_result.get("DocumentCurrency", ""),
                    quantity_in_purchase_order_unit=purchase_order_result.get(
                        "QuantityInPurchaseOrderUnit", ""
                    ),
                )
            )

    # return invoices
    return ToolResponse(
        success=True, message="The data was successfully retrieved", content=invoices
    )
