from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.adobe_workfront_client import get_adobe_workfront_client
from agent_ready_tools.utils.tool_credentials import ADOBE_WORKFRONT_CONNECTIONS


@dataclass
class AdobeDeleteTaskResponse:
    """Represents the result of a delete operation performed on a task in Adobe Workfront."""

    http_code: int


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=ADOBE_WORKFRONT_CONNECTIONS,
)
def adobe_delete_task(task_id: str) -> AdobeDeleteTaskResponse:
    """
    Deletes a task in Adobe Workfront.

    Args:
        task_id: The id of the task, returned by the `list_all_tasks` tool.

    Returns:
        The status of the delete operation.
    """

    client = get_adobe_workfront_client()

    http_code = client.delete_request(entity=f"task/{task_id}")

    return AdobeDeleteTaskResponse(http_code=http_code)
