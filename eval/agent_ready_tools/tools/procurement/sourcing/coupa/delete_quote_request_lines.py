from typing import Any, Dict

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_delete_quote_request_lines(quote_request_id: int, line_id: int) -> ToolResponse[bool]:
    """
    Delete Coupa quote requests lines.

    Args:
        quote_request_id: quote request id to be updated
        line_id: line item id to be updated

    Returns:
        boolean weather the update was successful or not
    """

    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    quote_request = client.get_request(resource_name=f"quote_requests/{quote_request_id}")

    if quote_request.get("state") not in {"draft", "new"}:
        return ToolResponse(
            success=False,
            message=f"Cannot delete lines: RFP state is '{quote_request.get('state')}'. Must be 'draft' or 'new'.",
            content=False,
        )

    lines = quote_request.get("lines", [])
    line_ids = {line.get("id") for line in lines}
    if line_id not in line_ids:
        return ToolResponse(
            success=False,
            message=f"Line ID {line_id} not found in quote request {quote_request_id}",
            content=False,
        )

    payload: Dict[str, Any] = {"lines": [{"id": line_id, "_destroy": True}]}

    response = client.put_request(
        resource_name=f"quote_requests/{quote_request_id}", payload=payload
    )

    if "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))

    return ToolResponse(
        success=True, message="The quote lines were successfully deleted", content=True
    )
