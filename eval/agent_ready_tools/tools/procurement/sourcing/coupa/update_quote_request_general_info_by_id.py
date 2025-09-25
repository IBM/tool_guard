from typing import Any, Dict, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_update_quote_request_general_info_by_id(
    quote_request_id: int,
    description: Optional[str] = None,
    comments: Optional[str] = None,
    event_type: Optional[str] = "rfp",
    commodity_name: Optional[str] = None,
    currency_code: Optional[str] = None,
) -> ToolResponse[bool]:
    """
    Update Coupa quote requests general info.

    Args:
        quote_request_id: Quote request id in Coupa.
        description: Descriptions to be updated in quote request in Coupa.
        comments: Comments to be added in updated quote request in Coupa.
        event_type: Event Type in quote request default is 'RFP' in Coupa.
        commodity_name: Commodity name to get update in Coupa quote request.
        currency_code: Currency code to get update in quote request in Coupa.

    Returns:
        str with a success or fail message.
    """

    payload: Dict[str, Any] = {
        key: value
        for key, value in {
            "description": description,
            "event-type": event_type,
            "comments": comments,
            "commodity": {"name": commodity_name} if commodity_name else None,
            "currency": {"code": currency_code} if currency_code else None,
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
        return ToolResponse(
            success=False, message=coupa_format_error_string(response), content=None
        )
    return ToolResponse(
        success=True,
        message=f"Quote request details of {quote_request_id} updated successfully.",
        content=True,
    )
