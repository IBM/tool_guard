from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class OracleGetCompensationHistory:
    """Represents compensation history details of a user in Oracle HCM."""

    salary_frequency_code: Optional[str]
    currency_code: str
    date_from: str
    date_to: str
    salary_amount: float
    annual_salary: float


@dataclass
class OracleGetCompensationHistoryResponse:
    """Represents the response from getting a user's compensation history in Oracle HCM."""

    compensation_history: List[OracleGetCompensationHistory]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def get_compensation_history(assignment_id: int) -> OracleGetCompensationHistoryResponse:
    """
    Gets a user's compensation history in Oracle HCM.

    Args:
        assignment_id: The assignment_id uniquely identifying them within the Oracle HCM returned by
            the `get_assignment_details` tool.

    Returns:
        The user's compensation history.
    """
    client = get_oracle_hcm_client()

    response = client.get_request(
        "salaries",
        q_expr=f"AssignmentId={assignment_id}",
    )

    compensation_history: list[OracleGetCompensationHistory] = []

    for result in response.get("items", ""):
        compensation_history.append(
            OracleGetCompensationHistory(
                salary_frequency_code=result.get("SalaryFrequencyCode"),
                currency_code=result.get("CurrencyCode", ""),
                date_from=result.get("DateFrom", ""),
                date_to=result.get("DateTo", ""),
                salary_amount=result.get("SalaryAmount", ""),
                annual_salary=result.get("AnnualSalary", ""),
            )
        )
    return OracleGetCompensationHistoryResponse(compensation_history=compensation_history)
