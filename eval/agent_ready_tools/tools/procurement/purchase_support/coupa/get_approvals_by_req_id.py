from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_dataclasses import (
    CoupaApprovalList,
)
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_helper_functions import (
    coupa_build_approval_from_response,
    coupa_build_requisition_from_response,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_get_approvals_by_req_id(requisition_id: int) -> ToolResponse[CoupaApprovalList]:
    """
    Gets a list of approvals by requisition id in Coupa.

    Args:
        requisition_id: The id of the requisition.

    Returns:
        The list of approvals after retrieving with requisition_id.
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    response = client.get_request(resource_name=f"requisitions/{requisition_id}")
    if "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))

    requisition = coupa_build_requisition_from_response(response)

    if not requisition.approval_id_list:
        return ToolResponse(success=False, message="Approval ID list should be populated")

    approval_list = []
    for approval_id in requisition.approval_id_list:
        approval = client.get_request(resource_name=f"approvals/{approval_id}")
        if "errors" in approval:
            return ToolResponse(success=False, message=coupa_format_error_string(approval))
        approval_list.append(coupa_build_approval_from_response(response=approval))

    return ToolResponse(
        success=True,
        message="Approvals retrieved successfully.",
        content=CoupaApprovalList(approval_list=approval_list),
    )
