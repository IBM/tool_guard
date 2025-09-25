from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class UpdateSiteResponse:
    """Represents the result of updating a site in Microsoft SharePoint."""

    new_site_name: str
    site_description: Optional[str] = None


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def update_a_site(
    site_id: str,
    new_site_name: Optional[str] = None,
    site_description: Optional[str] = None,
) -> UpdateSiteResponse:
    """
    Update a site in Microsoft SharePoint.

    Args:
        site_id: The site_id uniquely identifying them within the MS Graph API, returned by
            `get_sites` tool
        new_site_name: The new title of the site to update.
        site_description: The new description of the site to update.

    Returns:
        The updated site title and description.
    """
    client = get_microsoft_client()

    payload = {
        "displayName": new_site_name,
        "description": site_description,
    }

    # Filter out the parameters which are None/Blank.
    payload = {key: value for key, value in payload.items() if value}

    response = client.update_request(endpoint=f"sites/{site_id}", data=payload)

    return UpdateSiteResponse(
        new_site_name=response.get("displayName", ""),
        site_description=response.get("description", ""),
    )
