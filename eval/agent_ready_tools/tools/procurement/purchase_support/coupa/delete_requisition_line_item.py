from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_delete_requisition_line_item(requisition_id: int, line_num: int) -> ToolResponse:
    """
    Deletes requisition line item from Coupa given a requisition ID and line number.

    Args:
        requisition_id: The ID of the requisition to update the line item from.
        line_num: The line number in the requisition to update.

    Returns:
        boolean whether the requisition item was updated successfully or not.
    """
    client = get_coupa_client()

    requisition = client.get_request(resource_name=f"requisitions/{requisition_id}")
    if "errors" in requisition:
        return ToolResponse(success=False, message=coupa_format_error_string(requisition))

    line_id: Optional[int] = None
    for line in requisition["requisition-lines"]:
        if line["line-num"] == line_num:
            line_id = line["id"]

    if not line_id:
        return ToolResponse(
            success=False,
            message=f"Line number {line_num} not found in requisition {requisition_id}",
        )

    response = client.delete_request(resource_name=f"requisition_lines/{line_id}")
    if isinstance(response, dict) and "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))

    return ToolResponse(
        success=True, message="Requisition line deleted successfully", content=response
    )
