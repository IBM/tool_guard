from typing import Any, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.invoice_management.coupa.common_classes_invoice_management import (
    CoupaReceiptHeader,
)
from agent_ready_tools.tools.procurement.invoice_management.coupa.helper_functions_invoice_management import (
    coupa_build_receipt_header_from_response,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_view_all_receipts(
    created_by: Optional[str] = None,
    created_at_start: Optional[str] = None,
    created_at_end: Optional[str] = None,
    order_by_direction: str = "desc",
    limit: int = 10,
    offset: int = 0,
) -> ToolResponse[List[CoupaReceiptHeader]]:
    """
    View all completed receipts in Coupa.

    Args:
        created_by: The user login of the person who created the invoice.
        created_at_start: The start of the date range for getting invoices (YYYY-MM-DD).
        created_at_end: The end of the date range for getting invoices (YYYY-MM-DD).
        order_by_direction: The direction in which the invoices will be ordered, ("asc" or "desc").
        limit: Optional, the count of invoices to return - default 10.
        offset: Optional, the number of entries to offset by for pagination - default 0.

    Returns:
        List of completed receipts in Coupa.
    """
    try:
        client = get_coupa_client(scope=["core.inventory.receiving.read"])
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params: dict[str, Any] = {
        key: value
        for key, value in {
            "limit": limit,
            "offset": offset,
            "order_by": "created-at",
            "dir": order_by_direction,
            "created-by[login]": created_by,
            "created-at[gt]": created_at_start,
            "created-at[lt]": created_at_end,
        }.items()
        if value is not None
    }

    response = client.get_request_list(resource_name="receiving_transactions", params=params)
    if len(response) == 1 and "errors" in response[0]:
        return ToolResponse(success=False, message=coupa_format_error_string(response[0]))

    receipt_header_list = []
    for receipt in response:
        receipt_header = coupa_build_receipt_header_from_response(receipt)
        receipt_header_list.append(receipt_header)

    return ToolResponse(
        success=True, message="Following is the list of all receipts.", content=receipt_header_list
    )
