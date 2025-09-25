from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class DeleteSystemUserResponse:
    """Represents the result of an system user delete operation in Service Now."""

    http_code: int


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def delete_a_system_user(user_name_system_id: str) -> DeleteSystemUserResponse:
    """
    Deletes the system user in ServiceNow.

    Args:
        user_name_system_id: The system_id of the user name returned by the `get_system_users` tool.

    Returns:
        The result from performing the delete a system user.
    """

    client = get_servicenow_client()

    response = client.delete_request(entity="sys_user", entity_id=user_name_system_id)
    return DeleteSystemUserResponse(http_code=response)
