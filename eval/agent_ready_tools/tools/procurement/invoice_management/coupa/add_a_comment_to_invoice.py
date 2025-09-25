from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@dataclass
class CoupaAddCommentToInvoiceResponse:
    """Represents the response from adding a commemt to an existing invoice in Coupa."""

    comment_id: int


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_add_a_comment_to_invoice(
    invoice_id: str, comment: str
) -> ToolResponse[CoupaAddCommentToInvoiceResponse]:
    """
    Add a comment to an invoice.

    Note: there is no comment deletion supported by Coupa API at this time.

    Args:
        invoice_id: a unique invoice identifier
        comment: a comment to be added to the invoice indentified by invoice_number as InvoiceHeader

    Returns:
        The result from submitting the requisition creation request.
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    resource_name = f"invoices/{invoice_id}/comments"
    payload = {
        "comments": f"{comment}",
        "commentable-id": f"{invoice_id}",
        "commentable-type": "InvoiceHeader",
    }
    response = client.post_request(resource_name=resource_name, payload=payload)
    if "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))

    return ToolResponse(
        success=True,
        message="The comment was added to the invoice.",
        content=CoupaAddCommentToInvoiceResponse(comment_id=response["id"]),
    )
