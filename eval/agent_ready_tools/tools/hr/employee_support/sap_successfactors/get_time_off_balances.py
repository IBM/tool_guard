from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class SFTimeOffBalance:
    """Represents a time off balance in SAP SuccessFactors."""

    time_off_type: str
    time_off_balance: str


@dataclass
class SFTimeOffBalancesResponse:
    """Represents the response from getting a user's time off balances in SAP SuccessFactors.."""

    balances: List[SFTimeOffBalance]


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def get_time_off_balances(date: str, user_id: str) -> SFTimeOffBalancesResponse:
    """
    Gets a user's time off balances in SAP SuccessFactors.

    Args:
        date: The date for which the time account balances are requested in ISO 8601 format (e.g.,
            YYYY-MM-DD).
        user_id: The user's user_id uniquely identifying them within the SuccessFactors API.

    Returns:
        The user's time off balances.
    """
    client = get_sap_successfactors_client()

    response = client.get_time_management_request(
        endpoint="timeAccountBalances", params={"$at": date, "assignmentId": user_id}
    )

    timeoff_types: list[SFTimeOffBalance] = []
    for balance_type in response["value"]:
        timeoff_types.append(
            SFTimeOffBalance(
                time_off_type=balance_type["timeAccount"]["timeAccountType"]["externalName"],
                time_off_balance=balance_type["balances"]["available"][
                    "formattedWithUnitRoundedDown"
                ],
            ),
        )
    return SFTimeOffBalancesResponse(balances=timeoff_types)
