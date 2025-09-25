from typing import Any, Dict, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.ariba_client import get_ariba_client
from agent_ready_tools.clients.clients_enums import AribaApplications
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.tool_credentials import ARIBA_BUYER_CONNECTIONS


@dataclass
class AribaOrderLine:
    """Represents an individual purchase order line item for a purchase order in SAP Ariba."""

    order_line_id: str
    order_line_description: str
    order_line_type: Optional[str]
    order_line_num: int
    quantity: Optional[int]
    unit: Optional[str]
    price: float
    total: str
    supplier_part_number: Optional[str]
    manufacturer_name: Optional[str]
    manufacturer_part_number: Optional[str]
    address: Optional[str]
    city: Optional[str]
    postal_code: Optional[str]
    state: Optional[str]
    country: Optional[str]
    need_by_date: Optional[str] = None


@dataclass
class AribaOrderLines:
    """Represents the list of purchase order line items for a particular purchase order in Ariba."""

    order_lines: List[AribaOrderLine]


def build_ariba_purchase_order_line_item_from_response(
    response: Dict[str, Any],
) -> AribaOrderLines:
    """
    Processes and wraps an purchase order line item  API response.

    Args:
        response: Purchase order line item by id API response

    Returns:
        A structured purchase order line items dictionary containing transformed data
    from the original API response.
    """
    order_lines = AribaOrderLines(
        # total is not computed as tax / discount details are not available in API response
        order_lines=[
            AribaOrderLine(
                order_line_id=f'{order_line.get("documentNumber", "")}-{order_line.get("lineNumber", 0)}',
                order_line_description=order_line.get("description", ""),
                order_line_type=order_line.get("partType", ""),
                order_line_num=order_line.get("lineNumber", ""),
                quantity=order_line.get("quantity", None),
                unit=order_line.get("unitPrice", {}).get("currencyCode", {}),
                price=order_line.get("unitPrice", {}).get("amount", ""),
                total="0",  #  TODO
                supplier_part_number=order_line.get("supplierPart", ""),
                manufacturer_name=(
                    order_line.get("manufacturerName").get("value", "")
                    if isinstance(order_line.get("manufacturerName"), dict)
                    else ""
                ),
                manufacturer_part_number=order_line.get("manufacturerPartId", ""),
                # Shipping Address
                address=order_line.get("itemShipToStreet", ""),
                city=order_line.get("itemShipToCity", ""),
                postal_code=order_line.get("itemShipToPostalCode", ""),
                state=order_line.get("itemShipToState", ""),
                country=order_line.get("itemShipToCountry", ""),
                need_by_date=order_line.get("needBy", None),
            )
            for order_line in response.get("content", [])
        ]
    )

    return order_lines


@tool(expected_credentials=ARIBA_BUYER_CONNECTIONS)
def ariba_get_purchase_order_line_items_by_po_id(
    purchase_order_id: str,
) -> ToolResponse[AribaOrderLines]:
    """
    Gets a purchase order line item's details using purchase order line item id in Ariba.

    Args:
        purchase_order_id: The id of the purchase order line item.

    Returns:
        The resulting transformed purchase order item details after using the id to retrieve, from
        Ariba.
    """
    # Setting the application name to BUYER from ariba_client.py,
    # as this tool operates with these credentials.
    try:
        client = get_ariba_client(application=AribaApplications.BUYER)
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials.")

    endpoint = "purchase-orders/v1/prod/items"
    params = {
        "$filter": f"documentNumber eq '{purchase_order_id}'",
    }

    response = client.get_request(endpoint=endpoint, params=params)

    if "error" in response or "message" in response:
        content = response.get("message", "")
        return ToolResponse(
            success=False,
            message=f"Request unsuccessful {content}",
        )

    content = build_ariba_purchase_order_line_item_from_response(response)

    return ToolResponse(
        success=True,
        message="The data was successfully retrieved",
        content=content,
    )
