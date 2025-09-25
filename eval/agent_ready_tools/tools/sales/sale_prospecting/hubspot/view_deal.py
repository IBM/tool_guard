from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic import ValidationError

from agent_ready_tools.clients.hubspot_client import get_hubspot_client
from agent_ready_tools.tools.sales.sale_prospecting.hubspot.dataclasses import (
    HubspotDeal,
    HubspotErrorResponse,
)
from agent_ready_tools.utils.tool_credentials import HUBSPOT_CONNECTIONS


@tool(expected_credentials=HUBSPOT_CONNECTIONS)
def hubspot_view_deal(deal_id: str) -> HubspotDeal | HubspotErrorResponse:
    """
    View Hubspot deal using the deal ID.

    Args:
        deal_id: The unique ID for the deal

    Returns:
        A deal with the given ID.
    """

    client = get_hubspot_client()

    response = client.get_request(service="crm", version="v3", entity=f"objects/deals/{deal_id}")

    if "error" in response:
        return HubspotErrorResponse(
            message=response.get("message", "No deal returned with that ID")
        )

    try:
        deal = HubspotDeal(**response.get("properties", {}))
    except ValidationError:
        return HubspotErrorResponse(message="Deal formatted incorrectly")

    return deal
