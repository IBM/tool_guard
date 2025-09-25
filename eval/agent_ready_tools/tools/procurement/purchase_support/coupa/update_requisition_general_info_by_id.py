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
def coupa_update_requisition_general_info_by_id(
    requisition_id: int,
    requested_by: Optional[str] = None,
    business_unit: Optional[str] = None,
    business_purpose: Optional[str] = None,
    need_by_date: Optional[str] = None,
) -> ToolResponse[CoupaRequisition]:
    """
    Updates general requisition information from Coupa by ID.

    Args:
        requisition_id: The ID of the requisition in Coupa.
        requested_by: Optional, The person who requested the requisition.
        business_unit: Optional, The business unit of the requisition - unmodifiable after
            requisition is approved -> purchase order.
        business_purpose: Optional, The business purpose of the requisition - unmodifiable after
            requisition is approved -> purchase order.
        need_by_date: Optional, The date by which the item is needed, in ISO format (YYYY-MM-DD).

    Returns:
        boolean whether the requisition was updated successfully or not.
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    # NOTE: business purpose and business unit are unmodifiable after requisition is approved -> purchase order
    payload: dict[str, Any] = {
        key: value
        for key, value in {
            "justification": business_purpose,
            "department": {"name": business_unit} if business_unit else None,
            "requested_by": {"login": requested_by} if requested_by else None,
            "need-by-date": need_by_date,
        }.items()
        if value not in (None, "")
    }
    # NOTE: assigned_to not found in payload and unable to do anything related to assignments AFAIK

    response = client.put_request(resource_name=f"requisitions/{requisition_id}", payload=payload)
    if "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))

    return ToolResponse(
        success=True,
        message="Requisition updated successfully.",
        content=coupa_build_requisition_from_response(response),
    )
