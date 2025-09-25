from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class CreateDepartmentResult:
    """Represents the result of create a department in ServiceNow."""

    system_id: str
    department_name: str


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def create_a_department(
    department_name: str, description: Optional[str] = None, department_id: Optional[str] = None
) -> CreateDepartmentResult:
    """
    Creates a department in ServiceNow.

    Args:
        department_name: The name of the department.
        description: The description of the department.
        department_id: The unique identifier of the department.

    Returns:
        The result for performing the creation of department.
    """
    client = get_servicenow_client()

    payload: dict[str, Any] = {
        "name": department_name,
        "description": description,
        "id": department_id,
    }

    response = client.post_request(entity="cmn_department", payload=payload)
    result = response.get("result", None)
    return CreateDepartmentResult(
        department_name=result and result.get("name", ""),
        system_id=result.get("sys_id", ""),
    )
