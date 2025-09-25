from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.box_client import get_box_client
from agent_ready_tools.utils.date_conversion import iso_8601_datetime_convert_to_date
from agent_ready_tools.utils.tool_credentials import BOX_CONNECTIONS


@dataclass
class BoxFileTasks:
    """Represents tasks on a Box file."""

    task_id: str
    message: str
    created_by: str
    creation_date: str
    action: Optional[str]
    assigned_to: Optional[str]
    due_date: Optional[str]
    is_completed: Optional[bool]
    completion_date: Optional[str]


@dataclass
class BoxFileTasksResult:
    """Represents the response from getting tasks on a Box file."""

    box_file_tasks: List[BoxFileTasks]


@tool(expected_credentials=BOX_CONNECTIONS)
def get_tasks(file_id: str) -> BoxFileTasksResult:
    """
    Gets tasks on a Box file.

    Args:
        file_id: The id of the file returned by the `get_file_details_by_name` tool.

    Returns:
        The tasks on a Box file.
    """
    client = get_box_client()

    response = client.get_request(
        entity=f"files/{file_id}/tasks",
    )
    box_file_tasks: list[BoxFileTasks] = []
    for result in response["entries"]:
        box_file_tasks.append(
            BoxFileTasks(
                task_id=result.get("id", ""),
                action=result.get("action", ""),
                message=result.get("message", ""),
                created_by=result.get("created_by", {}).get("name", ""),
                creation_date=iso_8601_datetime_convert_to_date(result.get("created_at", "")),
                assigned_to=(
                    result.get("task_assignment_collection", {})
                    .get("entries", [])[0]
                    .get("assigned_to", {})
                    .get("name", "")
                    if result.get("task_assignment_collection", {}).get("entries", [])
                    else ""
                ),
                due_date=(
                    iso_8601_datetime_convert_to_date(result.get("due_at", ""))
                    if result.get("due_at", "")
                    else ""
                ),
                is_completed=result.get("is_completed", ""),
                completion_date=(
                    iso_8601_datetime_convert_to_date(
                        result.get("task_assignment_collection", {})
                        .get("entries", [])[0]
                        .get("completed_at", "")
                    )
                    if result.get("task_assignment_collection", {}).get("entries", [])
                    and result.get("task_assignment_collection", {})
                    .get("entries", [])[0]
                    .get("completed_at", "")
                    else ""
                ),
            )
        )
    return BoxFileTasksResult(box_file_tasks=box_file_tasks)
