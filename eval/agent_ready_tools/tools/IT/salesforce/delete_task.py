from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from pydantic.dataclasses import dataclass
from simple_salesforce.exceptions import SalesforceError

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@dataclass
class DeleteTaskResponse:
    """Represents the update response of the incident in ServiceNow."""

    http_code: int


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def delete_task(
    task_id: str,
) -> DeleteTaskResponse:
    """
    Deletes a task in Salesforce.

    Args:
        task_id: The id of the task in Salesforce returned by the tool 'list_tasks'.

    Returns:
        The deleted task status.
    """
    client = get_salesforce_client()

    http_code = None

    try:
        response = client.salesforce_object.Task.delete(task_id)  # type: ignore[operator]
        http_code = response.status_code if hasattr(response, "status_code") else response
    except SalesforceError as err:
        http_code = err.status

    return DeleteTaskResponse(http_code)
