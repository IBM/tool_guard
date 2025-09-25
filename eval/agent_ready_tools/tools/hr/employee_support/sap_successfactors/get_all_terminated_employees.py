from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class GetTerminatedEmployee:
    """Represents a single termination of an user in SAP SuccessFactors."""

    person_id_external: str
    user_id: str
    end_date: str
    event_reason: str


@dataclass
class GetAllTerminatedEmployeesResponse:
    """A list of terminated employees configured for a SuccessFactors deployment."""

    terminated_employees: list[GetTerminatedEmployee]


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def get_all_terminated_employees(person_id_external: str) -> GetAllTerminatedEmployeesResponse:
    """
    Gets a list of terminated employees configured for this SuccessFactors deployment.

    Args:
        person_id_external: The user's person_id_external uniquely identifying them within the
            SuccessFactors API for the logged in user.

    Returns:
        A list of terminated employees.
    """
    client = get_sap_successfactors_client()
    response = client.get_request(
        entity="EmpEmploymentTermination",
        filter_expr=f"employmentNav/empJobRelationshipNav/relUserId eq '{person_id_external}'",
        expand_expr="employmentNav/empJobRelationshipNav,jobInfoNav",
    )
    results = response["d"]["results"]

    terminated_employees_list = [
        GetTerminatedEmployee(
            person_id_external=employee.get("personIdExternal"),
            user_id=employee.get("userId"),
            end_date=employee.get("endDate"),
            event_reason=employee.get("jobInfoNav").get("eventReason"),
        )
        for employee in results
    ]

    return GetAllTerminatedEmployeesResponse(terminated_employees=terminated_employees_list)
