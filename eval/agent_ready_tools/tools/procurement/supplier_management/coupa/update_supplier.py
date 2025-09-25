from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.supplier_management.coupa.supplier_dataclasses import (
    CoupaPurchaseOrderType,
    CoupaRemitToAddress,
    InvoiceMatchingLevel,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@dataclass
class UpdateSupplierResult:
    """Represents the result of creating a supplier in Coupa."""

    id: int


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_update_supplier_details(
    supplier_id: int,
    status: Optional[str] = None,
    name: Optional[str] = None,
    po_email: Optional[str] = None,
    invoice_matching_level: Optional[InvoiceMatchingLevel] = None,
    po_method: Optional[CoupaPurchaseOrderType] = None,
    po_change_method: Optional[CoupaPurchaseOrderType] = None,
    remit_to_address: Optional[CoupaRemitToAddress] = None,
) -> ToolResponse[UpdateSupplierResult]:
    """
    Update a supplier details in Coupa.

    Args:
        supplier_id: Supplier ID
        status: Supplier status
        name: Supplier name
        po_email: Email where POs are sent if PO transmission is 'email'
        invoice_matching_level: Invoice matching level
        po_method: Purchase order transmission method
        po_change_method: Purchase order change transmission method
        remit_to_address: Remit-to-address

    Returns:
        Result from updating supplier
    """

    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    payload: dict[str, Any] = {}

    fields = ["id"]

    optional_fields = {
        "name": name,
        "status": status,
        "po-email": po_email,
        "invoice-matching-level": (str(invoice_matching_level) if invoice_matching_level else None),
        "po-method": str(po_method) if po_method else None,
        "po-change-method": str(po_change_method) if po_change_method else None,
        "remit-to-address": remit_to_address,
    }

    for key, value in optional_fields.items():
        if value is not None:
            payload[key] = value
            fields.append(key)

    fields_str = '["' + '","'.join(fields) + '"]'

    response = client.put_request(
        resource_name=f"suppliers/{supplier_id}",
        params={"fields": fields_str},
        payload=payload,
    )

    if "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))

    return ToolResponse(
        success=True,
        message="Supplier details updated",
        content=UpdateSupplierResult(id=response["id"]),
    )
