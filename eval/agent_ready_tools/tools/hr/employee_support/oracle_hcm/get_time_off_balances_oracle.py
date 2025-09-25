from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class OracleTimeOffBalance:
    """Represents a time off balance in Oracle HCM."""

    time_off_type: str
    time_off_balance: str


@dataclass
class OracleTimeOffBalancesResponse:
    """Represents the response from getting a user's time off balances in Oracle HCM."""

    balances: List[OracleTimeOffBalance]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def get_time_off_balances_oracle(person_id: str, date: str) -> OracleTimeOffBalancesResponse:
    """
    Gets a user's time off balances in Oracle HCM.

    Args:
        person_id: The person_id uniquely identifying them within the Oracle HCM returned by the
            `get_user_oracle_ids` tool.
        date: The date for which balance is calculated in ISO 8601 format (e.g., YYYY-MM-DD).

    Returns:
        The user's time off balances.
    """
    client = get_oracle_hcm_client()
    response = client.get_request(
        "planBalances",
        finder_expr=f"findByPersonIdPlanIdLevelDate;personId={person_id},balanceAsOfDate={date}",
    )

    time_off_balances: list[OracleTimeOffBalance] = []
    for result in response["items"]:
        time_off_balances.append(
            OracleTimeOffBalance(
                time_off_type=result.get("planName", ""),
                time_off_balance=result.get("formattedBalance", ""),
            )
        )
    return OracleTimeOffBalancesResponse(balances=time_off_balances)
