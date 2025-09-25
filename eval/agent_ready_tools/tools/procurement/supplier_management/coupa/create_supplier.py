from typing import Any

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.supplier_management.coupa.supplier_dataclasses import (
    CoupaPurchaseOrderType,
    CreateSupplierResult,
    InvoiceMatchingLevel,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_create_supplier(
    name: str,
    po_email: str,
    invoice_matching_level: InvoiceMatchingLevel = InvoiceMatchingLevel.NONE,
    po_method: CoupaPurchaseOrderType = CoupaPurchaseOrderType.EMAIL,
    po_change_method: CoupaPurchaseOrderType = CoupaPurchaseOrderType.EMAIL,
) -> ToolResponse[CreateSupplierResult]:
    """
    Create a supplier in Coupa.

    Args:
        name: Supplier name
        po_email: Email where POs are sent if PO transmission is 'email'.
        invoice_matching_level: The invoice matching level in Coupa.
        po_method: The purchase order transmission method in Coupa.
        po_change_method: The purchase order transmission method in Coupa.

    Returns:
        Result from creating a supplier
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    payload: dict[str, Any] = {
        "name": name,
        "po-email": po_email,
        "invoice-matching-level": str(invoice_matching_level),
        "po-method": str(po_method),
        "po-change-method": str(po_change_method),
    }

    response = client.post_request(
        resource_name="suppliers", params={"fields": '["id"]'}, payload=payload
    )

    if "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))

    return ToolResponse(
        success=True,
        message="Supplier created",
        content=CreateSupplierResult(id=response["id"]),
    )
