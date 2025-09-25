from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.invoice_management.coupa.common_classes_invoice_management import (
    CoupaInvoiceHeader,
    CoupaInvoicesResponse,
    InvoiceStatus,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_get_all_invoices(
    invoice_number: Optional[str] = None,
    supplier_name: Optional[str] = None,
    status: Optional[InvoiceStatus] = None,
    creation_date_start: Optional[str] = None,
    creation_date_end: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
) -> ToolResponse[CoupaInvoicesResponse]:
    """
    Gets the list of the invoices from Coupa.

    Args:
        invoice_number: The number of the invoice.
        supplier_name: The supplier name returned by `get_supplier` tool.
        status: The current status of the invoice.
        creation_date_start: The start date for filtering invoices by creation date in ISO 8601 format.
        creation_date_end: The end date for filtering invoices by creation date in ISO 8601 format.
        limit: The maximum number of invoices to retrieve in a single API call. Defaults to 10.
        offset: The number of invoices to skip for pagination purposes.

    Returns:
        List of invoices.
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params = {
        "fields": '["id","invoice-number",{"supplier":["name"]},"net-due-date","gross-total",{"currency":["code"]},"status","created-at"]',
        "invoice-number": invoice_number,
        "supplier[name][contains]": supplier_name,
        "status": status,
        "created-at[gt_or_eq]": creation_date_start,
        "created-at[lt_or_eq]": creation_date_end,
        "limit": limit,
        "offset": offset,
    }
    params = {key: value for key, value in params.items() if value not in (None, "", "null")}

    response = client.get_request_list(resource_name="invoices", params=params)
    if len(response) == 1 and "errors" in response[0]:
        return ToolResponse(success=False, message=coupa_format_error_string(response[0]))

    if len(response) == 0:
        return ToolResponse(
            success=True, message="There were no invoices that matched the provided criteria."
        )

    invoices: List[CoupaInvoiceHeader] = []
    for invoice in response:
        invoices.append(
            CoupaInvoiceHeader(
                invoice_id=invoice.get("id", 0),
                invoice_number=invoice.get("invoice-number", "") or "",
                supplier_name=(
                    invoice.get("supplier", {}).get("name")
                    if isinstance(invoice.get("supplier"), dict)
                    else invoice.get("supplier")
                )
                or "",
                net_due_date=invoice.get("net-due-date", "") or "",
                total_amount=invoice.get("gross-total", ""),
                currency=(
                    invoice.get("currency", {}).get("code")
                    if isinstance(invoice.get("currency"), dict)
                    else invoice.get("currency")
                )
                or "",
                status=invoice.get("status", ""),
                created_at=invoice.get("created-at", ""),
            )
        )

    return ToolResponse(
        success=True,
        message="Following is the list of invoices that match your criteria",
        content=CoupaInvoicesResponse(invoices=invoices),
    )
