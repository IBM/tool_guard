from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.supplier_management.coupa.supplier_dataclasses import (
    CreateSupplierItemResult,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_create_supplier_item(
    item_id: int,
    supplier_id: int,
    supplier_part_num: str,
    price: float,
    preferred: bool = False,
    currency_code: str = "USD",
) -> ToolResponse[CreateSupplierItemResult]:
    """
    Create a supplier item in Coupa.

    Args:
        item_id: Item's ID.
        supplier_id: Supplier's ID.
        supplier_part_num: Supplier part number.
        price: Price of item
        preferred: Indicates preferred supplier for this item, defaults to False
        currency_code: Currency of transaction, defaults to "USD"

    Returns:
        Result from creating a supplier item.
    """

    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    payload = {
        "item": {"id": item_id},
        "supplier": {"id": supplier_id},
        "price": price,
        "supplier-part-num": supplier_part_num,
        "preferred": preferred,
        "currency": {"code": currency_code},
    }

    response = client.post_request(
        resource_name="supplier_items",
        params={"fields": '["id",{"supplier":["id"]},{"item":["id"]}]'},
        payload=payload,
    )

    if "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))

    return ToolResponse(
        success=True,
        message="Supplier item created",
        content=CreateSupplierItemResult(
            item_id=response["item"]["id"],
            supplier_id=response["supplier"]["id"],
            supplier_item_id=response["id"],
        ),
    )
