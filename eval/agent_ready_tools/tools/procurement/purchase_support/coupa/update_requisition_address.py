from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_dataclasses import (
    CoupaAddress,
)
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_helper_functions import (
    coupa_build_address,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_update_requisition_address(
    requisition_id: int,
    street1: Optional[str] = None,
    city: Optional[str] = None,
    postal_code: Optional[str] = None,
    state: Optional[str] = None,
    country_code: Optional[str] = None,  # 2-letter ISO
) -> ToolResponse[CoupaAddress]:
    """
    Updates an existing address of a requisition in Coupa.

    Args:
        requisition_id: The Coupa ID of the requisition to update (required).
        street1: Required first street line.
        city: Required if providing full address.
        postal_code: Required if providing full address.
        state: Optional state/province.
        country_code: Required if providing full address.

    Returns:
        The resulting address after updating it.
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    response = client.get_request(resource_name=f"requisitions/{requisition_id}")
    if "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))
    address_id = (
        response.get("ship-to-address", {}).get("id") if response.get("ship-to-address") else None
    )
    if not address_id:
        return ToolResponse(
            success=False,
            message="Requisition does not have address, use add_address_to_requisition instead.",
        )

    # update address payload
    update_payload: dict[str, Any] = {
        key: value
        for key, value in {
            "street1": street1,
            "city": city,
            "postal-code": postal_code,
            "state": state,
            "country": {"code": country_code} if country_code else None,
        }.items()
        if value not in (None, "")
    }

    # updating the address itself will update it in the requisition automatically
    updated_address = client.put_request(
        resource_name=f"addresses/{address_id}", payload=update_payload
    )
    if "errors" in updated_address:
        return ToolResponse(success=False, message=coupa_format_error_string(updated_address))

    return ToolResponse(
        success=True,
        message="Address updated successfully.",
        content=coupa_build_address(address=updated_address),
    )
