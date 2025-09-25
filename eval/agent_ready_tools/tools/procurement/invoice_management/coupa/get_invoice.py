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
def coupa_get_invoice(invoice_number: str) -> ToolResponse[CoupaInvoice]:
    """
    Read/retrieve an invoice.

    Args:
        invoice_number: an invoice number (alphanumeric)

    Returns:
        corresponding invoice retrieved
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    resource_name = "invoices/"
    invoice_number = invoice_number.strip()
    params = {"invoice-number": invoice_number}
    response_list = client.get_request_list(resource_name=resource_name, params=params)
    if len(response_list) == 1 and "errors" in response_list[0]:
        return ToolResponse(success=False, message=coupa_format_error_string(response_list[0]))

    if len(response_list) == 0:
        return ToolResponse(
            success=True, message="There are no invoices that match with the provided invoice id."
        )
    if len(response_list) > 1:
        return ToolResponse(success=False, message="There are multiple invoices with this number.")

    return ToolResponse(
        success=True,
        message=f"Following are the details of the invoice that matches {invoice_number}",
        content=coupa_build_invoice_from_response(response_list[0]),
    )
