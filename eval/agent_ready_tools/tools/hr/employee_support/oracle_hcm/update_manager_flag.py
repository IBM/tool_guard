from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.get_id_from_links import get_id_from_links
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class OracleManagerFlagResponse:
    """Represents the response from updating a user's manager flag in Oracle HCM."""

    assignment_uniq_id: str
    manager_flag: bool
    action_code: str


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def update_manager_flag(
    worker_id: str,
    period_of_service_id: str,
    action_code: str,
    assignment_uniq_id: str,
    is_manager: bool,
) -> OracleManagerFlagResponse:
    """
    Updates a user's manager flag in Oracle HCM.

    Args:
        worker_id: The worker_id uniquely identifying them within the Oracle HCM returned by the
            `get_user_oracle_ids` tool.
        period_of_service_id: The period_of_service_id uniquely identifying them within the Oracle
            HCM returned by the `get_assignment_details` tool.
        action_code: The action_code from the assigment in Oracle HCM returned by the
            `get_assignment_details` tool.
        assignment_uniq_id: The assignment_uniq_id uniquely identifying them within the Oracle HCM
            returned by the `get_assignment_details` tool.
        is_manager: Manager flag

    Returns:
        The worker's updated info.
    """
    client = get_oracle_hcm_client()

    response = client.update_request(
        entity=f"workers/{worker_id}/child/workRelationships/{period_of_service_id}/child/assignments/{assignment_uniq_id}",
        payload={"ManagerFlag": is_manager, "ActionCode": action_code},
    )

    href = response.get("links", [{}])[0].get("href", "")
    assignment_uniq_id = get_id_from_links(href)

    return OracleManagerFlagResponse(
        assignment_uniq_id=assignment_uniq_id,
        manager_flag=response.get("ManagerFlag", ""),
        action_code=response.get("ActionCode", ""),
    )
