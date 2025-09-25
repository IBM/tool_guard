from typing import Any, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_dataclasses import (
    CoupaRequisition,
    CoupaRequisitionList,
)
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_helper_functions import (
    coupa_build_requisition_from_response,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_get_all_requisitions(
    status: Optional[str] = None,
    department: Optional[str] = None,
    created_by: Optional[str] = None,
    created_at_start: Optional[str] = None,
    created_at_end: Optional[str] = None,
    order_by_direction: str = "desc",
    limit: int = 10,
    offset: int = 0,
) -> ToolResponse[CoupaRequisitionList]:
    """
    Get all requisitions in Coupa.

    Args:
        status: The status of the requisition ("draft", "pending_approval", etc.).
        department: The department name that the requisition is associated with ("Operations",
            etc.).
        created_by: The user login that created the requisition.
        created_at_start: The start of the date range for getting requisitions (YYYY-MM-DD).
        created_at_end: The end of the date range for getting requisitions (YYYY-MM-DD).
        order_by_direction: The direction in which the requisitions will be ordered, ("asc" or
            "desc").
        limit: Optional, the count of requisitions to return - default 10.
        offset: Optional, the number of entries to offset by for pagination - default 0.

    Returns:
        The retrieved list of requisitions in this Coupa instance.
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params: dict[str, Any] = {
        key: value
        for key, value in {
            "limit": limit,
            "offset": offset,
            "order_by": "created-at",
            "dir": order_by_direction,
            "status": status,
            "department[name]": department,
            "created-by[login]": created_by,
            "created-at[gt]": created_at_start,
            "created-at[lt]": created_at_end,
        }.items()
        if value not in (None, "")
    }

    response = client.get_request_list(resource_name="requisitions", params=params)
    if len(response) == 0:
        return ToolResponse(success=False, message="No requisitions found.")

    if "errors" in response[0]:
        return ToolResponse(success=False, message=coupa_format_error_string(response[0]))

    requisition_list: List[CoupaRequisition] = []
    for requisition in response:
        requisition_list.append(coupa_build_requisition_from_response(requisition))

    return ToolResponse(
        success=True,
        message="Requisitions retrieved successfully.",
        content=CoupaRequisitionList(requisition_list=requisition_list),
    )
