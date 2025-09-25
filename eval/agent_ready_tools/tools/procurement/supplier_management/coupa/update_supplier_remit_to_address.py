from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@dataclass
class CoupaUpdateRemitToAddressResponse:
    """Represents the result of updating supplier remit to address details in Coupa."""

    remit_to_address_id: int


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_update_supplier_remit_to_address(
    supplier_id: int,
    remit_to_address_id: int,
    remit_to_code: Optional[str] = None,
    name: Optional[str] = None,
    street1: Optional[str] = None,
    street2: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    postal_code: Optional[str] = None,
    active: Optional[str] = None,
    country: Optional[str] = None,
) -> ToolResponse[CoupaUpdateRemitToAddressResponse]:
    """
    Updates remit to address for a supplier in Coupa.

    Args:
        supplier_id: The id of the supplier, returned from get_all_suppliers tool.
        remit_to_address_id: The id of the supplier remit address, returned from
            get_supplier_remit_to_addresses tool.
        remit_to_code: The unique code of the remit address.
        name: The name of the address.
        street1: The first line of the address.
        street2: The second line of the address.
        city: The city associated with the address.
        state: The state associated with the address.
        postal_code: The postal code associated with the address.
        active: The active state of the address (Possible values: true, false).
        country: The 2 digit ISO code of the country associated with the address.

    Returns:
        Result from updating a supplier remit to address.
    """

    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    payload: dict[str, Any] = {
        key: value
        for key, value in {
            "remit-to-code": remit_to_code,
            "name": name,
            "street1": street1,
            "street2": street2,
            "city": city,
            "state": state,
            "postal-code": postal_code,
            "active": active,
            "country": {"code": country} if country else None,
        }.items()
        if value is not None
    }

    resource_name = f"suppliers/{supplier_id}/addresses/{remit_to_address_id}"

    response = client.put_request(resource_name=resource_name, payload=payload)

    if "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))

    return ToolResponse(
        success=True,
        message="Supplier remit to address updated",
        content=CoupaUpdateRemitToAddressResponse(remit_to_address_id=response.get("id", "")),
    )
