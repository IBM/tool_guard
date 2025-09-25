from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_dataclasses import (
    CoupaRequisitionLine,
)
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_helper_functions import (
    coupa_build_requisition_line_from_response,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_update_requisition_line_item(
    requisition_id: int,
    line_num: int,
    description: Optional[str] = None,
    unit_price: Optional[float] = None,
    currency: Optional[str] = None,
    quantity: Optional[float] = None,
    supplier_id: Optional[int] = None,
    billing_account_id: Optional[int] = None,
    item_id: Optional[int] = None,
    unit: Optional[str] = None,
    commodity: Optional[str] = None,
    supplier_part_number: Optional[str] = None,
    shipping_terms: Optional[str] = None,
    payment_terms: Optional[str] = None,
    need_by_date: Optional[str] = None,
    transmission_method: Optional[str] = None,
    manufacturer_name: Optional[str] = None,
    manufacturer_part_number: Optional[str] = None,
) -> ToolResponse[CoupaRequisitionLine]:
    """
    Updates requisition line item from Coupa given a requisition ID and line number.

    Args:
        requisition_id: The ID of the requisition to update the line item from.
        line_num: The line number in the requisition to update.
        description: Optional, The item name of the requisition line in Coupa.
        unit_price: Optional, Price of each unit of the requisition item.
        currency: Optional, Currency for the price of the item of the requisition item.
        quantity: Optional, Quantity of the requisition item.
        supplier_id: Optional, The ID of the supplier in Coupa deployment for which this requisition
            line needs to be procured from.
        billing_account_id: Optional, The ID of the internal org/department account financially
            responsible for the line item (1538).
        item_id: Optional, The ID of the item from the catalog to update the line with.
        unit: Optional, The unit of measure for the requisition item (e.g., "each").
        commodity: Optional, The category or classification of the item (e.g., "MRO", "Beverages").
        supplier_part_number: Optional, The part number for the item as specified by the supplier.
        shipping_terms: Optional, The terms under which the item will be shipped (e.g., "Standard",
            "UPS").
        payment_terms: Optional, The terms under which payment will be made to the supplier (e.g.,
            "2/10 Net 30", "Net 30").
        need_by_date: Optional, The date by which the item is needed, in ISO format (YYYY-MM-DD).
        transmission_method: Optional, The method used to transmit the purchase order to the
            supplier (e.g., "supplier_default").
        manufacturer_name: Optional, The name of the item's manufacturer.
        manufacturer_part_number: Optional, The part number of the item as assigned by the
            manufacturer.

    Returns:
        boolean whether the requisition item was updated successfully or not.
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    requisition = client.get_request(resource_name=f"requisitions/{requisition_id}")
    if "errors" in requisition:
        return ToolResponse(success=False, message=coupa_format_error_string(requisition))

    line_id: Optional[int] = None
    for line in requisition["requisition-lines"]:
        if line["line-num"] == line_num:
            line_id = line["id"]

    if not line_id:
        return ToolResponse(
            success=False,
            message=f"Line number {line_num} not found in requisition {requisition_id}",
        )

    # basically if the value is not None, then add it to the payload - reduces repetitive if statements.
    payload: dict[str, Any] = {
        key: value
        for key, value in {
            "description": description,
            "unit-price": unit_price,
            "currency": {"code": currency} if currency else None,
            "quantity": quantity,
            "account": {"id": billing_account_id} if billing_account_id else None,
            "supplier": {"id": supplier_id} if supplier_id else None,
            "item": {"id": item_id} if item_id else None,
            "uom": {"name": unit} if unit else None,
            "commodity": {"name": commodity} if commodity else None,
            "source-part-num": supplier_part_number,
            "shipping-term": {"code": shipping_terms} if shipping_terms else None,
            "payment-term": {"code": payment_terms} if payment_terms else None,
            "need-by-date": need_by_date,
            "transmission-method-override": transmission_method,
            "manufacturer-name": manufacturer_name,
            "manufacturer-part-number": manufacturer_part_number,
        }.items()
        if value not in (None, "")  # include values like 0 still
    }

    response = client.put_request(resource_name=f"requisition_lines/{line_id}", payload=payload)
    if "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))

    return ToolResponse(
        success=True,
        message="Requisition line updated successfully.",
        content=coupa_build_requisition_line_from_response(response),
    )
