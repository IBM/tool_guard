from datetime import datetime
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class CompensationDetailsResult:
    """Represents a worker's compensation details in Oracle HCM."""

    annual_salary: Optional[str]
    currency: Optional[str]
    comparative_ratio: Optional[str]
    adjustment_amount: Optional[str]
    adjustment_percentage: Optional[str]
    effective_period: Optional[str]
    action_name: Optional[str]
    salary_basis_name: Optional[str]
    legal_employer_name: Optional[str]
    grade_name: Optional[str]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def get_current_compensation_details_oracle(assignment_id: str) -> CompensationDetailsResult:
    """
    Gets a user's current compensation details in Oracle HCM.

    Args:
        assignment_id: The assignment id of the worker's assignment as returned by
            `get_assignment_details` tool.

    Returns:
        worker's current compensation details.
    """

    client = get_oracle_hcm_client()

    current_date = datetime.today().date()

    response = client.get_request(
        entity="salaries",
        finder_expr=f'findByAssignmentIdAndDate;AssignmentId={assignment_id},EffectiveDate="{current_date}"',
    )

    result = response["items"]

    if len(result) == 0:
        return CompensationDetailsResult(
            annual_salary=None,
            currency=None,
            comparative_ratio=None,
            adjustment_amount=None,
            adjustment_percentage=None,
            effective_period=None,
            action_name=None,
            salary_basis_name=None,
            legal_employer_name=None,
            grade_name=None,
        )

    return CompensationDetailsResult(
        annual_salary=str(result[0].get("AnnualSalary", "")),
        currency=result[0].get("CurrencyCode", ""),
        comparative_ratio=str(result[0].get("CompaRatio", "")),
        adjustment_amount=str(result[0].get("AdjustmentAmount", "")),
        adjustment_percentage=str(result[0].get("AdjustmentPercentage", "")),
        effective_period=str(result[0].get("DateFrom", "")),
        action_name=str(result[0].get("ActionName", "")),
        salary_basis_name=str(result[0].get("SalaryBasisName", "")),
        legal_employer_name=str(result[0].get("LegalEmployerName", "")),
        grade_name=str(result[0].get("GradeName", "")),
    )
