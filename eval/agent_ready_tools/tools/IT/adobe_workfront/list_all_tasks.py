from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.adobe_workfront_client import get_adobe_workfront_client
from agent_ready_tools.utils.tool_credentials import ADOBE_WORKFRONT_CONNECTIONS


@dataclass
class Task:
    """Represents the class for retrieving tasks in Adobe Workfront."""

    task_id: str
    task_number: str
    task_name: str
    status: Optional[str] = None
    project_start_date: Optional[str] = None
    project_complete_date: Optional[str] = None
    object_code: Optional[str] = None


@dataclass
class ListTasksResponse:
    """Represents the response for retrieving tasks in Adobe Workfront."""

    tasks: List[Task]


@tool(expected_credentials=ADOBE_WORKFRONT_CONNECTIONS)
def list_all_tasks(
    task_id: Optional[str] = None,
    task_name: Optional[str] = None,
    limit: Optional[int] = 100,
    skip: Optional[int] = 0,
) -> ListTasksResponse:
    """
    Gets a list of tasks from Adobe Workfront.

    Args:
        task_id: Filter tasks by task ID.
        task_name: Filter tasks by task name.
        limit: The maximum number of tasks to return. Default is 100.
        skip: The number of tasks to skip, default is 0.

    Returns:
        List of tasks.
    """

    client = get_adobe_workfront_client()
    params = {"ID": task_id, "name": task_name, "$$LIMIT": limit, "$$FIRST": skip}

    params = {key: value for key, value in params.items() if value is not None}
    response = client.get_request(entity="task/search", params=params)

    tasks: List[Task] = [
        Task(
            task_id=result.get("ID", ""),
            task_name=result.get("name", ""),
            task_number=str(result.get("taskNumber", "")),
            status=result.get("status", ""),
            project_start_date=result.get("projectedStartDate", ""),
            project_complete_date=result.get("projectedCompletionDate", ""),
            object_code=result.get("objCode", ""),
        )
        for result in response.get("data", [])
    ]

    return ListTasksResponse(
        tasks=tasks,
    )
