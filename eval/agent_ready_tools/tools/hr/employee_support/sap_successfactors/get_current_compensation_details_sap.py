from dataclasses import field
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class CurrentCompensationDetails:
    """Represents a user's compensation details in SAP SuccessFactors."""

    currency: Optional[str] = field(default=None)
    yearly_base_salary: Optional[float] = field(default=None)


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def get_current_compensation_details_sap(user_id: str) -> CurrentCompensationDetails:
    """
    Gets a user's current compensation details in SAP SuccessFactors.

    Args:
        user_id: The user id uniquely identifying the user within SAP SuccessFactors.

    Returns:
        The user's compensation details.
    """
    client = get_sap_successfactors_client()

    expand_key = "empCompensationCalculatedNav"
    response = client.get_request(
        "EmpCompensation", filter_expr=f"userId eq '{user_id}'", expand_expr=expand_key
    )
    results = response["d"]["results"]

    current_compensation_details = CurrentCompensationDetails()
    if len(results) == 0:
        return current_compensation_details

    compensation_details = results[0].get(
        expand_key
    )  # TODO What if there are multiple results for the employee?
    current_compensation_details.currency = compensation_details.get("currency", None)
    current_compensation_details.yearly_base_salary = compensation_details.get(
        "yearlyBaseSalary", None
    )
    return current_compensation_details
