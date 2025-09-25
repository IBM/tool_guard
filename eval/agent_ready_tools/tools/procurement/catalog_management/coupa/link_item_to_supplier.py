from enum import StrEnum
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


class CoupaItemAvailabilityStatus(StrEnum):
    """Enum specifying the availabilty status of the item in Coupa."""

    IN_STOCK = "in_stock"
    OUT_OF_STOCK = "out_of_stock"
    BACKORDERED = "backordered"


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_link_item_to_supplier(
    supplier_id: str,
    item_id: str,
    price: str,
    currency_code: str,
    saving_percentage: Optional[str] = None,
    availability: Optional[CoupaItemAvailabilityStatus] = None,
    availability_date: Optional[str] = None,
    manufacturer: Optional[str] = None,
    contract_id: Optional[str] = None,
    minimum_order_quantity: Optional[str] = None,
    part_number: Optional[str] = None,
    auxiliary_part_number: Optional[str] = None,
) -> ToolResponse[int]:
    """
    Links an item to a supplier in Coupa.

    Args:
        supplier_id: The id of the supplier, returned by coupa_get_all_suppliers tool.
        item_id: The internal id of the item in coupa.
        price: The price of the item.
        currency_code: Specifies The currency code in ISO 4217 standard.
        saving_percentage: The percentage of savings for the item.
        availability: The item's availability status.
        availability_date: The date when the item becomes available, in ISO 8601 format.
        manufacturer: The name of the item's manufacturer.
        contract_id: The id of the contract.
        minimum_order_quantity: The minimum quantity required to order the item.
        part_number: The unique part number of the item.
        auxiliary_part_number: The unique auxiliary part number of the item.

    Returns:
        The item details, including its associated suppliers.
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failed to retrieve credentials.")

    payload = {
        "item": {"id": item_id},
        "price": price,
        "currency": {"code": currency_code},
        "supplier": {"id": supplier_id},
        "savings-pct": saving_percentage,
        "availability": (
            CoupaItemAvailabilityStatus[availability.upper()].value if availability else None
        ),
        "availability-date": availability_date,
        "manufacturer": manufacturer,
        "supplier-part-num": part_number,
        "supplier-aux-part-num": auxiliary_part_number,
        "minimum-order-quantity": minimum_order_quantity,
        "contract": {"id": contract_id} if contract_id else None,
    }

    payload = {key: value for key, value in payload.items() if value}

    response = client.post_request(resource_name="supplier_items", payload=payload)
    if "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))

    if "id" not in response:
        return ToolResponse(
            success=False, message="There was an issue linking the item to the supplier."
        )

    return ToolResponse(
        success=True,
        message="The item was successfully linked to the supplier.",
        content=response.get("id"),
    )
