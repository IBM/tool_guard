from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class OracleBenefitPlans:
    """Represents the response from getting a benefit plan from Oracle HCM."""

    plan_id: int
    plan_name: str
    person_name: str
    program_name: str
    option_name: str
    enrollment_coverage_start_date: str
    currency_code: str
    coverage_amount: Optional[str] = None
    enrollment_coverage_end_date: Optional[str] = None


@dataclass
class OracleBenefitPlansResponse:
    """Represents the response from getting a list of benefit plans from Oracle HCM."""

    benefit_plans: List[OracleBenefitPlans]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def view_benefit_plans(person_id: int) -> OracleBenefitPlansResponse:
    """
    Gets benefits plans from Oracle HCM.

    Args:
        person_id: The person_id uniquely identifies them within the Oracle HCM returned by the
            `get_user_oracle_ids` tool.

    Returns:
        The list of benefit plans.
    """
    client = get_oracle_hcm_client()

    q_expr = f"PersonId={person_id}"
    response = client.get_request("benefitEnrollments", q_expr=q_expr)

    benefit_plans: list[OracleBenefitPlans] = []
    for result in response["items"]:
        benefit_plans.append(
            OracleBenefitPlans(
                plan_id=result.get("PlanId", ""),
                plan_name=result.get("PlanName", ""),
                person_name=result.get("PersonName", ""),
                program_name=result.get("ProgramName", ""),
                option_name=result.get("OptionName", ""),
                coverage_amount=result.get("CoverageAmount", ""),
                enrollment_coverage_start_date=result.get("EnrollmentCoverageStartDate", ""),
                enrollment_coverage_end_date=result.get("EnrollmentCoverageEndDate", ""),
                currency_code=result.get("CurrencyCode", ""),
            )
        )
    return OracleBenefitPlansResponse(benefit_plans=benefit_plans)
