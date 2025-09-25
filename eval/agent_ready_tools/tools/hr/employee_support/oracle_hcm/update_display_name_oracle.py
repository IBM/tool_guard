from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class OracleUpdateDisplayNameResponse:
    """Represents the response from updating a user's display name in Oracle HCM."""

    first_name: str
    last_name: str
    display_name: str


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def update_display_name_oracle(
    worker_id: str, names_id: str, first_name: str, last_name: str
) -> OracleUpdateDisplayNameResponse:
    """
    Updates user's display name in Oracle HCM.

    Args:
        worker_id: The worker_id uniquely identifying them within the Oracle HCM returned by the
            `get_user_oracle_ids` tool.
        names_id: The names_id uniquely identifying them within the Oracle HCM returned by the
            `get_user_names_id` tool.
        first_name: The first name of the user in Oracle HCM.
        last_name: The last name of the user in Oracle HCM.

    Returns:
        The worker's updated info.
    """
    client = get_oracle_hcm_client()

    response = client.update_request(
        entity=f"workers/{worker_id}/child/names/{names_id}",
        payload={"FirstName": first_name, "LastName": last_name},
    )

    return OracleUpdateDisplayNameResponse(
        first_name=response.get("FirstName", ""),
        last_name=response.get("LastName", ""),
        display_name=response.get("DisplayName", ""),
    )
