from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_void_a_receipt(receipt_id: int) -> ToolResponse[bool]:
    """
    void_a_receipt.

    Args:
        receipt_id: a unique receipt identifier

    Returns:
        an receipt retrieved
    """
    try:
        client = get_coupa_client(
            scope=["core.inventory.receiving.read", "core.inventory.receiving.write"]
        )
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    resource_name = f"receiving_transactions/{receipt_id}/void"
    response = client.put_request(resource_name=resource_name)
    if "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))

    return ToolResponse(success=True, message="The receipt was successfully voided.", content=True)
