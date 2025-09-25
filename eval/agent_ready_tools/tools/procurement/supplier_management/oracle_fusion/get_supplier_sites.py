from typing import Any, Dict, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.oracle_fusion_client import get_oracle_fusion_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.supplier_management.oracle_fusion.supplier_dataclasses import (
    OracleFusionSupplierSiteHeaders,
)
from agent_ready_tools.utils.tool_credentials import ORACLE_FUSION_CONNECTIONS


@tool(expected_credentials=ORACLE_FUSION_CONNECTIONS)
def oracle_fusion_get_supplier_sites(
    supplier_id: str,
    site_name: Optional[str] = None,
    limit: Optional[int] = 20,
    skip: Optional[int] = 0,
) -> ToolResponse[List[OracleFusionSupplierSiteHeaders]]:
    """
    Gets all the sites of a supplier from Oracle Fusion.

    Args:
        supplier_id: The id of the supplier, returned by the oracle_fusion_get_all_suppliers tool. This ID is obtained by applying filters such as the supplier's name, number, or other relevant criteria.
        site_name: The name of the site.
        limit: Number of records returned per page.
        skip: Number of records to skip for pagination.

    Returns:
        A list of site details for a supplier.
    """

    try:
        client = get_oracle_fusion_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params: Dict[str, Any] = {"limit": limit, "offset": skip}

    if site_name:
        params["q"] = f"SupplierSite = {site_name}"

    response = client.get_request(
        resource_name=f"suppliers/{supplier_id}/child/sites", params=params
    )

    if "errors" in response:
        return ToolResponse(success=False, message=response["errors"])

    if "items" not in response or len(response["items"]) == 0:
        return ToolResponse(success=False, message="No sites found for the given supplier")

    sites = []

    for site in response["items"]:
        sites.append(
            OracleFusionSupplierSiteHeaders(
                site_id=site.get("SupplierSiteId", -1),
                site_name=site.get("SupplierSite", ""),
                procurement_business_unit=site.get("ProcurementBU", ""),
                address_name=site.get("SupplierAddressName", ""),
            )
        )

    return ToolResponse(
        success=True,
        message="Retrieved the site details of a supplier from Oracle Fusion successfully",
        content=sites,
    )
