from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.supplier_management.coupa.supplier_dataclasses import (
    CreateRemitToAddressResult,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_create_supplier_remit_to_address(
    supplier_id: int,
    remit_to_code: str,
    name: str,
    street1: str,
    city: str,
    state: str,
    postal_code: str,
    active: bool,
    country_code: str,
    street2: Optional[str] = None,
) -> ToolResponse[CreateRemitToAddressResult]:
    """
    Create a supplier remit-to-address.

    Args:
        supplier_id: Supplier ID
        remit_to_code: Remit To Code (if a Supplier address)
        name: Address 'Nickname'
        street1: Address Line 1
        city: City Name
        state: State Abbreviation. This field accepts any value.
        postal_code: Postal Code
        active: Is the item given for this supplier & contract active?
        country_code: ISO Country Code
        street2: Address Line 2

    Returns:
        Result from creating remit-to-address
    """

    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    payload = {
        "remit-to-code": remit_to_code,
        "name": name,
        "street1": street1,
        "city": city,
        "state": state,
        "postal-code": postal_code,
        "active": active,
        "country": {"code": country_code},
    }

    optional_fields = {
        "street2": street2,
    }

    for key, value in optional_fields.items():
        if value is not None:
            payload[key] = value

    response = client.post_request(
        resource_name=f"suppliers/{supplier_id}/addresses",
        params={"fields": '["id"]'},
        payload=payload,
    )

    if "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))

    return ToolResponse(
        success=True,
        message="Supplier remit to address created",
        content=CreateRemitToAddressResult(id=response["id"]),
    )
