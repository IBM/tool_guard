from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class GetEmployeeLocationResponse:
    """Represents the employee's location as retrieved from the EmpJob entity."""

    location: Optional[str]
    company: Optional[str]


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def get_employee_location(user_id: str) -> GetEmployeeLocationResponse:
    """
    Gets an employee's location in SAP SuccessFactors.

    Args:
        user_id: The user's unique identifier in SAP SuccessFactors.

    Returns:
        The employee's location (as stored in the EmpJob record), if found.
    """
    client = get_sap_successfactors_client()

    filter_expr = f"userId eq '{user_id}'"
    response = client.get_request(
        entity="EmpJob", filter_expr=filter_expr, select_expr="location,company"
    )

    results = response.get("d", {}).get("results", [])
    employee_location = results[0].get("location") if results else None
    employee_company = results[0].get("company") if results else None
    return GetEmployeeLocationResponse(location=employee_location, company=employee_company)
