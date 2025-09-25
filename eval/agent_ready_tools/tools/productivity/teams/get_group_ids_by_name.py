from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class GetGroupIdResponse:
    """Represents the result of getting goup ids in Teams."""

    ids: List[str]


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def get_group_ids_by_name(group_name: str) -> GetGroupIdResponse:
    """
    Get id for given group name in Teams.

    Args:
        group_name: The name of the group within the MS Graph API.

    Returns:
        List of ids.
    """
    client = get_microsoft_client()

    endpoint = f"groups?$filter=displayName eq '{group_name}'"
    response = client.get_request(endpoint)
    ids: List[str] = []

    for group in response["value"]:
        ids.append(group.get("id", ""))

    return GetGroupIdResponse(ids=ids)
