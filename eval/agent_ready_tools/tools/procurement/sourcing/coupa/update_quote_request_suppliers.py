from typing import Any, Dict, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_update_quote_request_suppliers(
    quote_request_id: int,
    supplier_name: str,
    supplier_email: str,
    supplier_contact_name: Optional[str] = None,
) -> ToolResponse[bool]:
    """
    Update Coupa quote requests suppliers.

    Args:
        quote_request_id: quote request id to be updated in Coupa
        supplier_name: quote request supplier  name to be updated in Coupa
        supplier_email: quote request supplier email to be updated in Coupa
        supplier_contact_name: quote request supplier contact name to be updated in Coupa

    Returns:
        boolean weather the update was successful or not
    """

    supplier_payload: Dict[str, Any] = {
        key: value
        for key, value in {
            "name": supplier_name,
            "contact-name": supplier_contact_name,
            "email": supplier_email,
        }.items()
        if value is not None
    }
    payload: dict[str, Any] = {"quote-suppliers": [supplier_payload]}

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
        success=True, message="The quote details were successfully updated", content=True
    )
