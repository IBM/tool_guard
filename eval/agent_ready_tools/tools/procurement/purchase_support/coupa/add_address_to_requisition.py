from typing import Optional

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
def coupa_add_address_to_requisition(
    requisition_id: int,
    street1: str,
    city: str,
    postal_code: str,
    state: Optional[str] = None,
    country_code: str = "US",  # 2-letter ISO
) -> ToolResponse[CoupaAddress]:
    """
    Adds an address to a requisition in Coupa.

    Args:
        requisition_id: The Coupa ID of the requisition to update (required).
        street1: Required first street line.
        city: Required if providing full address.
        postal_code: Required if providing full address.
        state: Optional state/province.
        country_code: Required if providing full address.

    Returns:
        The resulting requisition after submitting the requisition update request.
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    requisition = client.get_request(resource_name=f"requisitions/{requisition_id}")
    if "errors" in requisition:
        return ToolResponse(success=False, message=coupa_format_error_string(requisition))

    if requisition.get("line-count", 0) == 0:
        return ToolResponse(
            success=False,
            message="You cannot add an address to this requisition yet since it currently does not contain any line items.",
        )

    # creating a new address in the system
    address_payload = {
        "street1": street1,
        "city": city,
        "postal-code": postal_code,
        "country": {"code": country_code},
        # required unique identifier per address you make in addition to the actual address ID
        "location-code": f"ship-to-{requisition_id}",
    }
    if state:
        address_payload["state"] = state

    new_address = client.post_request(resource_name="addresses", payload=address_payload)
    if "errors" in new_address:
        return ToolResponse(success=False, message=coupa_format_error_string(new_address))

    # update requisition with new address
    ship_to_address_payload = {"id": new_address["id"]}
    update_payload = {"ship-to-address": ship_to_address_payload}

    response = client.put_request(
        resource_name=f"requisitions/{requisition_id}", payload=update_payload
    )
    if "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))
    ship_to_address = response["ship-to-address"]

    return ToolResponse(
        success=True,
        message="Address was successfully added.",
        content=coupa_build_address(address=ship_to_address),
    )
