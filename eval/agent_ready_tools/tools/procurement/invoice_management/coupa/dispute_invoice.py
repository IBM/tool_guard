from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@dataclass
class CoupaDisputeInvoiceResponse:
    """Represents the result of disputing an invoice in Coupa."""

    invoice_id: int
    status: str


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_dispute_invoice(invoice_id: int) -> ToolResponse[CoupaDisputeInvoiceResponse]:
    """
    Dispute an invoice.

    Args:
        invoice_id: The ID of the invoice to dispute in Coupa.

    Returns:
        Confirmation that the invoice has been disputed.
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    invoice = client.get_request(resource_name=f"invoices/{invoice_id}")
    if "errors" in invoice:
        return ToolResponse(success=False, message=coupa_format_error_string(invoice))

    current_status = invoice.get("status", "")
    allowed_statuses = {"pending_action", "pending_receipt", "pending_approval"}
    if current_status not in allowed_statuses:
        return ToolResponse(
            success=False, message=f"Cannot dispute invoice with status: {current_status}."
        )

    resource_name = f"invoices/{invoice_id}/dispute"
    response = client.put_request(resource_name=resource_name)
    if "errors" in invoice:
        return ToolResponse(success=False, message=coupa_format_error_string(response))

    return ToolResponse(
        success=True,
        message="The invoice was successfully disputed.",
        content=CoupaDisputeInvoiceResponse(
            invoice_id=response.get("id", invoice_id), status=response.get("status", "Disputed")
        ),
    )
