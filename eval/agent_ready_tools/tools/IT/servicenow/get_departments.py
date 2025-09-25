from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class GetDepartments:
    """Represents the details of a department in ServiceNow."""

    system_id: Optional[str]
    department_name: Optional[str]
    parent_department: Optional[str]
    department_description: Optional[str]
    business_unit: Optional[str]
    department_head: Optional[str]
    company: Optional[str]
    primary_contact: Optional[str]


@dataclass
class GetDepartmentsResponse:
    """A list of departments configured in a ServiceNow deployment."""

    departments: list[GetDepartments]


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def get_departments(
    department_name: Optional[str] = None,
    business_unit: Optional[str] = None,
    limit: Optional[int] = 10,
    skip: Optional[int] = 0,
) -> GetDepartmentsResponse:
    """
    Gets a list of departments configured in this ServiceNow deployment.

    Args:
        department_name: The name of the department.
        business_unit: The business unit name of the system user returned by `get_business_units`
            tool.
        limit: The maximum number department to retrieve in a single API call. Defaults to 10. Use
            this to control the size of the result set.
        skip: The number of department to skip for pagination

    Returns:
        A list of departments.
    """

    client = get_servicenow_client()

    params = {
        "department_name": department_name,
        "business_unit": business_unit,
        "sysparm_limit": limit,
        "sysparm_offset": skip,
        "sysparm_display_value": True,
    }

    params = {key: value for key, value in params.items() if value is not None}

    response = client.get_request(entity="cmn_department", params=params)
    results = response["result"]
    departments_list = [
        GetDepartments(
            system_id=item.get("sys_id", ""),
            department_name=item.get("name", ""),
            parent_department=(
                item.get("parent_department").get("display_value")
                if item.get("parent_department")
                else ""
            ),
            department_description=item.get("description", ""),
            business_unit=item.get("business_unit", ""),
            department_head=(
                item.get("dept_head").get("display_value") if item.get("dept_head") else ""
            ),
            company=item.get("company").get("display_value") if item.get("company") else "",
            primary_contact=(
                item.get("primary_contact").get("display_value")
                if item.get("primary_contact")
                else ""
            ),
        )
        for item in results
    ]

    return GetDepartmentsResponse(departments=departments_list)
