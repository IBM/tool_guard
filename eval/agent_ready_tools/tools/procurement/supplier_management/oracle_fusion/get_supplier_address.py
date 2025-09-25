from typing import Any, Dict, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.oracle_fusion_client import get_oracle_fusion_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.supplier_dataclasses import (
    OracleFusionSupplierAddressHeader,
)
from agent_ready_tools.utils.tool_credentials import ORACLE_FUSION_CONNECTIONS


@tool(expected_credentials=ORACLE_FUSION_CONNECTIONS)
def oracle_fusion_get_supplier_addresses(
    supplier_id: str,
    remit_to_address_flag: Optional[str] = None,
    address_name: Optional[str] = None,
    limit: Optional[int] = 20,
    skip: Optional[int] = 0,
) -> ToolResponse[List[OracleFusionSupplierAddressHeader]]:
    """
    Gets the address details of a supplier from Oracle Fusion.

    Args:
        supplier_id: The id of the supplier, returned by the oracle_fusion_get_all_suppliers tool. This ID is obtained by
            applying filters such as the supplier's name, number, or other relevant criteria.
        remit_to_address_flag: Set this to "true" to retrieve only the supplier addresses that are specifically marked as remit-to-address.
        address_name: The name of the address.
        limit: Number of records returned per page.
        skip: Number of records to skip for pagination.

    Returns:
        A list of address details for a supplier.
    """

    try:
        client = get_oracle_fusion_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params: Dict[str, Any] = {"limit": limit, "offset": skip}

    if remit_to_address_flag:
        params["q"] = f"AddressPurposeRemitToFlag = {remit_to_address_flag}"
    if address_name:
        params["q"] = f"AddressName = {address_name}"

    response = client.get_request(
        resource_name=f"suppliers/{supplier_id}/child/addresses", params=params
    )

    if "errors" in response:
        return ToolResponse(success=False, message=response["errors"])

    if "items" not in response or len(response["items"]) == 0:
        return ToolResponse(
            success=False, message="No address details found for the given supplier"
        )

    address_details = []

    for address in response["items"]:
        address_details.append(
            OracleFusionSupplierAddressHeader(
                address_id=address.get("SupplierAddressId", -1),
                country=address.get("Country", ""),
                address_name=address.get("AddressName", ""),
                address_line1=address.get("AddressLine1", ""),
                address_line2=address.get("AddressLine2", ""),
                city=address.get("City", ""),
                state=address.get("State", ""),
                postal_code=address.get("PostalCode", ""),
                county=address.get("County", ""),
                province=address.get("Province", ""),
            )
        )

    return ToolResponse(
        success=True,
        message="Retrieved the address details of a supplier from Oracle Fusion successfully",
        content=address_details,
    )
