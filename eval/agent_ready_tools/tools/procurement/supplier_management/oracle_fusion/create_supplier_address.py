from dataclasses import asdict
from typing import Iterator, List, Optional, Union

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.oracle_fusion_client import get_oracle_fusion_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.supplier_dataclasses import (
    OracleFusionAddressPurposeMap,
    OracleFusionAddressPurposeType,
    OracleFusionCreateSupplierAddressResult,
    OracleFusionSupplierAddress,
)
from agent_ready_tools.utils.tool_credentials import ORACLE_FUSION_CONNECTIONS


@tool(expected_credentials=ORACLE_FUSION_CONNECTIONS)
def oracle_fusion_create_supplier_address(
    supplier_id: str,
    street1: str,
    city: str,
    country_code: str,
    country: Optional[str],
    postal_code: str,
    email: str,
    name: Optional[str] = None,
    street2: Optional[str] = None,
    state: Optional[str] = None,
    purpose: Optional[
        Union[Iterator[OracleFusionAddressPurposeType], OracleFusionAddressPurposeType, str]
    ] = None,
) -> ToolResponse[OracleFusionCreateSupplierAddressResult]:
    """
    Create a supplier address in Oracle Fusion.

    Args:
        supplier_id: Supplier ID.
        street1: Address Line 1.
        city: City name.
        country_code: ISO country code (e.g., 'US').
        country: Full country name (e.g., 'United States').
        postal_code: ZIP or postal code.
        email: Contact email for the address.
        name: Name or label for the address (e.g., 'HQ').
        street2: (Optional) Address Line 2.
        state: (Optional) State or province.
        purpose: (Optional) List of address purposes. Supported values include 'ordering', 'remit_to', 'rfq_or_bidding', 'payment', and 'procurement'.

    Returns:
        ToolResponse containing the created supplier address ID.
    """
    try:
        client = get_oracle_fusion_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    # Normalize purpose(s) to a list of lowercase strings
    if purpose is None:
        purposes: List[str] = []
    else:
        if isinstance(purpose, (str, OracleFusionAddressPurposeType)):
            purposes = [purpose]
        else:
            purposes = list(purpose)

    purposes = [p.value if hasattr(p, "value") else p for p in purposes]

    # Build the dict of Oracle purpose flags
    purpose_flags = {
        OracleFusionAddressPurposeMap.PURPOSES[p]: True
        for p in purposes
        if p in OracleFusionAddressPurposeMap.PURPOSES
    }

    # Build the payload using dataclass
    address = OracleFusionSupplierAddress(
        address_name=name,
        address_line1=street1,
        address_line2=street2,
        city=city,
        state=state,
        country_code=country_code,
        country=country,
        postal_code=postal_code,
        email=email,
        **purpose_flags,
    )

    payload = {
        OracleFusionSupplierAddress.FIELD_NAME_MAP[k]: ("Y" if isinstance(v, bool) and v else v)
        for k, v in asdict(address).items()
        if v is not None
    }

    response = client.post_request(
        resource_name=f"suppliers/{supplier_id}/child/addresses", payload=payload
    )

    if "errors" in response:
        return ToolResponse(success=False, message=response["errors"])

    items = response.get("items", [])
    address_data = items[0] if items else {}

    return ToolResponse(
        success=True,
        message="Supplier address created",
        content=OracleFusionCreateSupplierAddressResult(
            supplier_id=supplier_id,
            address_id=address_data.get("SupplierAddressId"),
            raw_response=address_data,
        ),
    )
