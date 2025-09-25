# create_list.py
from typing import Any

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class CreateListResult:
    """Represents the result of create operation of a list in Microsoft Sharepoint."""

    list_name: str


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def create_list(site_id: str, display_name: str, description: str) -> CreateListResult:
    """
    Create a list in Sharepoint.

    Args:
        site_id: The site_id uniquely identifying them within the MS Graph API, returned by
            `get_sites` tool.
        display_name: The display name of the list to be created in Microsoft SharePoint.
        description: The description of the list to be created in Microsoft Sharepoint.

    Returns:
        The name of the created list.
    """
    client = get_microsoft_client()

    payload: dict[str, Any] = {"displayName": display_name, "description": description}
    payload = {key: value for key, value in payload.items() if value}

    endpoint = f"sites/{site_id}/lists"

    response = client.post_request(endpoint=endpoint, data=payload)
    return CreateListResult(list_name=response.get("displayName", ""))
