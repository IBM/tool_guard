from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.get_id_from_links import get_id_from_links
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class AssignmentManagersResult:
    """Represents the response from getting a assignment manager's unique id from Oracle HCM."""

    manager_uniq_id: str


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def get_all_assignment_managers(
    worker_id: str, period_of_service_id: int, assignment_uniq_id: str, manager_type: str
) -> AssignmentManagersResult:
    """
    Gets assignment manager's unique id from Oracle HCM.

    Args:
        worker_id: The worker_id uniquely identifies workers within the Oracle HCM, returned by the
            `get_user_oracle_ids` tool.
        period_of_service_id: The period_of_service_id of the worker's work relationship as returned
            by `get_assignment_details` tool.
        assignment_uniq_id: The assignment_uniq_id of the worker's assignment as returned by
            `get_assignment_details` tool.
        manager_type: The manager_type to retrieve manager_uniq_id from assignment managers (Eg.
            PROJECT_MANAGER, LINE_MANAGER).

    Returns:
        The assignment manager's unique id within Oracle HCM.
    """
    client = get_oracle_hcm_client()

    response = client.get_request(
        entity=f"workers/{worker_id}/child/workRelationships/{period_of_service_id}/child/assignments/{assignment_uniq_id}/child/managers",
        q_expr=f"ManagerType={manager_type}",
    )
    href = response.get("items", [])[0].get("links", [])[0].get("href", "")
    return AssignmentManagersResult(manager_uniq_id=get_id_from_links(href))
