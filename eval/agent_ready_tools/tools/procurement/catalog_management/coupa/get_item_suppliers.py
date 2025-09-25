from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@dataclass
class CoupaItemSupplierDetails:
    """Represents an a purchase item."""

    id: int
    name: str
    number: Optional[str] = None
    status: Optional[str] = None


@dataclass
class CoupaSearchSuppliersResponse:
    """Represents an a purchase item."""

    total_count: int
    suppliers: list[CoupaItemSupplierDetails]


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_get_item_suppliers(item_id: str) -> ToolResponse[CoupaSearchSuppliersResponse]:
    """
    search for supplier of an item using item_id.

    Args:
        item_id: The search item.

    Returns:
        suppliers of the item.
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failed to retrieve credentials.")

    params = {"fields": '[{"supplier":["id","name","number","status"]}]'}

    response = client.get_request_list(
        resource_name=f"items/{item_id}/supplier_items", params=params
    )
    if len(response) == 1 and "errors" in response[0]:
        return ToolResponse(success=False, message=coupa_format_error_string(response[0]))

    if len(response) == 0:
        return ToolResponse(
            success=True, message="There are no suppliers for this item in the system"
        )

    result = CoupaSearchSuppliersResponse(
        total_count=len(response),
        suppliers=[
            CoupaItemSupplierDetails(
                id=r["supplier"].get("id", 0),
                name=r["supplier"].get("name", ""),
                number=r["supplier"].get("number", None),
                status=r["supplier"].get("status", None),
            )
            for r in response
            if "supplier" in r
        ],
    )

    return ToolResponse(
        success=True, message="Following is the list of suppliers for the item.", content=result
    )
