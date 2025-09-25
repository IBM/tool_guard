from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.date_conversion import sap_date_to_iso_8601
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class Wage:
    """Represents payslip details of a user in SAP SuccessFactors."""

    wage_type: Optional[str]
    amount: str


@dataclass
class SapPayslip:
    """Represents payslip details of a user in SAP SuccessFactors."""

    start_date: str
    end_date: str
    currency: str
    wages: List[Wage]


@dataclass
class SapPayslipResponse:
    """Represents the response from getting a user's payslip in SAP SuccessFactors."""

    payslips: List[SapPayslip]


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def get_payslip_details(user_id: str, start_date: str, end_date: str) -> SapPayslipResponse:
    """
    Gets a user's payslip details in SAP SuccessFactors.

    Args:
        user_id: The user's user_id uniquely identifying them within the SuccessFactors API.
        start_date: The start of a date range filter in ISO 8601 format (e.g., YYYY-MM-DD)
        end_date: The end of a date range filter in ISO 8601 format (e.g., YYYY-MM-DD).

    Returns:
        The user's payslip details.
    """
    client = get_sap_successfactors_client()

    response = client.get_request(
        "EmployeePayrollRunResults",
        filter_expr=f"userId eq '{user_id}' and startDateWhenPaid ge '{start_date}' and endDateWhenPaid le '{end_date}'",
        expand_expr="employeePayrollRunResultsItems",
    )
    payslips: list[SapPayslip] = []

    for result in response["d"]["results"]:
        # Get the start date, end date and currency of each payslip
        start_date_when_paid_iso = sap_date_to_iso_8601(result.get("startDateWhenPaid"))
        end_date_when_paid_iso = sap_date_to_iso_8601(result.get("endDateWhenPaid"))
        currency = result.get("currency")

        wages = []
        for item in result["employeePayrollRunResultsItems"]["results"]:
            # Iterate over the various wage types to include all payslip info
            wages.append(
                Wage(
                    wage_type=item.get("wageType"),
                    amount=item.get("amount"),
                )
            )
        payslips.append(
            SapPayslip(
                start_date=start_date_when_paid_iso,
                end_date=end_date_when_paid_iso,
                currency=currency,
                wages=wages,
            )
        )

    return SapPayslipResponse(payslips=payslips)
