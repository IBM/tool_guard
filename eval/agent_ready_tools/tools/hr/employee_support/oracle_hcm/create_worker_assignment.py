from typing import Any

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class CreateWorkerAssignmentResponse:
    """Represents the result of creating a worker's assignment in Oracle HCM."""

    assignment_id: str
    assignment_name: str
    assignment_status: str


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def create_worker_assignment(
    worker_unique_id: str,
    period_of_service_id: str,
    action_code: str,
    business_unit_id: str,
) -> CreateWorkerAssignmentResponse:
    """
    Creates a worker assignment in Oracle HCM.

    Args:
        worker_unique_id: The unique identifier of the worker, returned by the tool
            `get_user_oracle_ids`
        period_of_service_id: The unique identifier of the worker's work relationship, returned by
            the tool `get_assignment_details`.
        action_code: The action code of the assignment, returned by the tool `get_action_ids`.
        business_unit_id: The id of the business unit, returned by the tool `get_business_units`.

    Returns:
        The result of create operation performed on an assignment.
    """

    client = get_oracle_hcm_client()

    entity = f"workers/{worker_unique_id}/child/workRelationships/{period_of_service_id}/child/assignments"

    payload: dict[str, Any] = {"ActionCode": action_code, "BusinessUnitId": business_unit_id}

    payload = {key: value for key, value in payload.items() if value}

    response = client.post_request(entity=entity, payload=payload)

    result = CreateWorkerAssignmentResponse(
        assignment_id=response.get("AssignmentId", ""),
        assignment_name=response.get("AssignmentName", ""),
        assignment_status=response.get("AssignmentStatusType", ""),
    )

    return result
