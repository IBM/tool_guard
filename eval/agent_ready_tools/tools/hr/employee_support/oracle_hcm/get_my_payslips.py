from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class OraclePayslip:
    """Represents payslip details of a user in Oracle HCM."""

    start_date: str
    end_date: str
    payment_date: str
    currency: str
    amount: float


@dataclass
class OraclePayslipResponse:
    """Represents the response from getting a user's payslip in Oracle HCM."""

    payslips: List[OraclePayslip]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def get_my_payslips(person_id: int, start_date: str, end_date: str) -> OraclePayslipResponse:
    """
    Gets a user's payslips in Oracle HCM.

    Args:
        person_id: The person_id uniquely identifying them within the Oracle HCM returned by the
            `get_user_oracle_ids` tool.
        start_date: The start date to get payslips in ISO 8601 format (e.g., YYYY-MM-DD).
        end_date: The end date to get payslips in ISO 8601 format (e.g., YYYY-MM-DD).

    Returns:
        The user's payslips.
    """
    client = get_oracle_hcm_client()

    response = client.get_request(
        "payslips",
        q_expr=f"PersonId={person_id};PeriodStartDate>='{start_date}';PeriodEndDate<='{end_date}'",
    )

    payslips: list[OraclePayslip] = []

    for result in response["items"]:
        payslips.append(
            OraclePayslip(
                amount=result.get("Amount", ""),
                start_date=result.get("PeriodStartDate", ""),
                end_date=result.get("PeriodEndDate", ""),
                currency=result.get("CurrencyCode", ""),
                payment_date=result.get("PaymentDate", ""),
            )
        )
    return OraclePayslipResponse(payslips=payslips)
