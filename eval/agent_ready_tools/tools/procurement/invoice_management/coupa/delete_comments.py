from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_delete_a_comment_of_an_invoice(invoice_id: int, comment_id: int) -> ToolResponse[bool]:
    """
    delete invoice all comments.

    Args:
        invoice_id: a unique invoice identifier
        comment_id: a unique comment identifier

    Returns:
        true if succeeded, false otherwise
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    resource_name = f"invoices/{invoice_id}/comments/{comment_id}"
    response = client.delete_request(resource_name=resource_name)
    if isinstance(response, dict) and "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))

    return ToolResponse(
        success=True,
        message=f"The comment {comment_id} was successfully deleted from invoice {invoice_id}.",
        content=response == 200,
    )
