from typing import Any, Dict, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.sourcing.coupa.common_classes_sourcing import LinesType
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_update_quote_request_lines(
    quote_request_id: int,
    line_id: Optional[int] = None,
    line_type: Optional[str] = None,
    line_quantity: Optional[str] = None,
    line_need_by_date: Optional[str] = None,
    line_description: Optional[str] = None,
    line_price_currency_code: Optional[str] = None,
    line_price_amount: Optional[str] = None,
) -> ToolResponse[bool]:
    """
    Update Coupa quote requests lines.

    Args:
        quote_request_id: quote request id to be updated
        line_id: line item id to be updated
        line_type: The line type of item in Coupa
        line_quantity: the quantity of items in Coupa
        line_need_by_date: The date that item is needed
        line_description: description to be added in Coupa
        line_price_currency_code: The currency if item in Coupa
        line_price_amount: The price amount of the item in the Coupa.

    Returns:
        boolean weather the update was successful or not
    """

    line_payload: Dict[str, Any] = {
        key: value
        for key, value in {
            "id": line_id,
            "type": LinesType[line_type.strip().upper()].value if line_type else None,
            "quantity": line_quantity,
            "description": line_description,
            "price-amount": line_price_amount,
            "need-by-date": line_need_by_date,
            "price-currency": (
                {"code": line_price_currency_code} if line_price_currency_code else None
            ),
        }.items()
        if value not in (None, "", "null")
    }

    payload: dict[str, Any] = {"lines": [line_payload]}

    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    response = client.put_request(
        resource_name=f"quote_requests/{quote_request_id}", payload=payload
    )

    if "errors" in response:
        return ToolResponse(
            success=False, message=coupa_format_error_string(response), content=None
        )

    return ToolResponse(
        success=True, message="The quote request line was successfully updated", content=True
    )
