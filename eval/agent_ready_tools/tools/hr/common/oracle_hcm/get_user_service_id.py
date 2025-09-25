from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class UserServiceID:
    """Represents the response from getting a user's service id from Oracle HCM."""

    service_id: Optional[int]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def get_user_service_id(
    worker_id: str,
) -> UserServiceID:
    """
    Gets a user's `service_id` from Oracle HCM.

    Args:
        worker_id: The worker_id is the internal unique identifier hash string for a person in HCM
            returned by the `get_user_oracle_ids` tool.

    Returns:
        User Service ID which refers to a person's specific Work Relationship/Arrangement.
    """
    client = get_oracle_hcm_client()

    # Get service_id
    service_id_found = None
    result = client.get_request(
        entity=f"workers/{worker_id}/child/workRelationships",
    )

    service_result = result.get("items", {})[0]

    if service_result:
        service_id_found = service_result.get("PeriodOfServiceId")

    return UserServiceID(
        service_id=service_id_found,
    )
