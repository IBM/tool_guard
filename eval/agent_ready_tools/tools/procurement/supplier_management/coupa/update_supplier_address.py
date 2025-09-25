from typing import Dict, Iterator, List, Optional, Union

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.supplier_management.coupa.supplier_dataclasses import (
    CoupaAddressPurposeType,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@dataclass
class CoupaUpdateSupplierAddressResponse:
    """Represents the result of updating supplier address details in Coupa."""

    supplier_id: int


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_update_supplier_address(
    supplier_id: int,
    address_id: int,
    street1: Optional[str] = None,
    city: Optional[str] = None,
    country: Optional[str] = None,
    postal_code: Optional[str] = None,
    name: Optional[str] = None,
    street2: Optional[str] = None,
    state: Optional[str] = None,
    purpose: Optional[Union[Iterator[CoupaAddressPurposeType] | CoupaAddressPurposeType]] = None,
) -> ToolResponse[CoupaUpdateSupplierAddressResponse]:
    """
    Updates address for a supplier in coupa.

    Args:
        supplier_id: The id of the supplier, returned from get_all_suppliers tool.
        address_id: "The id of the supplier address, returned from get_supplier_by_id tool."
        street1: The first line of the address.
        city: The city associated with the address.
        country: The 2 digit ISO code of the country associated with the address.
        postal_code: The postal code associated with the address.
        name: The name of the address.
        street2: The second line of the address.
        state: The state associated with the address.
        purpose: The purpose of the address.

    Returns:
        Result from updating a supplier address.
    """

    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    if purpose is None:
        purposes: List[CoupaAddressPurposeType] = []
    else:
        purposes = list([purpose] if isinstance(purpose, str) else purpose)

    purposes_list: List[Dict[str, str]] = [{"name": name} for name in purposes]

    payload = {
        "supplier-addresses": [
            {
                "id": address_id,
                "name": name,
                "street1": street1,
                "street2": street2,
                "city": city,
                "state": state,
                "postal-code": postal_code,
                "purposes": purposes_list,
                "country": {"code": country} if country else None,
            }
        ]
    }

    payload = {
        key: [{key: value for key, value in item.items() if value} for item in value]
        for key, value in payload.items()
        if value
    }

    response = client.put_request(
        resource_name=f"suppliers/{supplier_id}",
        payload=payload,
        params={"fields": '["id"]'},
    )

    if "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))

    return ToolResponse(
        success=True,
        message="Supplier address updated",
        content=CoupaUpdateSupplierAddressResponse(supplier_id=response.get("id", "")),
    )
