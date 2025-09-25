from typing import Any, Dict, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.date_conversion import convert_str_to_coupa_time
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_update_quote_request_timeline(
    quote_request_id: int,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    start_on_submit: Optional[bool] = None,
) -> ToolResponse[bool]:
    """
    Update Coupa quote requests general info.

    Args:
        quote_request_id: Quote request id in Coupa.
        start_time: A timezone representing the new start
        end_time: A timezone representing the new end
        start_on_submit: If provided, toggles whether the RFP should start immediately on submit.

    Returns:
        Boolean weather the result is successful or not.
    """

    payload: Dict[str, Any] = {
        key: value
        for key, value in {
            "start-time": convert_str_to_coupa_time(start_time) if start_time else None,
            "end-time": convert_str_to_coupa_time(end_time) if end_time else None,
            "start-on-submit": start_on_submit,
        }.items()
        if value not in (None, "", "null")
    }

    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    response = client.put_request(
        resource_name=f"quote_requests/{quote_request_id}", payload=payload
    )

    if "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))

    return ToolResponse(
        success=True,
        message=f"Quote request {quote_request_id} timeline was successfully updated.",
        content=True,
    )
