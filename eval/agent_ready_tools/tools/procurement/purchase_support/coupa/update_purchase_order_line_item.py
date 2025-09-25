import json
from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_dataclasses import (
    CoupaPurchaseOrder,
)
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_helper_functions import (
    coupa_build_purchase_order_from_response,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_update_purchase_order_line_item(
    purchase_order_id: int,
    line_num: int,
    order_line_description: Optional[str] = None,
    item_description: Optional[str] = None,
    quantity: Optional[str] = None,
    unit: Optional[str] = None,
    price: Optional[str] = None,
    need_by_date: Optional[str] = None,
    supplier_part_number: Optional[str] = None,
    supplier_auxiliary_part_number: Optional[str] = None,
    commodity: Optional[str] = None,
    savings_percent: Optional[float] = None,
    manufacturer_name: Optional[str] = None,
    manufacturer_part_number: Optional[int] = None,
    billing_account_id: Optional[int] = None,
    period: Optional[str] = None,
) -> ToolResponse[CoupaPurchaseOrder]:
    """
    Updates purchase order information from Coupa by ID.

    Args:
        purchase_order_id: The ID of the purchase order in Coupa.
        line_num: The line number of the PO line to update (not the internal ID).
        order_line_description: Optional. Description of the order line.
        item_description: Optional. Description of the item.
        quantity: Optional. Quantity of items.
        unit: Optional. Unit of measure.
        price: Optional. Price per unit.
        need_by_date: Optional. The date the items are needed by.
        supplier_part_number: Optional. Supplier part number.
        supplier_auxiliary_part_number: Optional. Supplier auxiliary part number.
        commodity: Optional. Commodity code or name.
        savings_percent: Optional. Percentage of savings expected.
        manufacturer_name: Optional. Manufacturer name.
        manufacturer_part_number: Optional. Manufacturer part number.
        billing_account_id: Optional. ID of the billing account to charge.
        period: Optional. Time period for the order line.

    Returns:
        True if the purchase order line item was updated successfully, otherwise False.
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params = {
        "order-header[po-number]": purchase_order_id,
        "fields": json.dumps(["id"]),
        "line-num": line_num,
    }

    get_response = client.get_request_list("purchase_order_lines", params=params)
    if len(get_response) == 0:
        return ToolResponse(success=False, message="No purchase order lines found.")
    if "errors" in get_response[0]:
        return ToolResponse(success=False, message=coupa_format_error_string(get_response[0]))

    order_line_id = get_response[0]["id"]  # originally in a list because of query

    item = {
        "description": item_description,
        "uom": {"name": unit} if unit else None,
    }
    item = {key: value for key, value in item.items() if value is not None}

    line_payload = {
        "id": order_line_id,
        "description": order_line_description,
        "quantity": quantity,
        "price": price,
        "item": item if item else None,
        "source-part-num": supplier_part_number,
        "supp-aux-part-num": supplier_auxiliary_part_number,
        "commodity": {"name": commodity} if commodity else None,
        "manufacturer-name": manufacturer_name,
        "manufacturer-part-number": manufacturer_part_number,
        "need-by-date": need_by_date,
        "savings-pct": savings_percent,
        "account": {"id": billing_account_id} if billing_account_id else None,
        "period": {"name": period} if period else None,
    }
    line_payload = {key: value for key, value in line_payload.items() if value not in (None, "")}

    payload: dict[str, Any] = {"order-lines": [line_payload]}

    update_response = client.put_request(f"purchase_orders/{purchase_order_id}", payload=payload)
    if "errors" in update_response:
        return ToolResponse(success=False, message=coupa_format_error_string(update_response))

    return ToolResponse(
        success=True,
        message="Purchase order line updated successfully.",
        content=coupa_build_purchase_order_from_response(update_response),
    )
