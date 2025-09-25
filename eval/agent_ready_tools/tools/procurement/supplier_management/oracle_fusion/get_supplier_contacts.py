from typing import Any, Dict, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.oracle_fusion_client import get_oracle_fusion_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.supplier_dataclasses import (
    OracleFusionSupplierContactDetails,
)
from agent_ready_tools.utils.tool_credentials import ORACLE_FUSION_CONNECTIONS


@tool(expected_credentials=ORACLE_FUSION_CONNECTIONS)
def oracle_fusion_get_supplier_contacts(
    supplier_id: str,
    limit: Optional[int] = 20,
    skip: Optional[int] = 0,
) -> ToolResponse[List[OracleFusionSupplierContactDetails]]:
    """
    Get all contacts of a supplier from Oracle Fusion.

    Args:
        supplier_id: The id of the supplier, returned by the oracle_fusion_get_all_suppliers tool. This ID is obtained by
            applying filters such as the supplier's name, number, or other relevant criteria.
        limit: Number of contacts returned.
        skip: Number of contacts to skip for pagination.

    Returns:
        A list of contacts of a supplier.
    """

    try:
        client = get_oracle_fusion_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params: Dict[str, Any] = {"limit": limit, "offset": skip}

    response = client.get_request(
        resource_name=f"suppliers/{supplier_id}/child/contacts",
        params=params,
    )

    if "errors" in response:
        return ToolResponse(success=False, message=response["errors"])

    if "items" not in response or len(response["items"]) == 0:
        return ToolResponse(success=False, message="No contacts found for the given supplier")

    contact_details = []
    contact_details = [
        OracleFusionSupplierContactDetails(
            supplier_contact_id=item.get("SupplierContactId", ""),
            first_name=item.get("FirstName", ""),
            last_name=item.get("LastName", ""),
            phone_country_code=item.get("PhoneCountryCode", ""),
            phone_area_code=item.get("PhoneAreaCode", ""),
            phone_number=item.get("PhoneNumber", ""),
            mobile_country_code=item.get("MobileCountryCode", ""),
            mobile_area_code=item.get("MobileAreaCode", ""),
            mobile_number=item.get("MobileNumber", ""),
            email=item.get("Email", ""),
        )
        for item in response["items"]
    ]

    return ToolResponse(
        success=True,
        message="Retrieved the contact's details of supplier from Oracle Fusion.",
        content=contact_details,
    )
