from typing import Iterator, List, Optional, Union

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.oracle_fusion_client import get_oracle_fusion_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.supplier_dataclasses import (
    OracleFusionAddressPurposeMap,
    OracleFusionAddressPurposeType,
    OracleFusionUpdateSupplierAddress,
    OracleFusionUpdateSupplierAddressResult,
)
from agent_ready_tools.utils.tool_credentials import ORACLE_FUSION_CONNECTIONS


@tool(expected_credentials=ORACLE_FUSION_CONNECTIONS)
def oracle_fusion_update_supplier_address(
    supplier_id: str,
    address_id: str,
    street1: Optional[str] = None,
    city: Optional[str] = None,
    country_code: Optional[str] = None,
    country: Optional[str] = None,
    postal_code: Optional[str] = None,
    email: Optional[str] = None,
    name: Optional[str] = None,
    street2: Optional[str] = None,
    state: Optional[str] = None,
    purpose: Optional[
        Union[Iterator[OracleFusionAddressPurposeType], OracleFusionAddressPurposeType, str]
    ] = None,
) -> ToolResponse[OracleFusionUpdateSupplierAddressResult]:
    """
    Update an existing supplier address in Oracle Fusion.

    Args:
        supplier_id: Supplier ID.
        address_id: Address ID.
        street1: Address Line 1.
        city: City name.
        country_code: ISO country code (e.g., 'US').
        country: Full country name.
        postal_code: ZIP or postal code.
        email: Contact email.
        name: Label for the address.
        street2: Address Line 2.
        state: State or province.
        purpose: List of address purposes ('ordering', 'remit_to', etc.).

    Returns:
        ToolResponse containing the update result.
    """
    try:
        client = get_oracle_fusion_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    # Normalize purposes
    if purpose is None:
        purposes: List[str] = []
    else:
        if isinstance(purpose, (str, OracleFusionAddressPurposeType)):
            purposes = [purpose]
        else:
            purposes = list(purpose)

    purposes = [p.value if hasattr(p, "value") else p for p in purposes]

    purpose_flags = {
        OracleFusionAddressPurposeMap.PURPOSES[p]: True
        for p in purposes
        if p in OracleFusionAddressPurposeMap.PURPOSES
    }

    # Only include fields that are provided
    # Construct payload directly without intermediate dataclass
    address_data = {
        "address_name": name,
        "address_line1": street1,
        "address_line2": street2,
        "city": city,
        "state": state,
        "country_code": country_code,
        "country": country,
        "postal_code": postal_code,
        "email": email,
    }

    payload = {
        OracleFusionUpdateSupplierAddress.FIELD_NAME_MAP[k]: v
        for k, v in address_data.items()
        if v is not None and k in OracleFusionUpdateSupplierAddress.FIELD_NAME_MAP
    }

    # Add normalized purpose flags
    payload.update(
        {
            OracleFusionUpdateSupplierAddress.FIELD_NAME_MAP[k]: "Y"
            for k in purpose_flags
            if k in OracleFusionUpdateSupplierAddress.FIELD_NAME_MAP
        }
    )

    response = client.patch_request(
        resource_name=f"suppliers/{supplier_id}/child/addresses/{address_id}", payload=payload
    )

    if "errors" in response:
        return ToolResponse(success=False, message=response["errors"])

    return ToolResponse(
        success=True,
        message="Supplier address updated",
        content=OracleFusionUpdateSupplierAddressResult(
            supplier_id=supplier_id,
            address_id=address_id,
            raw_response=response,
        ),
    )
