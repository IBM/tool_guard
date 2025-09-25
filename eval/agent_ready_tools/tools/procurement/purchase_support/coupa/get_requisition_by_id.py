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
def coupa_get_requisition_by_id(requisition_id: int) -> ToolResponse[CoupaRequisition]:
    """
    Retrieves requisition from Coupa by ID.

    Args:
        requisition_id: The ID of the requisition in Coupa.

    Returns:
        The retrieved Coupa Requisition.
    """
    try:
        client = get_coupa_client(scope=["core.requisition.read"])
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")
    response = client.get_request(resource_name=f"requisitions/{requisition_id}")
    if "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))

    return ToolResponse(
        success=True,
        message="Requisition retrieved successfully.",
        content=coupa_build_requisition_from_response(response),
    )
