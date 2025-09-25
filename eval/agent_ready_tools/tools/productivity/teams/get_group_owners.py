from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class Owner:
    """Represents the result of Owner object in Teams."""

    id: str
    display_name: str
    user_principal_name: str
    account_enabled: bool


@dataclass
class GetTeamsOrganizationsResponse:
    """Represents the result of an event delete operation in Teams."""

    owners: List[Owner]


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def get_group_owners(group_id: str) -> GetTeamsOrganizationsResponse:
    """
    Get list owners for given group in Teams.

    Args:
        group_id: The id uniquely identifying group within the MS Graph API, as specified by the
            `get_group_ids_by_name` tool.

    Returns:
        List of owners.
    """
    client = get_microsoft_client()

    endpoint = f"groups/{group_id}/owners"
    response = client.get_request(endpoint)
    owners: List[Owner] = []

    for owner in response["value"]:
        owners.append(
            Owner(
                id=owner.get("id", ""),
                display_name=owner.get("displayName", ""),
                user_principal_name=owner.get("userPrincipalName", ""),
                account_enabled=owner.get("accountEnabled"),
            )
        )

    return GetTeamsOrganizationsResponse(owners=owners)
