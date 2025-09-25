from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class DeleteDepartmentResponse:
    """Represents the deletion of the department in ServiceNow."""

    http_code: int


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def delete_a_department(department_name_system_id: str) -> DeleteDepartmentResponse:
    """
    Deletes a department in ServiceNow.

    Args:
        department_name_system_id: The system_id of the department name returned by the
            `get_departments` tool.

    Returns:
        Confirmation of a department deletion.
    """

    client = get_servicenow_client()

    response = client.delete_request(entity="cmn_department", entity_id=department_name_system_id)
    return DeleteDepartmentResponse(http_code=response)
