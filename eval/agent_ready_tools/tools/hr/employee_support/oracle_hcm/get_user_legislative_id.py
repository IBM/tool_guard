from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.get_id_from_links import get_id_from_links
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class UserLegislativeID:
    """Represents the response from fetching the user's unique legislative identifier from Oracle
    HCM."""

    legislative_id: Optional[str]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def get_user_legislative_id(worker_id: str) -> UserLegislativeID:
    """
    Fetches a user's `legislative_id` from Oracle HCM.

    Args:
        worker_id: The worker's worker_id uniquely identifying them within the Oracle HCM API
            returned by tool `get_user_oracle_ids`.

    Returns:
        The user's unique legislative identifier within Oracle HCM.
    """
    client = get_oracle_hcm_client()

    entity = f"workers/{worker_id}/child/legislativeInfo"

    response = client.get_request(entity=entity)

    href = response.get("items", [])[0].get("links", [])[0].get("href", "")

    return UserLegislativeID(legislative_id=get_id_from_links(href))
