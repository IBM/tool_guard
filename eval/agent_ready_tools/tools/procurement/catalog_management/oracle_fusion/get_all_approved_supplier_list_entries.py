from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.oracle_fusion_client import get_oracle_fusion_client
from agent_ready_tools.tools.procurement.catalog_management.oracle_fusion.catalog_dataclasses import (
    OracleFusionApprovedSupplierListEntryList,
)
from agent_ready_tools.tools.procurement.catalog_management.oracle_fusion.catalog_helper_functions import (
    oracle_fusion_build_approved_supplier_list_entry_from_response,
)
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.tool_credentials import ORACLE_FUSION_CONNECTIONS


@tool(expected_credentials=ORACLE_FUSION_CONNECTIONS)
def oracle_fusion_get_all_approved_supplier_list_entries(
    supplier_name: Optional[str] = None,
    supplier_id: Optional[int] = None,
    item_name: Optional[str] = None,
    item_id: Optional[int] = None,
    ship_to_organization: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
) -> ToolResponse[OracleFusionApprovedSupplierListEntryList]:
    """
    Get all approved supplier list entries from Oracle Fusion.

    Args:
        supplier_name: name of supplier to filter for (e.g. United Parcel Service)
        supplier_id: id of supplier to filter for
        item_name: name of item to filter for - (e.g. PK101, SCH-01)
        item_id: id of item to filter for
        ship_to_organization: name of inventory organization to which the supplier should ship the goods - (e.g. Operations, Seattle)
        limit: number of supplier list entries
        offset: number of supplier list entries to offset for pagination

    Returns:
        A list of approved supplier list entries.
    """

    try:
        client = get_oracle_fusion_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    query_map = {
        "Supplier": supplier_name,
        "SupplierId": supplier_id,
        "Item": item_name,
        "ItemId": item_id,
        "ShipToOrganization": ship_to_organization,
    }

    expressions = []
    for field, value in query_map.items():
        if value:
            if str(value).isdigit():
                # isdigit for ids, adk tends to still have strings as input regardless
                expressions.append(f"{field} = {value}")
            else:
                # partial/lenient match on strings
                expressions.append(f"{field} LIKE {value}*")

    query_string = ";".join(expressions) if expressions else None

    params = {
        "q": query_string,
        "limit": limit,
        "offset": offset,
        "orderBy": "AslCreationDate:desc",
    }

    params = {key: value for key, value in params.items() if value is not None}

    response = client.get_request(
        resource_name="procurementApprovedSupplierListEntries",
        params=params,
    )

    if "errors" in response:
        return ToolResponse(success=False, message=response["errors"])

    if "items" not in response or len(response["items"]) == 0:
        return ToolResponse(success=False, message="No approved supplier list entries found.")

    supplier_list_entries = []
    for supplier_list_entry in response["items"]:
        supplier_list_entries.append(
            oracle_fusion_build_approved_supplier_list_entry_from_response(
                response=supplier_list_entry
            )
        )

    return ToolResponse(
        success=True,
        message="Approved supplier list entries retrieved successfully.",
        content=OracleFusionApprovedSupplierListEntryList(
            supplier_list_entry_list=supplier_list_entries
        ),
    )
