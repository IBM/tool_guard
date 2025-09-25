import json
from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.invoice_management.coupa.common_classes_invoice_management import (
    CoupaPOReceipt,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_get_purchase_order_receipts(purchase_order_id: int) -> ToolResponse[List[CoupaPOReceipt]]:
    """
    Returns a list of receipt IDs for a given purchase order in Coupa.

    Args:
        purchase_order_id: The ID of the purchase order.

    Returns:
        CoupaPOReceipt containing details of receipt against a Purchase Order.

    Raises:
        ValueError: If the API response is not a valid JSON or does not match the expected data
            structure.
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params = {
        "order-line[order-header-id]": purchase_order_id,
        "fields": json.dumps(
            [
                "id",
                "status",
                "type",
                "price",
                "quantity",
                "total",
                "created-at",
                {
                    "order_line": [
                        "id",
                        "order-header-id",
                        "line-num",
                        "name",
                        "status",
                        "description",
                        "price",
                        "quantity",
                    ]
                },
            ]
        ),
    }
    response = client.get_request_list(resource_name="receiving_transactions", params=params)
    if len(response) == 1 and "errors" in response[0]:
        return ToolResponse(success=False, message=coupa_format_error_string(response[0]))

    if len(response) == 0:
        return ToolResponse(
            success=True,
            message=f"There are no receipts associated with the purchase order {purchase_order_id}.",
        )

    result = [
        CoupaPOReceipt(
            order_id=r.get("order-line", {}).get("order-header-id"),
            line_id=r.get("order-line", {}).get("id"),
            line_number=r.get("order-line", {}).get("line-num"),
            description=r.get("order-line", {}).get("description"),
            receipt_id=r.get("id"),
            receipt_status=r.get("status"),
            created_at=r.get("created-at"),
            order_price=r.get("order-line", {}).get("price"),
            receipt_price=r.get("price"),
            order_quantity=r.get("order-line", {}).get("quantity"),
            receipt_quantity=r.get("quantity"),
        )
        for r in response
    ]

    return ToolResponse(
        success=True,
        message="Following is the details of receipts for the purchase order",
        content=result,
    )
