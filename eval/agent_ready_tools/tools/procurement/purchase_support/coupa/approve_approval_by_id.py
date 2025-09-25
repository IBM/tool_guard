from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_dataclasses import (
    CoupaApproval,
)
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_helper_functions import (
    coupa_build_approval_from_response,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_approve_approval_by_id(approval_id: int) -> ToolResponse[CoupaApproval]:
    """
    Approves a pending approval in Coupa.

    Args:
        approval_id: The id of the approval.

    Returns:
        The resulting approval after approving.
    """
    # an approved approval is still retrievable by get approval by id
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    response = client.get_request(
        resource_name=f"approvals/{approval_id}",
        params={"fields": '["status", "approvable-type", "approvable-id"]'},
    )
    if "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))

    # check that requisition should be in pending approval status
    if response["approvable-type"] == "RequisitionHeader":
        requisition_id = response["approvable-id"]
        requisition = client.get_request(resource_name=f"requisitions/{requisition_id}")
        if "errors" in response:
            return ToolResponse(success=False, message=coupa_format_error_string(response))

        if requisition["status"] != "pending_approval":
            return ToolResponse(
                success=False,
                message=f"Requisition should be in 'pending_approval' status instead of '{requisition["status"]}'.",
            )

        if requisition.get("current-approval", {}).get("id") != approval_id:
            return ToolResponse(
                success=False,
                message="This approval is not the currently pending approval for this requisition.",
            )

    # should be in this status before approving
    if response["status"] != "pending_approval":
        return ToolResponse(
            success=False, message="Approval status should be in 'pending_approval'."
        )

    response = client.put_request(resource_name=f"approvals/{approval_id}/approve")
    if "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))

    return ToolResponse(
        success=True,
        message="Approved successfully.",
        content=coupa_build_approval_from_response(response),
    )
