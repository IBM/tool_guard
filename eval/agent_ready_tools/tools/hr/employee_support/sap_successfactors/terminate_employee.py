from datetime import datetime, timezone
from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class TerminateEmployeeResult:
    """Represents the result of terminating an employee in SAP SuccessFactors."""

    http_code: int


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def terminate_employee(
    person_id_external: str,
    user_id: str,
    end_date: str,
    event_reason_external_code: str,
    stock_end_date: Optional[str] = None,
    benefits_end_date: Optional[str] = None,
    bonus_pay_expiration_date: Optional[str] = None,
    eligible_for_sal_continuation: Optional[str] = None,
    last_date_worked: Optional[str] = None,
    ok_to_rehire: Optional[bool] = None,
    payroll_end_date: Optional[str] = None,
    regret_termination: Optional[bool] = None,
    salary_end_date: Optional[str] = None,
) -> TerminateEmployeeResult:
    """
    Terminates a user's employment in SAP SuccessFactors.

    Args:
        person_id_external: The employee's person_id_external uniquely identifying them within the
            SuccessFactors API.
        user_id: The user's ID uniquely identifying the employee within the SuccessFactors
        end_date: The employee's date of termination
        event_reason_external_code: The external_code of event reason return from get_event_reasons
            tool (FOEventReason type)
        stock_end_date: The end date of an employee can use their vested stock options after leaving
            the company (Optional)
        benefits_end_date: The end date of an employee's benefits, like health insurance, remain
            active after they leave the company (Optional)
        bonus_pay_expiration_date: The last day an employee can claim or receive their bonus payment
            (Optional)
        eligible_for_sal_continuation: Whether an employee qualifies to keep receiving their salary
            for a certain period after their employment ends (Optional)
        last_date_worked: Last date of the employee performs their job (Optional)
        ok_to_rehire: Whether the employee is eligible to be rehired by the company in the future
            (Optional)
        payroll_end_date: End date of the payroll period (Optional)
        regret_termination: Whether the company regrets the termination of the employee (Optional)
        salary_end_date: The end date of the salary for an employee (Optional)

    Returns:
        The result from terminating the employee.
    """
    client = get_sap_successfactors_client()

    dt = datetime.strptime(end_date, "%Y-%m-%d")
    dt.replace(tzinfo=timezone.utc)
    end_date_milliseconds = int(dt.timestamp() * 1000)

    payload: dict[str, Any] = {
        "__metadata": {
            "uri": "EmpEmploymentTermination",
            "type": "SFOData.EmpEmploymentTermination",
        },
        "personIdExternal": person_id_external,
        "userId": user_id,
        "endDate": f"/Date({end_date_milliseconds})/",
        "eventReason": event_reason_external_code,
        "stockEndDate": stock_end_date,
        "benefitsEndDate": benefits_end_date,
        "bonusPayExpirationDate": bonus_pay_expiration_date,
        "eligibleForSalContinuation": eligible_for_sal_continuation,
        "lastDateWorked": last_date_worked,
        "okToRehire": ok_to_rehire,
        "payrollEndDate": payroll_end_date,
        "regretTermination": regret_termination,
        "salaryEndDate": salary_end_date,
    }
    payload = {key: value for key, value in payload.items() if value}

    response = client.upsert_request(payload=payload)
    return TerminateEmployeeResult(http_code=response["d"][0]["httpCode"])
