from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class InitiateManagerChangeResult:
    """Represents the result of a manager change in Oracle HCM."""

    manager_assignment_number: str
    manager_type: str
    action_code: str


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def initiate_manager_change(
    worker_id: str,
    period_of_service_id: int,
    assignment_uniq_id: str,
    manager_uniq_id: str,
    manager_assignment_number: str,
    manager_type: str,
) -> InitiateManagerChangeResult:
    """
    Initiate manager change for user in Oracle HCM.

    Args:
        worker_id: The worker_id uniquely identifies workers within the Oracle HCM, returned by the
            `get_user_oracle_ids` tool.
        period_of_service_id: The period_of_service_id of the worker's work relationship as returned
            by `get_assignment_details` tool.
        assignment_uniq_id: The assignment_uniq_id of the worker's assignment as returned by
            `get_assignment_details` tool.
        manager_uniq_id: The manager_uniq_id of the worker's manager as returned by the
            `get_all_assignment_managers` tool.
        manager_assignment_number: The manager_assignment_number of the manager as returned by the
            `get_all_managers` tool.
        manager_type: The manager_type to initiate manager transfer (Eg. PROJECT_MANAGER,
            LINE_MANAGER).

    Returns:
        The result from performing the initiate manager change for user.
    """

    client = get_oracle_hcm_client()
    payload = {
        "ActionCode": "MANAGER_CHANGE",
        "ManagerAssignmentNumber": manager_assignment_number,
        "ManagerType": manager_type,
    }

    payload = {key: value for key, value in payload.items() if value}
    entity = f"workers/{worker_id}/child/workRelationships/{period_of_service_id}/child/assignments/{assignment_uniq_id}/child/managers/{manager_uniq_id}"
    response = client.update_request(payload=payload, entity=entity)

    return InitiateManagerChangeResult(
        manager_assignment_number=response.get("ManagerAssignmentNumber", ""),
        manager_type=response.get("ManagerType", ""),
        action_code=response.get("ActionCode", ""),
    )
