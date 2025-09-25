from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.box_client import get_box_client
from agent_ready_tools.utils.tool_credentials import BOX_CONNECTIONS


@dataclass
class CreateTaskResponse:
    """Represents the result of creating a task in Box."""

    task_id: str
    file_id: str
    message: str
    action: Optional[str]
    completion_rule: Optional[str]
    http_code: Optional[int]


@tool(expected_credentials=BOX_CONNECTIONS)
def create_a_task(
    file_id: str,
    message: str,
    action: Optional[str] = None,
    completion_rule: Optional[str] = None,
) -> CreateTaskResponse:
    """
    Creates a task for a file in Box.

    Args:
        file_id: The id of the file returned by `get_file_details_by_name` tool.
        message: A message to include with the task.
        action: The action of the task, possible values are review, complete and defaults to review.
        completion_rule: The completion rule of the task, possible values are all_assignees,
            any_assignee and defaults to all_assignees.

    Returns:
        The result from performing the creation of a task.
    """
    client = get_box_client()

    payload = {
        "item": {"id": file_id, "type": "file"},
        "action": action,
        "message": message,
        "completion_rule": completion_rule,
    }
    payload = {key: value for key, value in payload.items() if value}

    response = client.post_request(entity="tasks", data=payload)
    return CreateTaskResponse(
        task_id=response.get("id", ""),
        message=response.get("message", ""),
        action=response.get("action", ""),
        completion_rule=response.get("completion_rule", ""),
        file_id=response.get("item", []).get("name", ""),
        http_code=response.get("status_code", None),
    )
