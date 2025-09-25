from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.adobe_workfront_client import get_adobe_workfront_client
from agent_ready_tools.tools.IT.adobe_workfront.adobe_workfront_schemas import (
    AdobeWorkfrontPriority,
)
from agent_ready_tools.utils.tool_credentials import ADOBE_WORKFRONT_CONNECTIONS


@dataclass
class AdobeCreateTaskResponse:
    """Represents the result for task creation in Adobe Workfront."""

    task_id: str
    name: str


@tool(expected_credentials=ADOBE_WORKFRONT_CONNECTIONS)
def create_task(
    project_id: str,
    name: str,
    priority: Optional[AdobeWorkfrontPriority] = None,
    description: Optional[str] = None,
    assigned_to_id: Optional[str] = None,
) -> AdobeCreateTaskResponse:
    """
    Creates a task in Adobe Workfront.

    Args:
        project_id: The id of the project, returned by the `list_projects` tool.
        name: The name of the task.
        priority: The priority of the task.
        description: The description of the task.
        assigned_to_id: The id of the user to whom the task is assigned, returned by the
            `list_users` tool.

    Returns:
        The result of creating a task.
    """

    client = get_adobe_workfront_client()

    payload: dict[str, Any] = {
        "projectID": project_id,
        "name": name,
        "priority": int(AdobeWorkfrontPriority[priority.upper()].value) if priority else None,
        "description": description,
        "assignedToID": assigned_to_id,
    }
    payload = {key: value for key, value in payload.items() if value}

    response = client.post_request(entity="task", payload=payload)
    data = response.get("data", {})
    return AdobeCreateTaskResponse(task_id=data.get("ID", ""), name=data.get("name", ""))
