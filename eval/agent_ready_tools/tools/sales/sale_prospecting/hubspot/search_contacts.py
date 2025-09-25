from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic import ValidationError

from agent_ready_tools.clients.hubspot_client import get_hubspot_client
from agent_ready_tools.tools.sales.sale_prospecting.hubspot.dataclasses import (
    HubspotContact,
    HubspotErrorResponse,
)
from agent_ready_tools.tools.sales.sale_prospecting.hubspot.utils import (
    hubspot_create_search_filter,
)
from agent_ready_tools.utils.tool_credentials import HUBSPOT_CONNECTIONS


@tool(expected_credentials=HUBSPOT_CONNECTIONS)
def hubspot_search_contacts(
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    company: Optional[str] = None,
    email: Optional[str] = None,
    job_title: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
) -> List[HubspotContact] | HubspotErrorResponse:
    """
    Search for contacts based on filtering criteria.

    Args:
        first_name: A first name of the contact to search for.
        last_name: A last name of the contact to search for.
        company: A company name of the contact to search for.
        email: An email address of the contact to search for.
        job_title: A job title of the contact to search for.
        city: The city of the contact to search for.
        state: The state of the contact to search for.

    Returns:
        A list of contacts matching the search criteria, or an error response in the event of failure.
    """

    client = get_hubspot_client()

    criteria = {
        "firstname": first_name,
        "lastname": last_name,
        "company": company,
        "email": email,
        "jobtitle": job_title,
        "city": city,
        "state": state,
    }

    filtered_criteria = {key: val for key, val in criteria.items() if val is not None}

    filters = hubspot_create_search_filter(filtered_criteria)

    response = client.post_request(
        service="crm", version="v3", entity="objects/contacts/search", payload=filters
    )

    if not response.get("results"):
        return HubspotErrorResponse(message="No contacts returned from search")
    if response.get("status") == "error":
        return HubspotErrorResponse(message=response.get("message", ""))

    contacts: List[HubspotContact] = []
    try:
        for r in response.get("results", []):
            contact = HubspotContact(**r.get("properties", {}))
            contacts.append(contact)
    except ValidationError:
        return HubspotErrorResponse(message="Contacts weren't formatted correctly")
    return contacts
