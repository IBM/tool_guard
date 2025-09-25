from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.supplier_management.coupa.supplier_dataclasses import (
    CoupaSupplierItemDetails,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS

QUERY_FIELDS = '["id",{"supplier":["id","name","number"]},{"item": ["id","name","item-number","description","storage-quantity","consumption-quantity","active"]},{"custom_fields": {}}]'


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_get_supplier_items_by_supplier_id(
    supplier_id: str,
) -> ToolResponse[List[CoupaSupplierItemDetails]]:
    """
    Get all items for a specified supplier by id.

    Args:
        supplier_id: The id of the supplier

    Returns:
        A list supplier items.
    """

    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failed to retrieve credentials.")

    params = {
        "fields": QUERY_FIELDS,
        "supplier[id]": supplier_id,
    }

    response = client.get_request_list(
        resource_name="supplier_items",
        params=params,
    )
    if len(response) == 1 and "errors" in response[0]:
        return ToolResponse(success=False, message=coupa_format_error_string(response[0]))

    if len(response) == 0:
        return ToolResponse(
            success=True, message="There are no items for this supplier", content=[]
        )

    supplier_items = []
    for supplier_item in response:
        supplier_items.append(
            CoupaSupplierItemDetails(
                item_id=supplier_item.get("item", {}).get("id"),
                item_name=supplier_item.get("item", {}).get("name"),
                item_number=supplier_item.get("item", {}).get("item-number"),
                is_active=supplier_item.get("item", {}).get("active"),
                description=supplier_item.get("item", {}).get("description"),
                storage_quantity=supplier_item.get("item", {}).get("storage-quantity"),
                consumption_quantity=supplier_item.get("item", {}).get("consumption-quantity"),
                supplier_id=supplier_item.get("supplier", {}).get("id"),
                supplier_name=supplier_item.get("supplier", {}).get("name"),
                supplier_number=supplier_item.get("supplier", {}).get("number"),
            )
        )

    return ToolResponse(
        success=True, message="Following is the list of supplier items", content=supplier_items
    )
