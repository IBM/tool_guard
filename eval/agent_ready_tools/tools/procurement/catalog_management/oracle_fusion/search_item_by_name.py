from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.oracle_fusion_client import get_oracle_fusion_client
from agent_ready_tools.tools.procurement.catalog_management.oracle_fusion.catalog_dataclasses import (
    OracleFusionItem,
)
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.tool_credentials import ORACLE_FUSION_CONNECTIONS


@tool(expected_credentials=ORACLE_FUSION_CONNECTIONS)
def oracle_fusion_search_item_by_name(
    search_term: str,
) -> ToolResponse[List[OracleFusionItem]]:
    """
    Retrieves items from Oracle Fusion that match the provided search term.

    Args:
        search_term: A keyword or phrase used to search items.

    Returns:
        The best match results.
    """

    try:
        client = get_oracle_fusion_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    response = client.get_request(
        resource_name="itemsV2", params={"q": f"ItemDescription LIKE '%{search_term}%'"}
    )

    if "errors" in response:
        return ToolResponse(success=False, message=response["errors"])

    if "items" not in response or len(response["items"]) == 0:
        return ToolResponse(success=False, message="No items found.")

    item_details = [
        OracleFusionItem(
            item_id=item.get("ItemId", -1),
            item_number=item.get("ItemNumber", ""),
            item_class=item.get("ItemClass", ""),
            item_description=item.get("ItemDescription", ""),
            primary_uom_value=item.get("PrimaryUOMValue", ""),
            organization_code=item.get("OrganizationCode", ""),
            lifecycle_phase=item.get("LifecyclePhaseValue", ""),
            item_status=item.get("ItemStatusValue", ""),
        )
        for item in response["items"]
    ]

    return ToolResponse(
        success=True,
        message="Retrieved the list of items based on your search term",
        content=item_details,
    )
