from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_dataclasses import (
    CoupaRequisition,
)
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_helper_functions import (
    coupa_build_requisition_from_response,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_add_item_to_requisition(
    requisition_id: int,
    billing_account_id: int,
    description: Optional[str] = None,
    unit_price: Optional[float] = None,
    supplier_id: Optional[int] = None,
    quantity: Optional[int] = None,
    item_id: Optional[int] = None,
    currency: Optional[str] = None,
    unit: Optional[str] = None,
    commodity: Optional[str] = None,
    supplier_part_number: Optional[str] = None,
    shipping_terms: Optional[str] = None,
    payment_terms: Optional[str] = None,
    need_by_date: Optional[str] = None,
    transmission_method: Optional[str] = None,
    manufacturer_name: Optional[str] = None,
    manufacturer_part_number: Optional[str] = None,
) -> ToolResponse[CoupaRequisition]:
    """
    Adds an item to an existing requisition in Coupa, using either a catalog item (item_id) or
    manual item fields.

    Args:
        requisition_id: ID of the requisition to which item will be added. It uniquely identifies a
            requisition in Coupa deployment.
        billing_account_id: Optional, The ID of the internal org/department account financially
            responsible for the line item (1538).
        description: Description of the item to be added to the requisition.
        unit_price: Price of each unit of the requisition item.
        supplier_id: The ID of the supplier in Coupa deployment for which this requisition line
            needs to be procured from.
        quantity: Optional, Quantity of the requisition item. (changes line type to
            RequisitionQuantityLine automatically
        item_id: The ID of the catalog item if provided.
        currency: Optional, Currency for the price of the item of the requisition item.
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
        The resulting requisition after submitting the requisition update request.
    """
    try:
        client = get_coupa_client(scope=["core.requisition.read", "core.requisition.write"])
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    is_catalog_flow = item_id is not None

    # Validation logic
    if is_catalog_flow:
        if not quantity:  # catalog items need quantities, RequisitionQuantityLine
            return ToolResponse(
                success=False, message="When using item_id, 'quantity' is required."
            )
    else:  # RequisitionAmountLine if no quantity or RequisitionQuantityLine
        if not all(
            [description, unit_price, supplier_id]
        ):  # need all 3 of these to manually enter an item at minimum
            return ToolResponse(
                success=False,
                message="To manually add an item (without item_id), 'description', 'unit_price', and 'supplier_id' are required.",
            )

    requisition_line: dict[str, Any] = {
        "account": {"id": billing_account_id},  # always need billing account id regardless
    }

    if is_catalog_flow:  # only use the item id
        requisition_line["item"] = {"id": item_id}
    else:  # manual item add
        requisition_line.update(
            {
                "description": description,
                "unit-price": unit_price,
                "supplier": {"id": supplier_id} if supplier_id else None,
            }
        )

    optional_fields = {
        "quantity": quantity,  # necessary for catalog item or 2. optional for manual item
        "currency": {"code": currency} if currency else None,
        "uom": {"name": unit} if unit else None,
        "commodity": {"name": commodity} if commodity else None,
        "source-part-num": supplier_part_number,
        "shipping-term": {"code": shipping_terms} if shipping_terms else None,
        "payment-term": {"code": payment_terms} if payment_terms else None,
        "need-by-date": need_by_date,
        "transmission-method-override": transmission_method,
        "manufacturer-name": manufacturer_name,
        "manufacturer-part-number": manufacturer_part_number,
    }

    requisition_line.update(
        {key: value for key, value in optional_fields.items() if value not in (None, "")}
    )

    payload = {"requisition-lines": [requisition_line]}

    response = client.put_request(resource_name=f"requisitions/{requisition_id}", payload=payload)
    if "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))

    return ToolResponse(
        success=True,
        message="Item was added successfully.",
        content=coupa_build_requisition_from_response(response=response),
    )
