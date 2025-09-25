from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class Department:
    """Represents a department in SAP SuccessFactors."""

    department_external_code: str
    department_name: str


@dataclass
class DepartmentResponse:
    """Represents the response of the list of departments in SAP SuccessFactors."""

    departments: List[Department]


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def search_departments_by_division_and_country(
    division_name: str,
    country: str,
) -> DepartmentResponse:
    """
    Gets the list of departments according to the division and country of company from SAP
    SuccessFactors.

    Args:
        division_name: The division_name within the SAP SuccessFactors API returned by the tool
            `search_division_by_business_unit`.
        country: The country to which the user belongs in SAP SuccessFactors, as returned by
            `get_country_of_employment` tool.

    Returns:
        The department external code and department name.
    """
    client = get_sap_successfactors_client()

    response = client.get_request(
        "FODepartment",
        filter_expr=f"cust_toDivision/name eq '{division_name}' and cust_toLegalEntity/country eq '{country}'",
        select_expr=f"name,externalCode",
        expand_expr=f"cust_toDivision,cust_toLegalEntity",
    )
    departments: list[Department] = []
    for result in response["d"]["results"]:
        departments.append(
            Department(
                department_external_code=result.get("externalCode"),
                department_name=result.get("name"),
            )
        )
    return DepartmentResponse(departments=departments)
