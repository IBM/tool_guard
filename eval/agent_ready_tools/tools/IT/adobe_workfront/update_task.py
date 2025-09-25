from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.adobe_workfront_client import get_adobe_workfront_client
from agent_ready_tools.tools.IT.adobe_workfront.adobe_workfront_schemas import (
    AdobeWorkfrontPriority,
    AdobeWorkfrontTaskStatus,
)
from agent_ready_tools.utils.tool_credentials import ADOBE_WORKFRONT_CONNECTIONS


@dataclass
class UpdateTaskResponse:
    """Represents the result for task updation in Adobe Workfront."""

    task_id: str
    name: str
    status: str


@tool(expected_credentials=ADOBE_WORKFRONT_CONNECTIONS)
def adobe_update_task(
    task_id: str,
    name: Optional[str] = None,
    status: Optional[AdobeWorkfrontTaskStatus] = None,
    priority: Optional[AdobeWorkfrontPriority] = None,
    description: Optional[str] = None,
    assigned_to_id: Optional[str] = None,
) -> UpdateTaskResponse:
    """
    Updates a task in Adobe Workfront.

    Args:
        task_id: The id of the task, returned by the `list_all_tasks` tool.
        name: The name of the task.
        status: The status of the task.
        priority: The priority of the task.
        description: The description of the task.
        assigned_to_id: The id of the user to whom the task is assigned, returned by the
            `list_users` tool.

    Returns:
        The result of updating a task.
    """

    client = get_adobe_workfront_client()

    payload: dict[str, Any] = {
        "name": name,
        "priority": AdobeWorkfrontPriority[priority.upper()].value if priority else None,
        "status": AdobeWorkfrontTaskStatus[status.upper()].value if status else None,
        "description": description,
        "assignedToID": assigned_to_id,
    }
    payload = {key: value for key, value in payload.items() if value}
    entity = f"task/{task_id}"
    response = client.put_request(entity=entity, payload=payload)
    data = response.get("data", {})
    result = UpdateTaskResponse(
        task_id=data.get("ID", ""),
        name=data.get("name", ""),
        status=AdobeWorkfrontTaskStatus(data.get("status")).name,
    )
    return result
