from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic import ValidationError

from agent_ready_tools.clients.hubspot_client import get_hubspot_client
from agent_ready_tools.tools.sales.sale_prospecting.hubspot.dataclasses import (
    HubspotDeal,
    HubspotErrorResponse,
)
from agent_ready_tools.tools.sales.sale_prospecting.hubspot.utils import (
    hubspot_create_search_filter,
)
from agent_ready_tools.utils.tool_credentials import HUBSPOT_CONNECTIONS


@tool(expected_credentials=HUBSPOT_CONNECTIONS)
def hubspot_search_deals(deal_name: str) -> List[HubspotDeal] | HubspotErrorResponse:
    """
    Search for deals using the deal name.

    Args:
        deal_name: A deal name to be searched for.

    Returns:
        Deals that contain the deal name given.
    """

    client = get_hubspot_client()

    filters = hubspot_create_search_filter({"dealname": deal_name})

    response = client.post_request(
        service="crm", version="v3", entity="objects/deals/search", payload=filters
    )

    if not response.get("results"):
        return HubspotErrorResponse(message="No deals returned from search")
    if response.get("status") == "error":
        return HubspotErrorResponse(message=response.get("message", ""))

    deals: List[HubspotDeal] = []
    try:
        for r in response.get("results", []):
            deal = HubspotDeal(**r.get("properties", {}))
            deals.append(deal)
    except ValidationError:
        return HubspotErrorResponse(message="Deals weren't formatted correctly")
    return deals
