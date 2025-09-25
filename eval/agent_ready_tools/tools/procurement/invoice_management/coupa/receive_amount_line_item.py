from typing import Any, Dict

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@dataclass
class CoupaReceiveAmountLineItemResponse:
    """Represents a response from receiving a purchase order line item."""

    receipt_id: int


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_receive_amount_line_item(
    po_id: int,
    line_number: int,
    receipt_date: str,
    amount: float = -1.0,
) -> ToolResponse[CoupaReceiveAmountLineItemResponse]:
    """
    receive a purchase order line item.

    Args:
        po_id: a unique purchase order id
        line_number: line number of the purchase order
        receipt_date: receipt date
        amount: amount received

    Returns:
        CoupaReceiveAmountLineItemResponse
    """
    try:
        client = get_coupa_client(
            scope=[
                "core.purchase_order.read",
                "core.inventory.receiving.read",
                "core.inventory.receiving.write",
            ]
        )
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    resource_name_po = "purchase_order_lines"
    params = {
        "order-header-id": f"{po_id}",
        "line-num": f"{line_number}",
        "fields": '["id", "price"]',
    }
    response = client.get_request_list(resource_name=resource_name_po, params=params)
    if len(response) == 1 and "errors" in response[0]:
        return ToolResponse(success=False, message=coupa_format_error_string(response[0]))

    if len(response) == 0:
        return ToolResponse(
            success=False,
            message=f"There are no line items with line number {line_number} in this purchase order.",
        )

    response_purchase_order_line: Dict[str, Any] = response[0]
    order_line_id = response_purchase_order_line["id"]
    if amount == -1.0:
        try:
            amount_from_line: Any = response_purchase_order_line.get("price")
            assert amount_from_line
            amount = float(amount_from_line)  # receiving all
        except (AssertionError, ValueError):
            return ToolResponse(
                success=False,
                message=f"Exception in converting price ({amount_from_line}) from line item",
            )

    resource_name_receiving = "receiving_transactions"
    data = {
        "order-line": {
            "id": order_line_id,
        },
        "price": amount,
        "type": "ReceivingAmountConsumption",
    }
    if receipt_date:
        data.update({"transaction-date": receipt_date})
    response_receiving = client.post_request(resource_name=resource_name_receiving, payload=data)
    if "errors" in response_receiving:
        return ToolResponse(success=False, message=coupa_format_error_string(response_receiving))

    return ToolResponse(
        success=True,
        message="Line item was successfully received.",
        content=CoupaReceiveAmountLineItemResponse(receipt_id=response_receiving["id"]),
    )
