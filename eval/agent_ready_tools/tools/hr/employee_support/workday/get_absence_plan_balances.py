from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.workday_client import get_workday_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@dataclass
class AbsencePlanBalance:
    """Represents an absence plan balance in Workday."""

    plan_name: str
    unit: str
    quantity: str
    effective_date: str


@dataclass
class AbsencePlanBalanceResponse:
    """Represents the response from getting a user's absence plan balances in Workday."""

    absence_plans: list[AbsencePlanBalance]


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def get_absence_plan_balances(user_id: str) -> AbsencePlanBalanceResponse:
    """
    Gets a user's absence plan balances in Workday.

    Args:
        user_id: The user's id uniquely identifying them within the Workday API.

    Returns:
        The user's absence plan balances.
    """
    client = get_workday_client()

    url = f"api/absenceManagement/v1/{client.tenant_name}/balances"
    params = {"worker": user_id}
    response = client.get_request(url=url, params=params)

    absence_plans: list[AbsencePlanBalance] = []
    for report in response["data"]:
        absence_plans.append(
            AbsencePlanBalance(
                plan_name=report["absencePlan"]["descriptor"],
                unit=report["unit"]["descriptor"],
                quantity=report.get("quantity", "0"),
                effective_date=report["effectiveDate"],
            )
        )
    return AbsencePlanBalanceResponse(absence_plans=absence_plans)
