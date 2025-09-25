from enum import StrEnum
from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.date_conversion import sap_date_to_iso_8601
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


class S4HANAInvoiceStatus(StrEnum):
    """Enum specifying the status for invoices in SAP S4 HANA."""

    DEFINED_FOR_BACKGROUND_VERIFICATION = "1"
    DELETED = "2"
    WITH_ERRORS = "3"
    CORRECT = "4"
    POSTED = "5"
    PARKED = "A"
    PARKED_AND_COMPLETED = "B"
    PARKED_AND_HELD = "C"
    ENTERED_AND_HELD = "D"
    PARKED_AND_RELEASED = "E"


@dataclass
class S4HANAInvoice:
    """Represents an invoice in SAP S4 HANA."""

    invoice_id: str
    fiscal_year: str
    company_code: str
    creation_date: str
    supplier: str
    status: Optional[str] = None
    document_currency: Optional[str] = None
    invoice_gross_amount: Optional[str] = None
    document_number: Optional[str] = None
    posting_date: Optional[str] = None


@dataclass
class S4HANAInvoicesResponse:
    """Represents the response from retrieving a list of invoices in SAP S4 HANA."""

    invoices: List[S4HANAInvoice]


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_get_invoices(
    supplier_id: Optional[str] = None,
    invoice_status: Optional[S4HANAInvoiceStatus] = None,
    payment_blocked_invoice: Optional[bool] = False,
    limit: Optional[int] = 20,
    skip: Optional[int] = 0,
) -> ToolResponse:
    """
    Gets the list of the invoices from SAP S4 HANA.

    Args:
        supplier_id: The unique identifier of the supplier returned by `get_suppliers` tool.
        invoice_status: The current status of the invoice.
        payment_blocked_invoice: Filters the invoices where payments got blocked.
        limit: The number of invoices returned.
        skip: The number of invoices to skip for pagination.

    Returns:
        List of supplier invoices.
    """

    try:
        client = get_sap_s4_hana_client()

    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    filters = []
    if supplier_id:
        filters.append(f"(InvoicingParty eq '{supplier_id}')")
    if invoice_status:
        filters.append(
            f"(SupplierInvoiceStatus eq '{S4HANAInvoiceStatus[invoice_status.upper()].value}')"
        )
    if payment_blocked_invoice:
        filters.append("(PaymentBlockingReason eq 'A' or PaymentBlockingReason eq 'B')")

    filter_expr = " and ".join(filters) if filters else None

    params = {"$top": limit, "$skip": skip}

    response = client.get_request(
        entity="API_SUPPLIERINVOICE_PROCESS_SRV/A_SupplierInvoice",
        filter_expr=filter_expr,
        params=params,
    )

    if "error" in response:
        content = response.get("error", {}).get("message", {})
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    if "fault" in response:
        content = response.get("fault", {}).get("faultstring", "")
        return ToolResponse(success=False, message="Request unsuccessful", content=content)

    invoices: List[S4HANAInvoice] = []
    for result in response["response"]["d"]["results"]:
        invoices.append(
            S4HANAInvoice(
                invoice_id=result.get("SupplierInvoice", ""),
                fiscal_year=result.get("FiscalYear", ""),
                company_code=result.get("CompanyCode", ""),
                status=S4HANAInvoiceStatus(result.get("SupplierInvoiceStatus", "")).name,
                creation_date=(sap_date_to_iso_8601(result.get("CreationDate", ""))),
                document_currency=result.get("DocumentCurrency", ""),
                invoice_gross_amount=result.get("InvoiceGrossAmount", ""),
                supplier=result.get("InvoicingParty", ""),
                document_number=result.get("ReverseDocument", ""),
                posting_date=(sap_date_to_iso_8601(result.get("PostingDate", ""))),
            )
        )
    result = S4HANAInvoicesResponse(invoices=invoices)
    return ToolResponse(success=True, message="The data was successfully retrieved", content=result)
