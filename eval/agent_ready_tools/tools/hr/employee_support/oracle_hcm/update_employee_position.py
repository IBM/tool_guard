from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_assignment_details import (
    get_worker_work_relationship,
)
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


class Constants:
    """The class containing the list of constants used in this file."""

    TRANSFER_ACTION_CODE = "TRANSFER"


@dataclass
class OracleEmployeePositionResponse:
    """Represents the response from updating a user's employee position in Oracle HCM."""

    http_code: int
    message: Optional[str]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def update_employee_position(
    worker_id: str, assignment_uniq_id: str, position_id: str
) -> OracleEmployeePositionResponse:
    """
    Updates the position of an employee in Oracle HCM.

    Args:
        worker_id: The worker_id uniquely identifying a worker within the Oracle HCM is returned by
            the `get_user_oracle_ids` tool.
        assignment_uniq_id: The assignment_uniq_id of the worker's assignment as returned by
            `get_assignment_details` tool.
        position_id: The position_id of the worker's position as returned by `get_positions_oracle`
            tool.

    Returns:
        The result from performing the update employee position.
    """

    client = get_oracle_hcm_client()

    get_worker_work = get_worker_work_relationship(worker_id).worker_work_relationship[0]
    period_of_service_id = get_worker_work.period_of_service_id

    payload = {
        "ActionCode": Constants.TRANSFER_ACTION_CODE,
        "PositionId": position_id,
    }
    response = client.update_request(
        entity=f"workers/{worker_id}/child/workRelationships/{period_of_service_id}/child/assignments/{assignment_uniq_id}",
        payload=payload,
    )

    return OracleEmployeePositionResponse(
        http_code=response.get("status_code", ""),
        message=response.get("message", None),
    )
