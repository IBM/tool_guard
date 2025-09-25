from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.supplier_management.coupa.supplier_dataclasses import (
    CoupaRemitToAddress,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_get_supplier_remit_to_addresses(
    supplier_id: int,
) -> ToolResponse[List[CoupaRemitToAddress]]:
    """
    Get a supplier's remit-to-address in Coupa.

    Args:
        supplier_id: The supplier's ID

    Returns:
        A list of remit-to-address for the given supplier
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    response = client.get_request_list(
        resource_name=f"suppliers/{supplier_id}/addresses",
        params={
            "fields": '["id","remit-to-code","name","street1","street2","city","state",{"country":["code"]},"active","postal-code"]'
        },
    )

    if len(response) == 0:
        return ToolResponse(success=False, message="No remit to addresses returned")

    if "errors" in response[0]:
        return ToolResponse(success=False, message=coupa_format_error_string(response[0]))

    addresses = []
    for address in response:
        addresses.append(
            CoupaRemitToAddress(
                remit_to_address_id=address["id"],
                name=address["name"],
                active=address["active"],
                street1=address["street1"],
                street2=address["street2"],
                city=address["city"],
                state=address["state"],
                postal_code=address["postal-code"],
                remit_to_code=address["remit-to-code"],
                country=address["country"]["code"],
            )
        )

    return ToolResponse(
        success=True,
        message="Get supplier remit to address successful",
        content=addresses,
    )
