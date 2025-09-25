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
class CoupaCreateSupplierAddressResult:
    """Represents the result of creating supplier address in Coupa."""

    supplier_id: int


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_create_supplier_address(
    supplier_id: str,
    street1: str,
    city: str,
    country: str,
    postal_code: str,
    name: Optional[str] = None,
    street2: Optional[str] = None,
    state: Optional[str] = None,
    purpose: Optional[Union[Iterator[CoupaAddressPurposeType] | CoupaAddressPurposeType]] = None,
) -> ToolResponse[CoupaCreateSupplierAddressResult]:
    """
    creates address for a supplier in coupa.

    Args:
        supplier_id: The id of the supplier, returned from `get_all_suppliers` tool.
        street1: The first line of the address.
        city: The city associated with the address.
        country: The 2 digit ISO code of the country associated with the address.
        postal_code: The postal code associated with the address.
        name: The name of the address.
        street2: The second line of the address.
        state: The state associated with the address.
        purpose: The purpose of the address.

    Returns:
        Result from creating a supplier address.
    """

    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    if purpose is None:
        purposes: List[CoupaAddressPurposeType] = []
    else:
        purposes = list([purpose] if isinstance(purpose, str) else purpose)

    purposes_list: List[Dict[str, str]] = [{"name": p} for p in purposes]

    address = {
        "name": name,
        "street1": street1,
        "street2": street2,
        "city": city,
        "state": state,
        "postal-code": postal_code,
        "country": {"code": country},
        "purposes": purposes_list,
    }

    address_payload = {key: value for key, value in address.items() if value not in (None, "")}

    payload = {"supplier-addresses": [address_payload]}

    response = client.put_request(
        resource_name=f"suppliers/{supplier_id}",
        payload=payload,
        params={"fields": '["id"]'},
    )

    if "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))

    return ToolResponse(
        success=True,
        message="Supplier address created",
        content=CoupaCreateSupplierAddressResult(supplier_id=response.get("id", "")),
    )
