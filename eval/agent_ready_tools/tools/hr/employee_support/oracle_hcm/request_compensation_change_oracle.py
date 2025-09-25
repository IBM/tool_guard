from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class RequestCompensationChangeResult:
    """Represents the result of requesting compensation change in Oracle HCM."""

    message: Optional[str] = None
    effective_date_from: Optional[str] = None
    salary_amount: Optional[int] = 0


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def request_compensation_change_oracle(
    assignment_id: int,
    salary_basis_id: str,
    effective_date_from: str,
    salary_amount: int,
    action_id: str,
) -> RequestCompensationChangeResult:
    """
    Updates salary amount of an employee in Oracle HCM.

    Args:
        assignment_id: The assignment id of the worker's assignment as returned by
            `get_assignment_details` tool.
        salary_basis_id: The salary basis id representing the type of salary of the worker as
            returned by `get_salary_bases` tool.
        effective_date_from: The date on which salary change takes place based on ISO: 8601 format
            (e.g., "YYYY-MM-DD").
        salary_amount: The salary amount to be updated for the worker.
        action_id: The action name representing the reason for salary change of the worker as
            returned by `get_action_ids` tool.

    Returns:
        The updated salary amount of an worker.
    """

    client = get_oracle_hcm_client()
    payload = {
        "AssignmentId": assignment_id,
        "SalaryBasisId": salary_basis_id,
        "DateFrom": effective_date_from,
        "SalaryAmount": salary_amount,
        "ActionId": action_id,
    }
    entity = "salaries"
    response = client.post_request(entity=entity, payload=payload)

    if response.get("status_code") != 201:
        return RequestCompensationChangeResult(message=response.get("message"))
    else:
        return RequestCompensationChangeResult(
            effective_date_from=response.get("DateFrom", ""),
            salary_amount=response.get("SalaryAmount", ""),
        )
