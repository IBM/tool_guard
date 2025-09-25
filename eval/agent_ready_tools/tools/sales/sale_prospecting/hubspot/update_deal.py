from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.hubspot_client import get_hubspot_client
from agent_ready_tools.tools.sales.sale_prospecting.hubspot.dataclasses import HubspotErrorResponse
from agent_ready_tools.utils.tool_credentials import HUBSPOT_CONNECTIONS


@dataclass
class HubspotUpdateDealResponse:
    """The response from Hubspot when updating a Deal."""

    deal_id: str


@tool(expected_credentials=HUBSPOT_CONNECTIONS)
def hubspot_update_deal(
    deal_id: str,
    deal_name: Optional[str] = None,
    deal_type: Optional[str] = None,
    description: Optional[str] = None,
    deal_stage: Optional[str] = None,
    amount: Optional[float] = None,
    pipeline: Optional[str] = None,
) -> HubspotUpdateDealResponse | HubspotErrorResponse:
    """
    Update a deal in Hubspot.

    Args:
        deal_id: The unique identifier for the deal
        deal_name: The name given to this deal
        deal_type: The type of deal. By default, categorize your deal as either a New Business or Existing Business.
        description: Description of the deal
        deal_stage: The stage of the deal. Deal stages allow you to categorize and track the progress of the deals that you are working on
        amount: The total amount of the deal
        pipeline: The pipeline the deal is in. This determines which stages are options for the deal

    Returns:
        The success response or an error
    """

    client = get_hubspot_client()

    props = {
        "dealname": deal_name,
        "dealtype": deal_type,
        "description": description,
        "dealstage": deal_stage,
        "amount": amount,
        "pipeline": pipeline,
    }

    properties = {key: val for key, val in props.items() if val is not None}

    response = client.patch_request(
        service="crm",
        version="v3",
        entity=f"objects/deals/{deal_id}",
        payload={"properties": properties},
    )

    if response.get("status") == "error":
        return HubspotErrorResponse(message=response.get("message", ""))

    return HubspotUpdateDealResponse(deal_id=response.get("id", ""))
