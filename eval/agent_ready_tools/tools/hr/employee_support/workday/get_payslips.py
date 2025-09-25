from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.workday_client import get_workday_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@dataclass
class Payslip:
    """Represents a payslip in Workday."""

    description: str
    gross: str
    net: str
    date: str


@dataclass
class PayslipsResponse:
    """Represents the response from getting a user's payslips in Workday."""

    payslips: list[Payslip]


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def get_payslips(user_id: str) -> PayslipsResponse:
    """
    Gets a user's payslips from Workday.

    Args:
        user_id: The user's id uniquely identifying them within the Workday API.

    Returns:
        The user's payslips.
    """
    client = get_workday_client()

    url = f"api/v1/{client.tenant_name}/workers/{user_id}/paySlips"
    response = client.get_request(url=url)

    payslips: list[Payslip] = []
    for slip in response["data"]:
        payslips.append(
            Payslip(
                description=slip.get("descriptor", ""),
                gross=slip.get("gross", ""),
                net=slip.get("net", ""),
                date=slip.get("date", ""),
            )
        )
    return PayslipsResponse(payslips=payslips)
