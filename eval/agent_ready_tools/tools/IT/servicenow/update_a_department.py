from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class UpdateDepartmentResponse:
    """Represents the update response of the department in ServiceNow."""

    http_code: int


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def update_a_department(
    department_name_system_id: str,
    description: Optional[str] = None,
    head_count: Optional[str] = None,
    business_unit_name: Optional[str] = None,
    department_head_system_id: Optional[str] = None,
    cost_center_name: Optional[str] = None,
    primary_contact_system_id: Optional[str] = None,
) -> UpdateDepartmentResponse:
    """
    updates a department in ServiceNow.

    Args:
        department_name_system_id: The system_id of the department name returned by the
            `get_departments` tool.
        description: The description of the department.
        head_count: The head count of the department.
        business_unit_name: The value of the business unit, returned by the `get_business_units`
            tool.
        department_head_system_id: The system_id of the user name returned by the `get_system_users`
            tool.
        cost_center_name: The value of the cost center, returned by the `get_cost_centers` tool.
        primary_contact_system_id: The system_id of the user name returned by the `get_system_users`
            tool.

    Returns:
        The result from performing the update a department.
    """

    client = get_servicenow_client()
    payload = {
        "description": description,
        "head_count": head_count,
        "business_unit": business_unit_name,
        "dept_head": department_head_system_id,
        "cost_center": cost_center_name,
        "primary_contact": primary_contact_system_id,
    }

    payload = {key: value for key, value in payload.items() if value}

    response = client.patch_request(
        entity="cmn_department",
        entity_id=department_name_system_id,
        payload=payload,
    )
    return UpdateDepartmentResponse(http_code=response["status_code"])
