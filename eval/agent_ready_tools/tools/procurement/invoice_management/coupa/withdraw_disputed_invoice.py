from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@dataclass
class CoupaWithdrawDisputedInvoiceResponse:
    """Represents the result of withdrawing a disputed invoice in Coupa."""

    invoice_id: int
    status: str


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_withdraw_disputed_invoice(
    disputed_invoice_id: int,
) -> ToolResponse[CoupaWithdrawDisputedInvoiceResponse]:
    """
    Withdraw a disputed invoice.

    Args:
        disputed_invoice_id: The ID of the disputed invoice in Coupa.

    Returns:
        Confirmation that the disputed invoice has been withdrawn,
        or a message indicating that withdrawal is not allowed.
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    # Fetch current status of the invoice
    invoice = client.get_request(resource_name=f"invoices/{disputed_invoice_id}")
    current_status = invoice.get("status", "")

    # Only allow withdrawal if invoice is in Disputed status
    if current_status.lower() != "disputed":
        return ToolResponse(
            success=False,
            message=f"Cannot withdraw invoice {disputed_invoice_id} the status is not disputed: {current_status}",
        )

    # Withdraw the dispute
    resource_name = f"invoices/{disputed_invoice_id}/withdraw_dispute"
    response = client.put_request(resource_name=resource_name)
    if "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))

    return ToolResponse(
        success=True,
        message="The disputed invoice was successfully withdrawn.",
        content=CoupaWithdrawDisputedInvoiceResponse(
            invoice_id=response.get("id", disputed_invoice_id),
            status=response.get("status", "Withdrawn"),
        ),
    )
