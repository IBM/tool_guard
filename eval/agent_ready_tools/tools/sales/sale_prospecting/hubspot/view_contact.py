from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic import ValidationError

from agent_ready_tools.clients.hubspot_client import get_hubspot_client
from agent_ready_tools.tools.sales.sale_prospecting.hubspot.dataclasses import (
    HubspotContact,
    HubspotErrorResponse,
)
from agent_ready_tools.utils.tool_credentials import HUBSPOT_CONNECTIONS


@tool(expected_credentials=HUBSPOT_CONNECTIONS)
def hubspot_view_contact(contact_id: str) -> HubspotContact | HubspotErrorResponse:
    """
    View Hubspot contact using the deal ID.

    Args:
        contact_id: The unique ID for the contact

    Returns:
        A contact with the given ID.
    """

    client = get_hubspot_client()

    response = client.get_request(
        service="crm", version="v3", entity=f"objects/contacts/{contact_id}"
    )

    if "error" in response:
        return HubspotErrorResponse(
            message=response.get("message", "No contact returned with that ID")
        )

    try:
        contact = HubspotContact(**response.get("properties", {}))
    except ValidationError:
        return HubspotErrorResponse(message="Contact formatted incorrectly")

    return contact
