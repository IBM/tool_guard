from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.invoice_management.coupa.common_classes_invoice_management import (
    CoupaInvoice,
)
from agent_ready_tools.tools.procurement.invoice_management.coupa.helper_functions_invoice_management import (
    coupa_build_invoice_from_response,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_get_invoice_by_id(invoice_id: int) -> ToolResponse[CoupaInvoice]:
    """
    Get an invoice by its ID.

    Args:
        invoice_id: an invoice ID (digits)

    Returns:
        corresponding invoice retrieved
    """
    try:
        client = get_coupa_client(scope=["core.invoice.read"])
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    resource_name = f"invoices/{invoice_id}"
    invoice_dict = client.get_request(resource_name=resource_name)
    if "errors" in invoice_dict:
        return ToolResponse(success=False, message=coupa_format_error_string(invoice_dict))

    return ToolResponse(
        success=True,
        message="The invoice details were successfully retrieved.",
        content=coupa_build_invoice_from_response(invoice_dict),
    )
